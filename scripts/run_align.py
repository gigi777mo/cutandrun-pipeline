#!/usr/bin/env python3
"""Align paired-end CUT&RUN reads with Bowtie2 --dovetail and filter."""

import argparse
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="CUT&RUN Bowtie2 alignment + filter")
    parser.add_argument("--input", required=True, help="Directory with trimmed FASTQs")
    parser.add_argument("--index", required=True, help="Bowtie2 index prefix")
    parser.add_argument("--out", default="results/bam")
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--mapq", type=int, default=20)
    parser.add_argument("--mito", default="chrM")
    parser.add_argument("--no-dovetail", action="store_true")
    args = parser.parse_args()

    indir = Path(args.input)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    r1_files = sorted(indir.glob("*_R1*.fastq.gz"))
    for r1 in r1_files:
        name = r1.name.replace("_R1.fastq.gz", "").replace("_R1_val_1.fq.gz", "")
        r2 = indir / f"{name}_R2.fastq.gz"
        if not r2.exists():
            r2 = indir / f"{name}_R2_val_2.fq.gz"
        if not r2.exists():
            print(f"[!] Missing R2 for {name}")
            continue

        raw_bam = outdir / f"{name}.raw.bam"
        filt_bam = outdir / f"{name}.filtered.bam"
        log = outdir / f"{name}.bowtie2.log"

        dovetail = [] if args.no_dovetail else ["--dovetail"]
        print(f"[+] Aligning {name} (dovetail={'on' if dovetail else 'off'})...")

        cmd_align = [
            "bowtie2", "-p", str(args.threads), "-x", args.index,
            "-1", str(r1), "-2", str(r2),
            "--local", "--very-sensitive-local",
            "--no-unal", "--no-mixed", "--no-discordant",
            "-I", "10", "-X", "700",
        ] + dovetail

        with open(log, "w") as lf:
            p1 = subprocess.Popen(cmd_align, stdout=subprocess.PIPE, stderr=lf)
            p2 = subprocess.Popen(["samtools", "view", "-bS", "-"], stdin=p1.stdout, stdout=subprocess.PIPE)
            subprocess.run(["samtools", "sort", "-@", str(args.threads), "-o", str(raw_bam)],
                           stdin=p2.stdout, check=True)
            p1.wait()
        subprocess.run(["samtools", "index", str(raw_bam)], check=True)

        # Filter: proper pair, MAPQ, exclude mito
        print(f"[+] Filtering {name}...")
        # Keep autosomes + chrX/Y; drop mito
        subprocess.run(
            f"samtools view -@ {args.threads} -b -q {args.mapq} -F 1804 -f 2 {raw_bam} | "
            f"samtools sort -@ {args.threads} -o {filt_bam}",
            shell=True, check=True
        )
        subprocess.run(["samtools", "index", str(filt_bam)], check=True)
        print(f"    → {filt_bam}")

    print("[+] Alignment complete")

if __name__ == "__main__":
    main()
