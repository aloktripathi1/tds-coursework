import zipfile
import json
from collections import defaultdict

ZIP_FILE = "api_data_your-student-id.zip"

counts = defaultdict(int)

with zipfile.ZipFile(ZIP_FILE) as z:
    for name in z.namelist():
        if not name.endswith(".json"):
            continue
        data = json.loads(z.read(name))
        # Each file is a list of records
        records = data if isinstance(data, list) else [data]
        for rec in records:
            level = rec.get("metrics", {}).get("level")
            if level is not None:
                counts[int(level)] += 1

result = "|".join(f"level{k}:{counts[k]}" for k in sorted(counts))
print(result)
