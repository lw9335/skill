from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / "references/provenance.json").read_text(encoding="utf-8"))
source = (root / manifest["source"]).read_bytes()
assert hashlib.sha256(source).hexdigest() == manifest["source_sha256"], "Source changed"
assert len(manifest["prompts"]) == 12, "Expected 12 prompts"
assert len({p["path"] for p in manifest["prompts"]}) == 12, "Duplicate paths"
actual_files = {p.relative_to(root).as_posix() for p in (root / "assets/prompts").glob("*.txt")}
assert actual_files == {p["path"] for p in manifest["prompts"]}, "Prompt file set changed"
for entry in manifest["prompts"]:
    data = (root / entry["path"]).read_bytes()
    original = source[entry["start_byte"]:entry["end_byte_exclusive"]]
    assert data == original, f"Text differs: {entry['path']}"
    assert hashlib.sha256(data).hexdigest() == entry["sha256"], f"Hash differs: {entry['path']}"
print("PASS: all 12 prompts match exact source byte ranges and SHA-256 hashes.")
