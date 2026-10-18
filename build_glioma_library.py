#!/usr/bin/env python3
"""Build a compact, versioned glioma biomarker reference FASTA library from official NCBI MANE.

The script selects exactly MANE Select transcript/protein accessions from the MANE summary,
then fetches only those records from NCBI E-utilities. Reference sequences are not tumor
variants, neoantigens, or clinical recommendations. Requires internet when run.
Usage: python build_glioma_library.py --out data/glioma_reference_library --max-mb 30
"""
from __future__ import annotations
import argparse,gzip,json,re,sys,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
PANEL=[
("IDH1","IDH hotspot; defining molecular class","classification"),("IDH2","IDH hotspot; defining molecular class","classification"),("ATRX","Astrocytoma IDH-mutant; chromatin remodeling","classification"),("TP53","Astrocytoma IDH-mutant / H3-altered contexts","classification"),("CIC","Oligodendroglioma IDH-mutant, 1p/19q-codeleted","classification"),("FUBP1","Oligodendroglioma; recurrent alteration","classification"),("TERT","Promoter hotspot in IDH-wt GBM/oligodendroglioma; mRNA/protein is not the promoter","promoter-specific"),("EGFR","Amplification/variants including EGFRvIII; GBM","target/diagnostic"),("CDKN2A","Homozygous deletion informs grade in IDH-mutant astrocytoma","classification"),("CDKN2B","Co-deletion with CDKN2A; locus-level assay","classification"),("MGMT","Promoter methylation; treatment-context biomarker","epigenetic"),("H3-3A","H3 K27/G34 variants; pediatric-type glioma contexts","histone"),("ACVR1","Alterations in a subset of diffuse midline glioma","pediatric"),("PDGFRA","Amplification/alteration; glioma signaling driver subset","target"),("EZHIP","Overexpression/alteration in H3 K27-altered midline glioma","pediatric"),("BRAF","V600E/fusions; subset-specific therapeutic relevance","target"),("NF1","MAPK pathway; NF1-associated/pediatric and GBM subsets","pathway/predisposition"),("PTEN","PI3K pathway loss; recurrent tumor suppressor alteration","pathway"),("RB1","Cell-cycle pathway alteration","pathway"),("PIK3CA","PI3K pathway hotspot alterations","pathway/target"),("PIK3R1","PI3K pathway alterations","pathway"),("CDK4","Amplification/cell-cycle axis","target"),("MDM2","Amplification/p53 pathway axis","pathway"),("MDM4","Amplification/p53 pathway axis","pathway"),("FGFR1","Mutation/fusion/amplification in selected gliomas","target"),("FGFR3","FGFR3-TACC3 fusion in a subset of IDH-wt glioma","target/fusion"),("NTRK1","Rare actionable fusion; fusion context must be verified","target/fusion"),("NTRK2","Rare actionable fusion; fusion context must be verified","target/fusion"),("NTRK3","Rare actionable fusion; fusion context must be verified","target/fusion"),("MET","Rearrangement/amplification in selected gliomas","target"),("MYB","MYB/MYBL1 alterations in pediatric low-grade glioma spectrum","pediatric"),("NOTCH1","Reported in oligodendroglioma molecular context","research")]
BASE='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
MANE='https://ftp.ncbi.nlm.nih.gov/refseq/MANE/MANE_human/release_1.5/MANE.GRCh38.v1.5.summary.txt.gz'
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'ProteinAnalytic academic prototype; NCBI E-utilities'})
 with urllib.request.urlopen(req,timeout=60) as r:return r.read()
def parse_records(s):
 out=[];head=None;seq=[]
 for l in s.splitlines():
  if l.startswith('>'):
   if head is not None:out.append((head,''.join(seq)))
   head=l[1:].strip();seq=[]
  elif head is not None:seq.append(l.strip())
 if head is not None:out.append((head,''.join(seq)))
 return out
def fasta_fetch(db,accs):
 if not accs:return []
 url=BASE+'efetch.fcgi?'+urllib.parse.urlencode({'db':db,'id':','.join(accs),'rettype':'fasta','retmode':'text'})
 return parse_records(get(url).decode())
def format_records(rows,db,acc_by_gene):
 out=[]
 for h,seq in rows:
  m=re.search(r'((?:NM|NR|NP|XP|YP)_\d+\.\d+)',h)
  acc=m.group(1) if m else ''
  gene=next((g for g,a in acc_by_gene.items() if acc in a),None)
  if not gene or not seq:continue
  label=f'{gene}|{acc} {h}'
  out.append((gene,acc,label,seq))
 return '\n'.join('>'+h+'\n'+'\n'.join(s[i:i+70] for i in range(0,len(s),70)) for _,_,h,s in out)+'\n',out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='data/glioma_reference_library');ap.add_argument('--max-mb',type=float,default=30);args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 print('Downloading MANE v1.5 summary…',flush=True);summary=gzip.decompress(get(MANE)).decode();lines=summary.splitlines();cols=lines[0].lstrip('#').split('\t');rows=[]
 for l in lines[1:]:
  f=l.split('\t')
  if len(f)<10:continue
  d=dict(zip(cols,f))
  if d.get('MANE_status')=='MANE Select':rows.append(d)
 index={r['symbol']:r for r in rows};selected=[]
 for sym,role,cat in PANEL:
  d=index.get(sym)
  if not d and sym=='H3-3A':d=index.get('H3F3A')
  selected.append({'symbol':sym,'role':role,'category':cat,'gene_id':d.get('NCBI_GeneID','') if d else '', 'refseq_rna':d.get('RefSeq_nuc','') if d else '', 'refseq_protein':d.get('RefSeq_prot','') if d else '', 'mane_status':d.get('MANE_status','') if d else 'not found'})
 rna_acc={x['symbol']:[x['refseq_rna']] for x in selected if x['refseq_rna']};prot_acc={x['symbol']:[x['refseq_protein']] for x in selected if x['refseq_protein']}
 print(f'Fetching {len(rna_acc)} RNA and {len(prot_acc)} protein RefSeq accessions…',flush=True)
 rna_raw=fasta_fetch('nuccore',[v[0] for v in rna_acc.values()]);prot_raw=fasta_fetch('protein',[v[0] for v in prot_acc.values()])
 rna_text,rna_records=format_records(rna_raw,'nuccore',rna_acc);prot_text,prot_records=format_records(prot_raw,'protein',prot_acc)
 by={x['symbol']:{'role':x['role'],'category':x['category'],'gene_id':x['gene_id'],'refseq_rna':x['refseq_rna'],'refseq_protein':x['refseq_protein'],'rna_length':0,'protein_length':0} for x in selected}
 for gene,acc,h,s in rna_records:by[gene]['rna_length']=len(s)
 for gene,acc,h,s in prot_records:by[gene]['protein_length']=len(s)
 manifest={'dataset':'ProteinAnalytic glioma research reference sequences','species':'Homo sapiens','assembly':'GRCh38; MANE Select v1.5; NCBI RefSeq','retrieved_utc':datetime.now(timezone.utc).isoformat(),'panel_size':len(PANEL),'records':[{'symbol':sym,**record} for sym,record in by.items()],'non_fasta_biomarkers':['1p/19q whole-arm codeletion','whole chromosome 7 gain / chromosome 10 loss','MGMT promoter methylation','TERT promoter variants','EGFR amplification','DNA methylation class'],'cautions':['Curated research panel, not a universal clinical panel.','Reference FASTAs are not patient tumor variants or neoantigens.','MANE Select is one representative transcript and may omit relevant isoforms.','TERT biomarker is promoter sequence/variant, not mRNA/protein FASTA.','MGMT predictive biomarker concerns promoter methylation; reference sequence does not provide methylation status.','Variants, fusions, copy number, expression and methylation require separate assay-specific data.','This bundle does not predict T-cell response, treatment benefit, or safety.']}
 bundle={'manifest':manifest,'fasta_rna':rna_text,'fasta_protein':prot_text}
 files={'glioma_panel_mane_rna.fasta':rna_text,'glioma_panel_mane_protein.fasta':prot_text,'glioma_panel_manifest.json':json.dumps(manifest,indent=2,ensure_ascii=False)+'\n','glioma_panel_library.json':json.dumps(bundle,separators=(',',':'),ensure_ascii=False)+'\n'}
 total=sum(len(v.encode()) for v in files.values())/(1024*1024)
 if total>args.max_mb:raise SystemExit(f'Aborting: output total {total:.2f} MB exceeds cap {args.max_mb} MB')
 for name,data in files.items():(out/name).write_text(data)
 print(json.dumps({'panel_genes':len(PANEL),'RNA_FASTA_records':len(rna_records),'protein_FASTA_records':len(prot_records),'combined_files_mb':round(total,3),'limit_mb':args.max_mb,'out':str(out)},indent=2))
if __name__=='__main__':main()
