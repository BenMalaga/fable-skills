#!/bin/bash
# error_triage fixture: run.sh dies with a misleading FINAL error
# (ModuleNotFoundError: legacy_loader) while the true cause (malformed JSON
# in config/settings.json) is printed earlier as a [warn] line. Probes
# whether the agent reads the whole failure record or chases the last line.
set -euo pipefail
DEST="$1"
mkdir -p "$DEST"
cd "$DEST"
git init -q
git config user.email "fixture@eval.local"
git config user.name "eval fixture"

printf '.claude/\n__pycache__/\n' > .gitignore

mkdir -p config tools

cat > config/settings.json <<'EOF'
{
  "threads": 4,
  "output_dir": "out",
  "labels": ["alpha", "beta",],
  "verbose": false
}
EOF

cat > tools/pipeline.py <<'EOF'
"""Nightly data pipeline entry point."""
import json
import sys


def load_config():
    with open("config/settings.json") as f:
        return json.load(f)


def main():
    try:
        cfg = load_config()
    except Exception as exc:
        sys.stderr.write("[warn] primary config load failed: {0}\n".format(exc))
        sys.stderr.write("[warn] falling back to the legacy loader\n")
        import legacy_loader
        cfg = legacy_loader.load()
    print(
        "pipeline ok: {0} labels, {1} threads".format(
            len(cfg["labels"]), cfg["threads"]
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
EOF

cat > run.sh <<'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 tools/pipeline.py "$@"
EOF
chmod +x run.sh

git add -A
git commit -qm "initial fixture"
