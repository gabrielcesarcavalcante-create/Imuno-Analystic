---
title: 'ImunoAnalyst: a browser-based research workbench for glioma biomarker context, immune-recognition hypotheses, and molecular exploration'
authors:
  - name: Gabriel César
    affiliation: 1
affiliations:
  - name: '[Institution or independent-researcher affiliation to confirm], Brazil'
    index: 1
date: 23 October 2026
tags:
  - glioma
  - neuro-oncology
  - immunology
  - molecular visualization
  - cheminformatics
  - research software
bibliography: paper.bib
---

# Summary

ImunoAnalyst is a browser-based research and educational workbench for exploring molecular contexts in glioma. It combines a curated 32-gene panel with reference nucleotide and protein sequences, predicted protein-structure views, a library of 20 glioma profiles, and an explicitly hypothetical immune-response simulation. A separate medicinal-chemistry module accepts SMILES strings and can calculate molecular descriptors when the optional RDKit engine is installed; an optional local bridge can run AutoDock Vina for researcher-prepared PDBQT files. The application is designed to make assumptions, data provenance, and limits visible while moving between these views.

The software distinguishes diagnostic or subtype-associated biomarkers from candidate immune targets. A biomarker does not, by itself, establish protein expression, peptide processing, HLA presentation, or recognition by a T-cell receptor or chimeric antigen receptor. The immune laboratory uses a synthetic, dimensionless ordinary differential equation and a schematic animation to illustrate user-defined scenarios; it is not fitted to patient or experimental data. Likewise, small-molecule descriptors and docking poses are computational outputs, not evidence of biological activity, safety, or therapeutic benefit. ImunoAnalyst is not a diagnostic, target-selection, or treatment-recommendation system.

# Statement of need

Glioma research requires interpretation across histological and molecular entities, sequence variation, expression, antigen processing, structural models, and experimental evidence. These concepts are often displayed in separate resources, which can make it difficult for students and early-stage researchers to keep the evidential steps distinct. The 2021 World Health Organization classification emphasizes integrated molecular and histopathological diagnosis rather than a universal gene checklist [@louis2021who]. Proteogenomic pipelines such as NeoDisc combine tumor-specific genomic, transcriptomic, and immunopeptidomic evidence to prioritize antigen hypotheses [@huber2025neodisc]; ImunoAnalyst does not perform those analyses. In parallel, predicted structures and reference sequences provide useful context but do not establish tumor-specific alterations or immune recognition [@varadi2022alphafold].

ImunoAnalyst is intended for neuropathology, neuro-oncology, immunology, and computational-biology researchers who need a transparent interface for exploratory work and teaching. Its profiles summarize context-level associations and candidate-target hypotheses; they are not patient calls. The application surfaces warnings where a promoter methylation event, copy-number change, fusion, or tumor variant cannot be inferred from a canonical reference FASTA. The interactive immune model gives users a way to inspect how their selected synthetic assumptions affect trajectories, while explicitly separating that exercise from clinical prediction.

A second, optional workbench provides a lightweight entry point to cheminformatics. This is scientifically distinct from the immune-cell simulation: SMILES descriptors and structure-based docking address small-molecule hypotheses, not T-cell or CAR recognition. By putting these exploratory workflows behind explicit limitations and keeping the engines optional, the application aims to support transparent hypothesis formulation without implying that the components constitute a validated discovery pipeline.

# State of the field

Established resources and specialist packages address parts of this workflow. The AlphaFold Protein Structure Database supplies predicted structures and confidence metadata [@varadi2022alphafold]; RDKit provides cheminformatics algorithms and molecular descriptors [@rdkit]; and AutoDock Vina supplies an open-source molecular-docking engine [@eberhardt2021vina]. Commercial systems such as BioSolveIT SeeSAR and BIOVIA Discovery Studio provide broader ligand-design, scoring, docking, pharmacophore, and simulation capabilities; AIDDISON integrates generative design and drug-discovery workflows [@biosolveit2026; @biovia2026; @rusinko2024aiddison]. ImunoAnalyst does not implement or reproduce proprietary algorithms such as HYDE, CDOCKER, GOLD, CHARMm, or AIDDISON's generative models, and its optional Vina adapter is not a substitute for those systems.

The contribution is instead an integrated, caveat-forward interface linking glioma molecular context, reference-sequence/structure exploration, candidate immune-recognition concepts, a reproducible toy-model scenario, and optional open cheminformatics engines. The build-versus-contribute choice is deliberate: ImunoAnalyst does not attempt to replace specialist predictors or clinical classification workflows. It provides a reusable teaching and hypothesis-tracking layer in which biomarker association, candidate antigen status, and computed outputs remain separate. Its scholarly value therefore depends on reuse, external evaluation, and contribution beyond the current prototype; those forms of impact have not yet been demonstrated.

# Software design

The core interface is implemented in HTML, CSS, and JavaScript and can be served as a static web application. Molecular-panel records, glioma profiles, structural coordinates, and educational knowledge are kept in separate local JavaScript data modules, allowing the interface and curated content to be revised independently. The structural view presents predicted reference-protein models and local-confidence annotations; it does not represent a tumor variant or an experimentally solved immune complex.

The immune laboratory combines adjustable scenario inputs with a deterministic ODE simulation. Users choose a glioma profile, one or more candidate targets, assumed coverage values, tumor and effector cell counts, model parameters, a virtual time window, and a relative threshold. A staged animation shows patrol, approach, assumed contact/recognition, and an illustrative attack. The animation is a visualization of the model assumptions, not a cell-level or molecular simulation. Scenario settings can be exported and re-imported as JSON to support reproducibility of the user-defined inputs.

The medicinal-chemistry workbench is modular and opt-in. A small Node.js bridge can call a locally installed RDKit Python package for descriptors and AutoDock Vina for docking, recording engine versions, parameters, and input hashes when a docking job completes. Docking requires receptor and ligand PDBQT files prepared outside the application; the atlas C-alpha models are not docking-ready. No molecular-dynamics engine, pharmacophore-search engine, generative model, or validated ADMET model is bundled. If the optional engines are absent, the interface reports that they are unavailable rather than fabricating results. This separation keeps the browser application usable for education while making computational dependencies explicit.

# Research impact statement

At the time of this draft, no peer-reviewed studies, independent adopters, external integrations, benchmark comparisons, or public release history for ImunoAnalyst have been documented. The current software bundle is a research prototype, not evidence of clinical utility or validated predictive performance. Its near-term research contribution is a reusable interface for demonstrating the separation between molecular biomarkers and immune-recognition evidence, and for recording user-defined simulation assumptions. Public source hosting, an OSI-approved license, automated or documented objective tests, versioned releases, and external evaluation are prerequisites for assessing broader impact and should be established before a JOSS submission.

# Availability

A web demonstration is linked from the project page at [Gliobio HealthScience](https://gliobio.healthscience.workers.dev/). This page is not a versioned source-code archive. A public source-repository URL and an OSI-approved license must be supplied before submission; neither is yet available in the current workspace. A versioned archive DOI should be added for the reviewed release during the post-review archiving step described by JOSS.

# AI usage disclosure

Arena.ai Agent Mode assisted with software implementation and refactoring, manual code validation, documentation, and drafting and editing this manuscript. The exact underlying model name and version were not exposed in the author-facing environment. The human author must review and verify the code, curated biomedical content, citations, and all claims; the author remains responsible for the final scientific interpretation and submission. Before submission, the author should add any available tool/version details and confirm that this disclosure accurately reflects the full development history.

# Acknowledgements

[Author: confirm and name any financial support, institutional resources, data providers, and contributors. If there was no external funding, state that explicitly.]

# References
