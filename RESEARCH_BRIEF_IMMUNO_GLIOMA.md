# ProteinAnalytic — revisão de desenho para predição de antígenos tumorais em glioma

**Escopo.** Síntese de pesquisa e arquitetura para plataforma de pesquisa, não revisão sistemática, dispositivo clínico ou aconselhamento médico. Não me apresento como médico; a proposta segue princípios de evidência, validação e segurança de bioinformática translacional.

## Conclusão executiva

Uma plataforma robusta não deve afirmar que “ensina” um linfócito a reconhecer glioma a partir de uma sequência FASTA. A inferência real percorre uma cadeia de eventos: evento tumoral específico → transcrito/proteína expressos → processamento → apresentação por HLA → reconhecimento por TCR → resposta celular funcional → seletividade tumoral e segurança. Os preditores tratam subproblemas distintos. A ligação peptídeo-HLA, uma estrutura prevista ou expressão gênica isolada não provam imunogenicidade, morte tumoral, benefício clínico ou segurança.

A decisão de desenho recomendada para ProteinAnalytic é um **sistema de evidências por eixo**, com proveniência e incerteza, não um único “escore de afinidade” ou “probabilidade de cura”. O diferencial útil seria juntar evidência multiômica, antigen presentation machinery, peptidômica de HLA, seletividade frente a tecido normal e contexto de heterogeneidade de glioma, explicitando o que foi observado e o que foi previsto.

## Fluxo computacional recomendado

1. **Contextualizar amostra e diagnóstico:** WHO CNS / diagnóstico integrado, tecido primário versus recorrente, pureza tumoral, local/tempo da amostra, consentimento e controle de acesso.
2. **Encontrar eventos somáticos:** comparar DNA tumoral e normal para SNVs/indels, CNVs, rearranjos/fusões; usar RNA-seq para verificar expressão do alelo, fusão e splicing. Registrar VAF, cobertura, clonabilidade, qualidade e incerteza do caller.
3. **Tipar HLA:** determinar HLA-I (A/B/C) e, quando útil, HLA-II com método adequado ao tipo de dado. Registrar confiança, alelos perdidos e LOH. A apresentação depende também de HLA, B2M, TAP1/2, NLRC5 e estado celular/interferon.
4. **Construir proteoma específico da amostra:** usar transcritos e variantes confirmados, construir pares peptídicos mutante/wild type com anotação de isoforma e coordenadas. A referência MANE é um controle de referência, não uma sequência tumoral personalizada.
5. **Modelar processamento e apresentação separadamente:** peptídeos processáveis, ligação ao HLA, eluição/ligante e estabilidade pMHC são endpoints distintos. Ferramentas possíveis incluem NetMHCpan/IEDB, MHCflurry, MixMHCpred e pipelines como pVACtools; conferir versões, alelos, calibração e cobertura de treinamento.
6. **Adicionar evidência observada:** imunopeptidômica LC-MS/MS pode detectar ligantes realmente apresentados. Exigir controle de FDR, decoys, rastreabilidade de espectro e contexto do ensaio. Ausência em MS não prova ausência biológica.
7. **Priorizar seletividade:** cruzar tumor vs normal pareado, expressão bulk e quando possível single-cell/spatial, proteômica e ligandomas de tecidos normais; sinalizar expressão em tecidos normais essenciais e similaridade com peptídeo selvagem. Avaliar escape por subclonalidade, heterogeneidade espacial, perda de HLA e evolução após tratamento.
8. **Tratar reconhecimento T como eixo experimental:** preditores de TCR/imunogenicidade são incertos. Resultado computacional não demonstra que um TCR reconhecerá ou matará célula tumoral. Exigir ensaios funcionais apropriados e revisão institucional para translação.
9. **Avaliar relevância de glioma:** separar glioblastoma IDH-wildtype, astrocitoma IDH-mutante, oligodendroglioma, gliomas pediátricos H3-alterados e outros. Incluir microambiente imunossupressor, baixa/heterogênea apresentação, recorrência e acesso ao SNC.
10. **Validar e governar:** validação externa por centro e subtipo; evitar vazamento de paciente/peptídeo; medir calibração, sensibilidade, especificidade, PPV e utilidade; registrar versões e corrigir bases com auditoria.

## Ferramentas, usos e limites

| Camada | Ferramentas / recursos possíveis | O que a saída significa | Limite crítico |
|---|---|---|---|
| FASTA e anotação | NCBI RefSeq/MANE, Ensembl/GENCODE, UniProt, VEP | identidade e anotação de sequência/referência | FASTA não indica mutação, expressão ou apresentação |
| HLA typing | HLA-HD, OptiType (escolha depende do input) | hipótese de genótipo HLA com confiança | erro de typing afeta todas as etapas seguintes |
| HLA binding/elution | IEDB/NetMHCpan, MHCflurry, MixMHCpred | estimativa endpoint-específica | binding ≠ processamento, pMHC real ou imunogenicidade |
| Workflows neoantígenos | pVACtools, NeoDisc, ImmuneMirror (ver release e licença) | geração/filtro/priorização de candidatos | benchmark não garante generalização para glioma ou paciente |
| Ligandoma | imunoprecipitação HLA + LC-MS/MS; HLA Ligand Atlas como recurso de referência | evidência empírica de peptídeo apresentado | sensível a abundância, sensibilidade, amostra e FDR |
| Expressão/normalidade | GTEx, TCGA/GDC, CPTAC/PDC, GEO, CGGA, single-cell/spatial | expressão/proteína por contexto e população | batch, composição celular, coortes e diferenças tumor-normal |
| Evidência de alvo/terapia | CIViC, Open Targets, literatura, ensaios e recursos regulatórios | contexto de evidência/actionability | evidência preclínica não equivale a benefício clínico |

Ferramentas citadas são candidatas de integração e exigem revisão de licença, versão, termos, infraestrutura e dados permitidos antes de qualquer uso comercial ou clínico.

## Base FASTA criada nesta iteração

Foi obtido e filtrado o arquivo oficial MANE Select v1.5 de NCBI/RefSeq (GRCh38). O banco local contém **32 transcritos RefSeq MANE Select e 32 proteínas correspondentes**, em FASTAs separados, com cabeçalhos contendo símbolo e accession.version, além de manifesto JSON. Payload compilado: aproximadamente 0,5 MB; limite configurado para todos os arquivos do pacote: 30 MiB. A coleção reúne IDH1, IDH2, ATRX, TP53, CIC, FUBP1, TERT, EGFR, CDKN2A, CDKN2B, MGMT, H3-3A, ACVR1, PDGFRA, EZHIP, BRAF, NF1, PTEN, RB1, PIK3CA, PIK3R1, CDK4, MDM2, MDM4, FGFR1, FGFR3, NTRK1, NTRK2, NTRK3, MET, MYB e NOTCH1.

A seleção é um **painel de pesquisa de marcadores de subtipos diversos**, não os “32 oficiais” nem painel de teste clínico universal. MANE Select é um transcrito representativo; CDKN2A possui isoformas relevantes (p14ARF/p16INK4A); fusions e mutações necessitam sequências/junções específicas.

### Alterações relevantes que não são “um FASTA de gene”

- 1p/19q codeleção inteira, +7/−10 e amplificação de EGFR: alterações de cromossomos/cópia.
- Metilação do promotor MGMT e classificação por metilação: estados epigenéticos.
- TERT c.-124/c.-146: variantes de promotor; FASTA mRNA/proteína não contém a região regulatória.
- EGFRvIII, IDH1 R132, IDH2 R172, H3 K27/G34 e fusões: variantes específicas; referência MANE não as representa.
- Expressão ou abundância de proteína exige dados experimentais/ômicos, não é deduzida apenas da sequência de referência.

## Priorização de saída recomendada

Mostrar painel separado, sem média opaca:

- qualidade/proveniência da variante;
- expressão tumoral e fração clonal;
- expressão em tecido normal e exclusividade tumoral;
- HLA genotype/LOH/APM;
- predição de processamento e ligação/eluição;
- evidência observada por MS;
- evidência de T-cell functional assay;
- incerteza/calibração e dado ausente;
- evidência clínica versus pré-clínica.

Não converter os resultados em “% de afinidade terapêutica” ou “probabilidade de ataque” se o endpoint não foi medido e validado. pLDDT/PAE de estrutura também não são afinidade molecular.

## Arquivos da implementação

- `data/glioma_reference_library/glioma_panel_mane_rna.fasta`
- `data/glioma_reference_library/glioma_panel_mane_protein.fasta`
- `data/glioma_reference_library/glioma_panel_manifest.json`
- `data/glioma_reference_library/glioma_panel_library.json` (bundle FASTA + manifesto para importar na interface)
- `build_glioma_library.py` (reconstrói o painel consultando a versão NCBI MANE definida no script; saída limitada a 30 MiB)
- `immunotherapy_knowledge.json` (módulos, ferramentas, score policy, governança, referências)
- `immunotherapy_knowledge.js` (dados de interface e dimensões de evidência)
- `immunotherapy_pipeline.py` (valida FASTA, accession.version, alfabetos e cap; não prediz imunogenicidade)
- `ProteinAnalytic.html` (interface; importar o bundle JSON pela seção de painel para salvar as FASTAs no armazenamento local do navegador)

## Referências principais

1. [NeoDisc: A comprehensive proteogenomic pipeline for neoantigen discovery](https://www.nature.com/articles/s41587-024-02420-y) (Nature Biotechnology, 2024).
2. [Computational methods and data resources for predicting tumor neoantigens](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222050/) (2025 review).
3. [ESMO Precision Medicine Working Group recommendations](https://pmc.ncbi.nlm.nih.gov/articles/PMC7885309/) (neoantigen prediction and clinical benefit).
4. [IEDB Next-Generation T-cell tools](https://nextgen-tools.iedb.org/docs/tools/tcell/index.html).
5. [NCBI MANE project](https://www.ncbi.nlm.nih.gov/refseq/MANE/) and [MANE v1.5 release](https://ncbiinsights.ncbi.nlm.nih.gov/2026/03/10/mane-v1-5/).
6. [CAP/AANP/AMP/SNO guideline: molecular biomarker testing for diffuse gliomas](https://pmc.ncbi.nlm.nih.gov/articles/PMC9311267/).
7. [EANO guideline on molecular diagnostic tools in gliomas](https://academic.oup.com/neuro-oncology/article/25/10/1731/7189810).
8. [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) — use policies and rate limits apply.
