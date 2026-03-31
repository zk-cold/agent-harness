import sys
from pathlib import Path

from scripts.mission_linter import lint

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "mission.md"
violations = lint(path)
for v in violations:
    print(v)
sys.exit(1 if violations else 0)
