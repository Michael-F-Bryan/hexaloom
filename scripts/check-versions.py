#!/usr/bin/env python3
"""Verify that every publishable Hexaloom component has the same version."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CRATES = {
    "hexaloom",
    "hexaloom-cli",
    "hexaloom-interpreter",
    "hexaloom-lsp",
    "hexaloom-syntax",
}


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as source:
        return tomllib.load(source)


def package_version(lockfile: dict[str, Any], name: str) -> str | None:
    matches = [
        package.get("version")
        for package in lockfile.get("package", [])
        if package.get("name") == name
    ]
    return matches[0] if len(matches) == 1 and isinstance(matches[0], str) else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", help="Release tag to compare with the package version")
    args = parser.parse_args()

    pyproject = load_toml(ROOT / "pyproject.toml")
    cargo = load_toml(ROOT / "Cargo.toml")
    uv_lock = load_toml(ROOT / "uv.lock")
    cargo_lock = load_toml(ROOT / "Cargo.lock")

    version = pyproject["project"]["version"]
    errors: list[str] = []

    if cargo["workspace"]["package"]["version"] != version:
        errors.append("Cargo workspace version differs from the Python package")

    if package_version(uv_lock, "hexaloom") != version:
        errors.append("uv.lock contains a different Hexaloom version")

    workspace_dependencies = cargo["workspace"].get("dependencies", {})
    for name, dependency in workspace_dependencies.items():
        if name in CRATES and dependency.get("version") != version:
            errors.append(f"workspace dependency {name!r} does not use {version}")

    manifests = sorted((ROOT / "crates").glob("*/Cargo.toml"))
    manifest_names: set[str] = set()
    for manifest_path in manifests:
        manifest = load_toml(manifest_path)
        package = manifest["package"]
        name = package["name"]
        manifest_names.add(name)
        if package.get("version") != {"workspace": True}:
            errors.append(f"{manifest_path.relative_to(ROOT)} does not inherit its version")

    if manifest_names != CRATES:
        missing = sorted(CRATES - manifest_names)
        unexpected = sorted(manifest_names - CRATES)
        errors.append(f"workspace crate set differs: missing={missing}, unexpected={unexpected}")

    for name in sorted(CRATES):
        if package_version(cargo_lock, name) != version:
            errors.append(f"Cargo.lock contains a different version for {name!r}")

    if args.tag is not None and args.tag != f"v{version}":
        errors.append(f"release tag {args.tag!r} does not match v{version}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Hexaloom versions agree at {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
