#!/usr/bin/env python3
"""FastQC + MultiQC for CUT&RUN."""

import argparse
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="results/qc")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()

    indir = Path(args.input)
    outdir = Path(args.out) / "raw"
    outdir.mkdir(parents=True, exist_ok=True)

    fastqs = list(indir.glob("*.fastq.gz")) + list(indir.glob("*.fq.gz"))
    if not fastqs:
        raise SystemExit(f"No FASTQs in {indir}")

    print(f"[+] FastQC on {len(fastqs)} files")
    subprocess.run(["fastqc", "-t", str(args.threads), "-o", str(outdir)] + [str(f) for f in fastqs], check=True)
    subprocess.run(["multiqc", str(outdir), "-o", str(args.out), "--force"], check=True)
    print(f"[+] MultiQC → {args.out}/multiqc_report.html")

if __name__ == "__main__":
    main()
