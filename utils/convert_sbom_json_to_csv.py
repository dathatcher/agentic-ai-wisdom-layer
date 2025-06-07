import json
import csv
import sys
from pathlib import Path

def flatten_components(sbom_json):
    components = []

    for comp in sbom_json.get("components", []):
        components.append({
            "Type": comp.get("type", ""),
            "Name": comp.get("name", ""),
            "Version": comp.get("version", ""),
            "Package URL": comp.get("purl", ""),
            "License(s)": ", ".join(lic.get("license", {}).get("id", "") for lic in comp.get("licenses", [])) if comp.get("licenses") else "",
            "CPE": ", ".join(comp.get("cpe", [])) if isinstance(comp.get("cpe"), list) else comp.get("cpe", ""),
            "Supplier": comp.get("supplier", {}).get("name", ""),
            "Description": comp.get("description", ""),
        })
    return components

def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_sbom_json_to_csv.py <path-to-sbom-json>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = input_path.with_suffix('.csv')

    try:
        with input_path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        rows = flatten_components(data)

        if not rows:
            print("No components found in SBOM.")
            sys.exit(0)

        with output_path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"✅ SBOM CSV written to {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
