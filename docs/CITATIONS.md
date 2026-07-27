# Citations — CUT&RUN Pipeline

Please cite the methods and tools you use. Core references for this pipeline:

## Method & peak calling

- **CUT&RUN method**  
  Skene PJ, Henikoff S.  
  *An efficient targeted nuclease strategy for high-resolution mapping of DNA binding sites.*  
  eLife. 2017;6:e21856.  
  https://doi.org/10.7554/eLife.21856

- **SEACR**  
  Meers MP, Tenenbaum D, Henikoff S.  
  *Peak calling by sparse enrichment analysis for CUT&RUN chromatin profiling.*  
  Epigenetics & Chromatin. 2019;12:42.  
  https://doi.org/10.1186/s13072-019-0287-4

- **MACS2**  
  Zhang Y, Liu T, Meyer CA, et al.  
  *Model-based analysis of ChIP-Seq (MACS).*  
  Genome Biology. 2008;9:R137.  
  https://doi.org/10.1186/gb-2008-9-9-r137

## Alignment & processing

- **Bowtie 2**  
  Langmead B, Salzberg SL.  
  *Fast gapped-read alignment with Bowtie 2.*  
  Nature Methods. 2012;9:357–359.  
  https://doi.org/10.1038/nmeth.1923

- **SAMtools**  
  Li H, et al. *The Sequence Alignment/Map format and SAMtools.* Bioinformatics. 2009.

- **bedtools**  
  Quinlan AR, Hall IM. *BEDTools: a flexible suite of utilities for comparing genomic features.* Bioinformatics. 2010.

- **Picard**  
  Broad Institute. *Picard Toolkit.* http://broadinstitute.github.io/picard/

## Community / reference pipelines

- **nf-core/cutandrun**  
  Hodgetts TL, et al.  
  *nf-core/cutandrun: A Nextflow pipeline for the analysis of CUT&RUN, CUT&Tag and TIP-seq datasets.*  
  Journal of Open Source Software. 2026;11(119):9672.  
  https://doi.org/10.21105/joss.09672

- **CUT&RUNTools**  
  Zhu Q, et al.  
  *CUT&RUNTools: a flexible pipeline for CUT&RUN processing and footprint analysis.*  
  Genome Biology. 2019;20:192.  
  https://doi.org/10.1186/s13059-019-1802-4

- **4DN CUT&RUN processing pipeline**  
  4D Nucleome Data Portal. https://data.4dnucleome.org/resources/data-analysis/cut-and-run-pipeline

## QC & visualization

- **Trim Galore!** — Krueger F. Babraham Bioinformatics.  
- **FastQC** — Andrews S. Babraham Bioinformatics.  
- **MultiQC** — Ewels P, et al. Bioinformatics. 2016.  
- **deepTools** — Ramírez F, et al. Nucleic Acids Research. 2016.

## Suggested acknowledgment

> CUT&RUN data were processed following community best practices (nf-core/cutandrun; Henikoff lab recommendations), with alignment using Bowtie 2 (Langmead & Salzberg, 2012) with dovetail-aware settings, and peak calling primarily with SEACR (Meers et al., 2019), with MACS2 (Zhang et al., 2008) as an optional orthogonal caller.
