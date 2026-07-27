# Install notes (CUT&RUN pipeline)

## Python + pip (from GitHub)

```bash
git clone https://github.com/gigi777mo/cutandrun-pipeline.git
cd cutandrun-pipeline

python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Aligners / peak callers (not pure pip)

Need **Bowtie2**, **samtools**, **SEACR**, optional **MACS2**, **Trim Galore**/fastp, **deepTools**.

**Recommended:**

```bash
conda env create -f environment.yml
conda activate cutandrun
```

Use pip only for the Python helper scripts if tools are already on PATH.
