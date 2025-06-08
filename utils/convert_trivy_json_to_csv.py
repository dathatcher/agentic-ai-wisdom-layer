import json
import csv
import sys
from pathlib import Path

def flatten_vulns(trivy_json):
    output = []
    for target in trivy_json.get("Results", []):
        for vuln in target.get("Vulnerabilities", []):
            output.append({
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
    return output

def flatten_components(sbom_json):
    output = []
    for comp in sbom_json.get("components", []):
        output.append({
            "Type": comp.get("type", ""),
            "Name": comp.get("name", ""),
            "Version": comp.get("version", ""),
            "Package URL": comp.get("purl", ""),
            "License(s)": ", ".join(lic.get("license", {}).get("id", "") for lic in comp.get("licenses", [])) if comp.get("licenses") else "",
            "CPE": ", ".join(comp.get("cpe", [])) if isinstance(comp.get("cpe"), list) else comp.get("cpe", ""),
            "Supplier": comp.get("supplier", {}).get("name", ""),
            "Description": comp.get("description", ""),
        })
    return output

def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_trivy_json_to_csv.py <path-to-json>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = input_path.with_suffix('.csv')

    try:
        with input_path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        if "Results" in data:
            rows = flatten_vulns(data)
        elif "components" in data:
            rows = flatten_components(data)
        else:
            print("❌ Error: Unsupported JSON structure.")
            sys.exit(1)

        if not rows:
            print("⚠️ No data to write.")
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
