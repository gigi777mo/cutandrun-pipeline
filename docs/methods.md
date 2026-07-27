# Methods & Literature Basis

This pipeline follows the consensus workflow used in published CUT&RUN analyses and community standards.

## Core references

1. **Skene & Henikoff (2017)** eLife — Original CUT&RUN method.
2. **Meers, Tenenbaum & Henikoff (2019)** Epigenetics & Chromatin — **SEACR** peak caller designed for low-background CUT&RUN.
3. **nf-core/cutandrun** (Hodgetts et al., JOSS 2026) — Community best-practice Nextflow pipeline; primary structural reference for this repo.
4. **4DN CUT&RUN pipeline** — Trimmomatic/Bowtie2 `--dovetail` / SEACR.
5. **CUT&RUNTools** (Zhu et al., Genome Biology 2019) — Emphasized dovetail alignment and short-fragment handling.

## Why these settings?

| Choice | Reason |
|--------|--------|
| Bowtie2 `--dovetail` | CUT&RUN PE reads frequently dovetail; treating them as concordant recovers true fragments (Henikoff, 4DN, nf-core). |
| SEACR as default | Optimized for sparse signal and low background typical of CUT&RUN; outperforms generic callers on these data. |
| MACS2 as secondary | Orthogonal validation; useful for histone marks or comparison with ChIP-seq literature. |
| IgG controls | SEACR uses control bedGraphs for empirical thresholds; strongly recommended. |
| Spike-in (E. coli) | Residual DNA from pA-MNase prep provides a natural calibrator; also supported via exogenous spike-ins. |
| Fragment size awareness | TF-focused analyses often retain ≤120 bp fragments; nucleosome-scale signals are larger. |
| Paired-end only | Single-end sacrifices fragment-length information and resolution. |

## Recommended experimental controls

- IgG or non-specific antibody control (same cell number / digestion conditions)
- Biological replicates (≥2)
- Optional: exogenous spike-in DNA or reliance on residual E. coli DNA for normalization

## QC checkpoints before interpretation

1. Fragment size distribution (deepTools bamPEFragmentSize) — should match expected TF vs nucleosome profile.
2. FRiP (fraction of reads in peaks).
3. Replicate concordance (IDR or simple overlap).
4. Spike-in alignment rate (if used).
5. MultiQC summary (alignment rate, duplication, mito content).
