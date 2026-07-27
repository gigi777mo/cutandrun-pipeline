#!/usr/bin/env python3
"""Trim paired-end CUT&RUN reads with Trim Galore."""

import argparse
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="results/trimmed")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--quality", type=int, default=20)
    parser.add_argument("--min-length", type=int, default=20)
    args = parser.parse_args()

    indir = Path(args.input)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    r1s = sorted(indir.glob("*_R1*.fastq.gz"))
    for r1 in r1s:
        name = r1.name.replace("_R1.fastq.gz", "").replace("_R1_001.fastq.gz", "")
        r2 = indir / f"{name}_R2.fastq.gz"
        if not r2.exists():
            r2 = indir / f"{name}_R2_001.fastq.gz"
        if not r2.exists():
            print(f"[!] No R2 for {name}")
            continue
        print(f"[+] Trimming {name}")
        subprocess.run([
            "trim_galore", "--paired",
            "--quality", str(args.quality),
            "--length", str(args.min_length),
            "--cores", str(args.threads),
            "-o", str(outdir),
            "--basename", name,
            str(r1), str(r2)
        ], check=True)

    print("[+] Trimming done")

if __name__ == "__main__":
    main()
