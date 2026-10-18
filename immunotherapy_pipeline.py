#!/usr/bin/env python3
"""Offline integrity/QC utilities for ProteinAnalytic research FASTA bundles.

This utility validates reference records and provenance only. It does NOT call epitopes,
model HLA/TCR binding, design immune receptors, or recommend patient treatment.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
MAX_BYTES=30*1024*1024
AA=set('ACDEFGHIKLMNPQRSTVWYBXZJUO*')
NT=set('ACGTUNRYKMSWBDHV')
def read_fasta(path):
 rec=[]; header=None;seq=[]
 for line in Path(path).read_text().splitlines():
  if line.startswith('>'):
   if header is not None:rec.append((header,''.join(seq)))
   header=line[1:].strip();seq=[]
  elif line.strip():
   if header is None:raise ValueError(f'{path}: sequence before FASTA header')
   seq.append(re.sub(r'\s+','',line).upper())
 if header is not None:rec.append((header,''.join(seq)))
 return rec
def validate(directory):
 d=Path(directory); files=[d/'glioma_panel_mane_rna.fasta',d/'glioma_panel_mane_protein.fasta',d/'glioma_panel_manifest.json',d/'glioma_panel_library.json']
 absent=[str(f) for f in files if not f.exists()]
 if absent:raise FileNotFoundError('Missing: '+', '.join(absent))
 total=sum(f.stat().st_size for f in files)
 if total>MAX_BYTES:raise ValueError(f'Files take {total/1048576:.2f} MiB; max is 30 MiB')
 manifest=json.loads(files[2].read_text());out=[]
 for f,typ,alphabet in [(files[0],'RNA/DNA',NT),(files[1],'protein',AA)]:
  records=read_fasta(f); seen=set()
  for h,s in records:
   if not s:out.append({'file':f.name,'header':h,'issue':'empty sequence'});continue
   acc=re.search(r'\b(?:NM|NR|NP|XP)_\d+\.\d+\b',h)
   if not acc:out.append({'file':f.name,'header':h,'issue':'no versioned RefSeq accession in header'})
   if h in seen:out.append({'file':f.name,'header':h,'issue':'duplicate FASTA header'})
   seen.add(h)
   bad=set(s)-alphabet
   if bad:out.append({'file':f.name,'header':h,'issue':'unexpected symbols '+''.join(sorted(bad))})
 symbols={r['symbol'] for r in manifest['records']}; headers=(read_fasta(files[0])+read_fasta(files[1]))
 represented={h.split('|')[0] for h,_ in headers}
 missing=sorted(symbols-represented)
 return {'valid':not out,'manifest_genes':len(symbols),'rna_records':len(read_fasta(files[0])),'protein_records':len(read_fasta(files[1])),'bytes_all_deliverables':total,'max_bytes':MAX_BYTES,'missing_genes_in_any_fasta':missing,'issues':out,'retrieved_utc':manifest.get('retrieved_utc'),'reference':manifest.get('assembly')}
def main():
 p=argparse.ArgumentParser();p.add_argument('directory',nargs='?',default='data/glioma_reference_library');a=p.parse_args()
 result=validate(a.directory);print(json.dumps(result,indent=2,ensure_ascii=False));sys.exit(0 if result['valid'] else 1)
if __name__=='__main__':main()
