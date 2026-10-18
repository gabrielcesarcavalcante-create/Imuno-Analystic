/* ProteinAnalytic research knowledge module.
 * Reference workflow and evidence dimensions only. No receptor engineering or treatment advice.
 * Usage: const kb = window.PROTEINANALYTIC_IMMUNOLOGY;
 */
(function (root) {
  'use strict';
  const panel = [
    ['IDH1','classification','IDH hotspot; molecular class; variant required for tumor peptide'],
    ['IDH2','classification','IDH hotspot; molecular class; variant required for tumor peptide'],
    ['ATRX','classification','IDH-mutant astrocytoma context; chromatin remodeling'],
    ['TP53','classification','Astrocytoma and H3-altered contexts; evaluate exact somatic variant'],
    ['CIC','classification','Oligodendroglioma, IDH-mutant / 1p19q-codeleted context'],
    ['FUBP1','classification','Oligodendroglioma-associated recurrent alterations'],
    ['TERT','promoter biomarker','Promoter variants; transcript/protein FASTA does not capture promoter event'],
    ['EGFR','target/diagnostic','Amplification, mutation, EGFRvIII; variant and expression context matter'],
    ['CDKN2A','classification','Homozygous deletion in IDH-mutant astrocytoma; locus event, not just sequence'],
    ['CDKN2B','classification','Often co-deleted with CDKN2A; locus-level assay needed'],
    ['MGMT','epigenetic','Promoter methylation is distinct from gene coding sequence or RNA abundance'],
    ['H3-3A','histone','H3 K27/G34 variant contexts; confirm current HGNC/RefSeq nomenclature'],
    ['ACVR1','pediatric glioma','Alterations in a subset of diffuse midline gliomas'],
    ['PDGFRA','target','Amplification/alteration in selected glioma contexts'],
    ['EZHIP','pediatric glioma','Expression/alteration associated with H3 K27-altered contexts'],
    ['BRAF','target','V600E and fusion are distinct events; subtype matters'],
    ['NF1','pathway/predisposition','MAPK axis; inherited and somatic contexts must be separated'],
    ['PTEN','pathway','Tumor-suppressor loss; expression alone is not genotype'],
    ['RB1','pathway','Cell-cycle pathway alteration'],
    ['PIK3CA','pathway/target','PI3K pathway variants require exact variant interpretation'],
    ['PIK3R1','pathway','PI3K pathway alteration'],
    ['CDK4','target','Amplification/cell-cycle axis; copy number is not in a coding FASTA'],
    ['MDM2','pathway','Amplification/p53 pathway axis'],
    ['MDM4','pathway','Amplification/p53 pathway axis'],
    ['FGFR1','target','Alterations and fusions occur in selected glioma subtypes'],
    ['FGFR3','target/fusion','FGFR3::TACC3 fusion requires junction-level evidence'],
    ['NTRK1','target/fusion','Rare fusion; confirm in-frame junction and transcript expression'],
    ['NTRK2','target/fusion','Rare fusion; confirm in-frame junction and transcript expression'],
    ['NTRK3','target/fusion','Rare fusion; confirm in-frame junction and transcript expression'],
    ['MET','target','Rearrangement/amplification in selected glioma contexts'],
    ['MYB','pediatric glioma','MYB/MYBL1 rearrangements in selected low-grade glioma spectrum'],
    ['NOTCH1','research','Reported molecular context; clinical actionability not implied']
  ].map(([symbol, category, rationale]) => ({symbol, category, rationale}));

  const pipeline = [
    {id:'specimen', title:'Specimen / diagnosis', evidence:['integrated histomolecular diagnosis','primary/recurrent','tumor purity','consent/provenance']},
    {id:'variants', title:'Tumor-specific event calling', evidence:['paired tumor-normal DNA','RNA expression','SNV/indel','fusion/splice','VAF/clonality']},
    {id:'hla', title:'HLA and antigen-processing machinery', evidence:['HLA genotype and call confidence','HLA LOH/CNV','HLA-A/B/C and B2M','TAP1/2, NLRC5']},
    {id:'source', title:'Candidate source antigen', evidence:['mutant/wild-type peptide pair','source transcript expression','variant phasing','isoform provenance']},
    {id:'presentation', title:'Peptide processing / pMHC', evidence:['proteasomal cleavage','TAP transport','HLA binding','eluted-ligand prediction','complex stability']},
    {id:'direct', title:'Observed presentation', evidence:['HLA immunopeptidomics','spectral evidence','decoys and FDR','matched normal data']},
    {id:'selectivity', title:'Tumor selectivity', evidence:['normal-tissue RNA/protein','normal immunopeptidome','single-cell/spatial expression','wild-type cross-reactivity']},
    {id:'recognition', title:'T-cell response evidence', evidence:['TCR recognition is not reliably inferred from binding alone','assay-specific functional evidence','immune context and escape']},
    {id:'validation', title:'Validation / governance', evidence:['independent cohort','calibration and uncertainty','data/model version','expert review']}
  ];
  const tools = [
    {name:'pVACtools',domain:'variant-to-neoantigen workflow',note:'Open-source workflow; assess software release, predictor coverage and benchmark assumptions.'},
    {name:'IEDB / NetMHCpan',domain:'MHC binding and eluted-ligand prediction',note:'Binding, processing and elution are separate endpoints; not a T-cell killing score.'},
    {name:'MHCflurry',domain:'HLA-I affinity/presentation',note:'Inspect allele coverage, release and calibration before comparing outputs.'},
    {name:'NeoDisc',domain:'integrated proteogenomic antigen prioritization',note:'Published end-to-end approach incorporating genomics, transcriptomics and immunopeptidomics.'},
    {name:'HLA-HD / OptiType',domain:'HLA typing',note:'Choice depends on input assay; retain caller confidence and validation.'},
    {name:'LC-MS/MS immunopeptidomics',domain:'direct natural ligand evidence',note:'Detection is empirical evidence; absence of detection is not proof of absent presentation.'}
  ];
  const scoring = {
    axes:['variant evidence','tumor expression','clonality','HLA genotype/LOH','processing/presentation','MS ligand evidence','normal tissue selectivity','T-cell functional evidence','clinical evidence'],
    policy:'Never collapse unlike endpoints into a single unvalidated probability or “affinity %”. Display evidence type, source, version, uncertainty and missingness separately.',
    doNotInfer:['HLA binding implies immunogenicity','structure confidence implies affinity','reference FASTA represents tumor variants','predicted peptide means naturally presented','immune recognition means safe tumor killing']
  };
  root.PROTEINANALYTIC_IMMUNOLOGY = Object.freeze({version:'1.0.0',panel,pipeline,tools,scoring,storageCapBytes:30*1024*1024});
})(typeof window !== 'undefined' ? window : globalThis);
