import json
import csv
import sys
from pathlib import Path

def flatten_vulns(trivy_json):
    vulnerabilities = []

    for target in trivy_json.get("Results", []):
        for vuln in target.get("Vulnerabilities", []):
            vulnerabilities.append({
                "Target": target.get("Target", ""),
                "PkgName": vuln.get("PkgName", ""),
                "InstalledVersion": vuln.get("InstalledVersion", ""),
                "FixedVersion": vuln.get("FixedVersion", ""),
                "Severity": vuln.get("Severity", ""),
                "Title": vuln.get("Title", ""),
                "Description": vuln.get("Description", "").replace("\n", " ").strip(),
                "PrimaryURL": vuln.get("PrimaryURL", ""),
                "CVSS Score": vuln.get("CVSS", {}).get("nvd", {}).get("V3Score", "")
            })
    return vulnerabilities

def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_trivy_json_to_csv.py <path-to-json>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = input_path.with_suffix('.csv')

    try:
        with input_path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        rows = flatten_vulns(data)

        if not rows:
            print("No vulnerabilities found in input.")
            sys.exit(0)

        with output_path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"✅ CSV written to {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
