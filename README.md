# CUT&RUN Analysis Pipeline

**Reproducible bulk CUT&RUN (and CUT&Tag-compatible) pipeline** following published best practices.

Based on standards from:
- **nf-core/cutandrun** (community best-practice Nextflow pipeline)
- **Henikoff lab / SEACR** (Meers et al., Epigenetics & Chromatin 2019)
- **4DN CUT&RUN processing pipeline**
- **CUT&RUNTools** principles (dovetail alignment, short-fragment handling)

---

## Pipeline Overview

```
1. QC                  FastQC → MultiQC
2. Trimming            Trim Galore! (or fastp) – critical for short fragments
3. Alignment           Bowtie2 with --dovetail (required for CUT&RUN PE overlaps)
4. Filtering           MAPQ filter, mitochondrial removal, optional duplicate marking
5. Spike-in (optional) Align to E. coli (or custom) for calibration
6. Coverage            bedGraph → bigWig (spike-in or CPM normalized)
7. Peak calling        SEACR (default, low-background) + MACS2 (optional)
8. Controls            IgG / non-specific antibody support
9. QC metrics          Fragment size distribution, FRiP, library complexity
10. Downstream         Consensus peaks, heatmaps (deepTools), MultiQC report
```

**Paired-end only** (single-end is not recommended for CUT&RUN resolution).

---

## Quick Start

```bash
git clone https://github.com/gigi777mo/cutandrun-pipeline.git
cd cutandrun-pipeline

conda env create -f environment.yml
conda activate cutandrun

# Edit config/config.yaml and data/samples.csv
# Place paired-end FASTQs in data/raw/

snakemake --cores 8 --use-conda
```

Or step-by-step:

```bash
python scripts/run_qc.py --input data/raw --out results/qc
python scripts/run_trim.py --input data/raw --out results/trimmed
python scripts/run_align.py --input results/trimmed --index /path/to/bowtie2_index --out results/bam
python scripts/run_peaks.py --bam results/bam --out results/peaks --method seacr
```

---

## Key Design Choices (Literature-Based)

| Step | Tool / Setting | Rationale |
|------|----------------|-----------|
| Aligner | **Bowtie2 `--dovetail`** | CUT&RUN fragments often have overlapping/dovetailing mates; required by Henikoff & 4DN pipelines |
| Peak caller (default) | **SEACR** | Designed for sparse, low-background CUT&RUN data (Meers et al. 2019) |
| Secondary peak caller | MACS2 | Widely used; good for comparison / broader peaks |
| Spike-in | E. coli residual DNA or exogenous | Natural calibrator from pA-MNase prep; supported in nf-core & Henikoff workflows |
| Controls | IgG | Used by SEACR for empirical thresholding |
| Fragment filter | Optional size selection (e.g. ≤120 bp for TF-focused) | Common in TF CUT&RUN to enrich local footprints |

---

## Configuration (`config/config.yaml`)

```yaml
genome: hg38
bowtie2_index: "/path/to/hg38"
spikein_index: "/path/to/ecoli"   # optional
blacklist: "/path/to/blacklist.bed"

align:
  dovetail: true
  min_mapq: 20
  remove_mito: true
  mark_duplicates: true

peaks:
  primary: seacr              # seacr | macs2
  seacr_mode: stringent       # stringent | relaxed
  seacr_norm: norm            # norm | non
  macs2_qvalue: 0.01
  use_igg_control: true

normalization:
  mode: spikein              # spikein | cpm | none
```

---

## Sample Sheet (`data/samples.csv`)

```csv
sample,condition,replicate,control,antibody
H3K27ac_rep1,treated,1,IgG_rep1,H3K27ac
H3K27ac_rep2,treated,2,IgG_rep1,H3K27ac
IgG_rep1,control,1,,IgG
```

- `control` column points to the IgG (or other) control sample name used for peak calling.
- Leave blank if no control.

---

## Outputs

```
results/
├── qc/
│   └── multiqc_report.html
├── trimmed/
├── bam/                     # filtered, sorted BAMs + indexes
├── coverage/
│   ├── *.bedgraph
│   └── *.bw                 # bigWig tracks
├── peaks/
│   ├── seacr/
│   └── macs2/
├── plots/
│   ├── fragment_sizes.pdf
│   └── peak_heatmaps/
└── logs/
```

---

## Spike-in Normalization

CUT&RUN often carries residual *E. coli* DNA from the pA-MNase preparation, which can serve as a natural spike-in.

1. Provide a Bowtie2 index for the spike-in genome (`spikein_index`).
2. Pipeline aligns reads to both target and spike-in genomes.
3. Scale factors are derived from spike-in read counts and applied to bedGraph/bigWig generation.

Alternatively use exogenous yeast/fly spike-in DNA if added experimentally.

---

## Peak Calling Notes

**SEACR** (default)
- Input: bedGraph (zero-signal regions omitted)
- Modes: `stringent` (higher specificity) or `relaxed`
- With IgG: `norm` mode recommended unless already spike-in normalized

**MACS2**
- Useful as orthogonal caller
- Prefer narrow peaks for TFs; broad for histone marks
- q-value default 0.01 (stricter than typical ChIP-seq)

Always inspect fragment-size distributions and FRiP before interpreting peaks.

---

## Requirements

- Paired-end FASTQ
- Bowtie2 index for target genome
- Optional: spike-in index, blacklist BED, IgG controls

---

## Citation

If you use this pipeline, please cite the underlying methods:

- **SEACR** — Meers MP, Tenenbaum D, Henikoff S. *Peak calling by sparse enrichment analysis for CUT&RUN chromatin profiling.* Epigenetics & Chromatin. 2019.
- **CUT&RUN method** — Skene PJ, Henikoff S. *An efficient targeted nuclease strategy for high-resolution mapping of DNA binding sites.* eLife. 2017.
- **nf-core/cutandrun** — Hodgetts et al., JOSS 2026 (community reference workflow).
- Bowtie2, MACS2, deepTools, Trim Galore!, Picard, SAMtools, bedtools — see respective papers.

---

## License

MIT
