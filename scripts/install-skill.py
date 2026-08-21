#!/usr/bin/env python3
"""Install the skill payload into a supported agent's skills directory."""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


SKILL_NAME = "building-immersive-video-websites"
TARGETS = {
    "codex": Path.home() / ".codex" / "skills" / SKILL_NAME,
    "claude": Path.home() / ".claude" / "skills" / SKILL_NAME,
    "agents": Path.home() / ".agents" / "skills" / SKILL_NAME,
}
PAYLOAD = ("SKILL.md", "agents", "references", "scripts", "assets", "compatibility")


def parse_args():
    parser = argparse.ArgumentParser(description="Install the skill payload safely.")
    parser.add_argument("--target", choices=(*TARGETS, "project"), default="codex")
    parser.add_argument("--dest", type=Path, help="Installation directory")
    parser.add_argument("--dry-run", action="store_true", help="Report without writing")
    parser.add_argument("--force", action="store_true", help="Back up an existing destination")
    args = parser.parse_args()
    if args.target == "project" and args.dest is None:
        parser.error("--dest is required when --target project")
    return args


def backup_path(destination):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return destination.with_name(f"{destination.name}.backup-{timestamp}")


def copy_payload(source, destination):
    destination.mkdir(parents=True)
    for name in PAYLOAD:
        item = source / name
        if item.is_file():
            shutil.copy2(item, destination / name)
        elif item.is_dir():
            shutil.copytree(item, destination / name)


def main():
    args = parse_args()
    source = Path(__file__).resolve().parents[1]
    destination = args.dest.expanduser() if args.dest else TARGETS[args.target]
    destination = destination.resolve()
    result = {
        "status": "dry-run" if args.dry_run else "installed",
        "source": str(source),
        "destination": str(destination),
    }

    if args.dry_run:
        print(json.dumps(result))
        return 0

    if destination.exists():
        if not args.force:
            print(json.dumps({**result, "status": "conflict"}), file=sys.stderr)
            return 2
        backup = backup_path(destination)
        shutil.move(str(destination), str(backup))
        result["backup"] = str(backup)

    copy_payload(source, destination)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
