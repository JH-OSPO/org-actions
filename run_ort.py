import argparse
import subprocess
import os
import sys

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-path", required=True, help="Path to the repository to scan")
    parser.add_argument("--ort-output", default="ort-results", help="Output directory for ORT results")
    parser.add_argument("--ort-analyzer", default="ort", help="Path to ORT CLI")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.repo_path)
    output_path = os.path.abspath(args.ort_output)
    ort_cmd = args.ort_analyzer

    os.makedirs(output_path, exist_ok=True)

    analyze_output = os.path.join(output_path, "analyzer")
    os.makedirs(analyze_output, exist_ok=True)
    run_cmd(f"{ort_cmd} analyze -i {repo_path} -o {analyze_output} --stacktrace")

    report_output = os.path.join(output_path, "report")
    os.makedirs(report_output, exist_ok=True)
    run_cmd(f"{ort_cmd} report -i {analyze_output} -o {report_output} --formats Html,Text")

    print(f"ORT scan completed. Results saved in: {output_path}")

if __name__ == "__main__":
    main()
