import json
import os

output_file = 'scancode-results/results.json'
github_output_file = os.environ.get('GITHUB_OUTPUT')

if not os.path.exists(output_file):
    print("Error: The results file was not found.")
    with open(github_output_file, 'a') as f:
        f.write("has_licenses=false\n")
        f.write("comment_body=No scan results file found.\n")
    exit(1)

with open(output_file, 'r') as f:
    data = json.load(f)

if not data.get('files', []):
    comment_body = "### ⚠️ ScanCode Check: NO FILES SCANNED\n\n"
    comment_body += "No files were found to scan, or the scan failed to produce a valid output."
    with open(github_output_file, 'a') as f:
        f.write("has_licenses=false\n")
        f.write(f"comment_body={comment_body}\n")
    exit(0)

files = data.get('files', [])
license_map = {}
for file in files:
    file_path = file.get('path')
    for lic in file.get('licenses', []):
        license_key = lic.get('spdx_license_key') or lic.get('key') or lic.get('license_expression')
        if license_key:
            license_map.setdefault(license_key, []).append(file_path)

comment_body = ""
has_licenses = "false"
if license_map:
    has_licenses = "true"
    comment_body += "### ✅ ScanCode License Check: SUCCESS\n\n"
    comment_body += "The following licenses were detected:\n\n"
    comment_body += "| License | Files |\n"
    comment_body += "|---|---|\n"
    for license_key, file_paths in license_map.items():
        comment_body += f"| `{license_key}` | `{', '.join(file_paths)}` |\n"
else:
    comment_body += "### ⚠️ ScanCode License Check: NO LICENSES DETECTED\n\n"
    comment_body += "No license information was found in the scanned files."

with open(github_output_file, 'a') as f:
    f.write(f"has_licenses={has_licenses}\n")
    comment_body = comment_body.replace('\n', '@@__gh_linebreak__@@')
    f.write(f"comment_body={comment_body}\n")
