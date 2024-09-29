import subprocess
from parse_pubmed_json import parse_pubmed_json
import sys
import json

pubmed_id = sys.argv[1]
script_path = ["python","get_pmid.py","pubmed_id"]
try:
    data = subprocess.run(script_path, stdout=subprocess.PIPE, check=True)
except subprocess.CalledProcessError as e:
    print(e.stdout)
    exit(1)

data = data.stdout

sections = ["abstract","methods","results","discuss"]
data = parse_pubmed_json(data, sections)
print(data["text"])
for section in data["sections"]:
   print(section, "length", len(data["sections"][section]))
