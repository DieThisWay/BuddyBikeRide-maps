"""Builds manifest.json, the list of country files the app shows, from the per-country build results."""
import json
import os
import sys

tag, repo, built = sys.argv[1], sys.argv[2], sys.argv[3]
countries = {c['id']: c for c in json.load(open('countries.json'))}
out = {'version': tag, 'countries': {}}
for cid, c in countries.items():
    pm, meta = os.path.join(built, f'{cid}.pmtiles'), os.path.join(built, f'{cid}.json')
    if not (os.path.exists(pm) and os.path.exists(meta)):
        continue
    m = json.load(open(meta))
    out['countries'][cid] = {
        'ru': c['ru'],
        'en': c['en'],
        'url': f'https://github.com/{repo}/releases/download/{tag}/{cid}.pmtiles',
        'bytes': os.path.getsize(pm),
        'bbox': m['bbox'],
        'boundary': m['boundary'],
    }
json.dump(out, open(os.path.join(built, 'manifest.json'), 'w'), ensure_ascii=False)
print(f"{len(out['countries'])} countries in manifest")
