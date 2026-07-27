# CUT&RUN Analysis Pipeline

---

> ## 🔴 USE MINICONDA — REQUIRED
>
> **Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) first.**  
> `conda env create -f environment.yml` → `conda activate cutandrun`  
> **Do not use pip-only** — aligners and SEACR need conda/bioconda.

---

**New user?** Open **[START_HERE.md](START_HERE.md)**.

CUT&RUN (and CUT&Tag-compatible) analysis following SEACR / Henikoff / nf-core-style practices.

```bash
conda env create -f environment.yml
conda activate cutandrun
snakemake --cores 4 --use-conda
```

Citations: [docs/CITATIONS.md](docs/CITATIONS.md)

## License

MIT
