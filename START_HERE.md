# START HERE (no bioinformatics experience needed)

---

> ## 🔴 USE MINICONDA — REQUIRED
>
> **Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) first.**  
> CUT&RUN needs Bowtie2, samtools, SEACR, etc.  
> **Pip alone will not work.** Use conda or you will hit missing-program errors.

---

## What this does (plain English)

CUT&RUN maps where a protein binds DNA in the genome.  
This pipeline:

1. Checks read quality  
2. Trims reads  
3. Aligns to the genome (Bowtie2, dovetail-aware)  
4. Calls peaks (SEACR, optional MACS2)  
5. Makes coverage tracks and QC plots  

---

## Step 1 — Miniconda

https://docs.conda.io/en/latest/miniconda.html  
Install → open a **new** terminal.

---

## Step 2 — Code

```bash
git clone https://github.com/gigi777mo/cutandrun-pipeline.git
cd cutandrun-pipeline
```

---

## Step 3 — Environment (one time)

```bash
conda env create -f environment.yml
conda activate cutandrun
```

---

## Step 4 — Your data

1. Paired-end FASTQs in `data/raw/`  
2. Copy `data/samples.csv.example` → `data/samples.csv` and fill sample names + IgG control column  
3. Edit `config/config.yaml`: set **genome Bowtie2 index** path (ask lab for this)  

---

## Step 5 — Run

```bash
conda activate cutandrun
snakemake --cores 4 --use-conda
```

Or step-by-step scripts in the README if you prefer smaller runs.

---

## Step 6 — Results

Under `results/`: BAMs, peaks (SEACR/MACS2), bigWigs, MultiQC report.

---

## If it fails

| Problem | Fix |
|---------|-----|
| `conda not found` | Install Miniconda; new terminal |
| `bowtie2: not found` | You are not in `conda activate cutandrun` |
| Index missing | Set correct `bowtie2_index` in config |
| Single-end data | This pipeline expects **paired-end** |

Citations: [docs/CITATIONS.md](docs/CITATIONS.md)
