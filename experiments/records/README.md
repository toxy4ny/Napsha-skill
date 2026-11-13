# Complete round records

Store exact inputs, settings exports, loading evidence, and reviewer notes here, one
directory per round:

```text
records/<round-id>/
  input-A-turn1.txt
  input-B-turn1.txt
  loading.txt
  settings.md
```

Response texts themselves stay under [`../raw/`](../raw/) and are never edited after
publication. Every artifact referenced by a complete manifest round must exist and
match its recorded SHA-256; see [`../SCHEMA.md`](../SCHEMA.md) and
[`../record-template.json`](../record-template.json).

Rounds 01–04 predate this directory. They are preserved as `historical_partial` and
are not a precedent for adding new rounds without complete provenance.
