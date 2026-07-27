#!/usr/bin/env python3
"""Peak calling for CUT&RUN with SEACR and/or MACS2."""

import argparse
import subprocess
from pathlib import Path

def bam_to_bedgraph(bam, bedgraph):
    subprocess.run(
        f"bedtools genomecov -bg -ibam {bam} | sort -k1,1 -k2,2n > {bedgraph}",
        shell=True, check=True
    )

def run_seacr(target_bg, out_prefix, control_bg=None, mode="stringent", norm="norm"):
    """Call SEACR. Requires SEACR_1.3.sh (or SEACR.sh) in PATH."""
    seacr = "SEACR_1.3.sh"
    # Try common names
    for candidate in ["SEACR_1.3.sh", "SEACR.sh", "seacr"]: 
        if subprocess.run(["which", candidate], capture_output=True).returncode == 0:
            seacr = candidate
            break

    out_dir = Path(out_prefix).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    if control_bg:
        cmd = ["bash", seacr, str(target_bg), str(control_bg), norm, mode, str(out_prefix)]
    else:
        # Numeric threshold (top 1% by default when no control)
        cmd = ["bash", seacr, str(target_bg), "0.01", norm, mode, str(out_prefix)]

    print("[+] SEACR:", " ".join(cmd))
    subprocess.run(cmd, check=False)

def run_macs2(bam, out_dir, name, control_bam=None, qvalue=0.01, broad=False):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "macs2", "callpeak",
        "-t", str(bam),
        "-f", "BAMPE",
        "-g", "hs",
        "-n", name,
        "--outdir", str(out_dir),
        "-q", str(qvalue),
    ]
    if control_bam:
        cmd += ["-c", str(control_bam)]
    if broad:
        cmd += ["--broad"]
    print("[+] MACS2:", " ".join(cmd))
    subprocess.run(cmd, check=False)

def main():
    parser = argparse.ArgumentParser(description="CUT&RUN peak calling (SEACR / MACS2)")
    parser.add_argument("--bam", required=True, help="Directory of filtered BAMs or single BAM")
    parser.add_argument("--out", default="results/peaks")
    parser.add_argument("--method", default="seacr", choices=["seacr", "macs2", "both"])
    parser.add_argument("--control", default=None, help="Control BAM or bedGraph (IgG)")
    parser.add_argument("--seacr-mode", default="stringent")
    parser.add_argument("--macs-qvalue", type=float, default=0.01)
    args = parser.parse_args()

    bam_path = Path(args.bam)
    bams = [bam_path] if bam_path.is_file() else sorted(bam_path.glob("*.filtered.bam"))
    if not bams:
        bams = sorted(Path(args.bam).glob("*.bam"))

    for bam in bams:
        name = bam.stem.replace(".filtered", "").replace(".raw", "")
        print(f"\n=== {name} ===")

        if args.method in ("seacr", "both"):
            bg = Path(args.out) / "bedgraph" / f"{name}.bedgraph"
            bg.parent.mkdir(parents=True, exist_ok=True)
            if not bg.exists():
                bam_to_bedgraph(bam, bg)
            ctrl_bg = None
            if args.control and Path(args.control).suffix in (".bedgraph", ".bdg"):
                ctrl_bg = args.control
            run_seacr(bg, Path(args.out) / "seacr" / name,
                      control_bg=ctrl_bg, mode=args.seacr_mode)

        if args.method in ("macs2", "both"):
            run_macs2(bam, Path(args.out) / "macs2", name,
                      control_bam=args.control if args.control and str(args.control).endswith(".bam") else None,
                      qvalue=args.macs_qvalue)

    print("\n[+] Peak calling finished")

if __name__ == "__main__":
    main()
