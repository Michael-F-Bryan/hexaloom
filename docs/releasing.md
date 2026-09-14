# Releasing Hexaloom

Hexaloom uses one version for the Python package and every Rust crate. Release Please maintains the release pull request and creates a `vX.Y.Z` GitHub release when that pull request is merged. The release workflow then dispatches `.github/workflows/cd.yml` at that tag.

Before merging a release pull request, CI must show that `pyproject.toml`, `uv.lock`, the Cargo workspace, internal dependency requirements, and `Cargo.lock` agree. `scripts/check-versions.py` enforces that transaction.

## Registry trust

The `pypi` and `crates-io` GitHub environments identify the publication jobs. Configure the registries against the exact repository, workflow and environment names:

| Registry | Repository | Workflow | Environment |
| --- | --- | --- | --- |
| PyPI | `Michael-F-Bryan/hexaloom` | `cd.yml` | `pypi` |
| crates.io | `Michael-F-Bryan/hexaloom` | `cd.yml` | `crates-io` |

PyPI supports a pending trusted publisher for the first release. Each crates.io crate must be published once with an API token before its trusted publisher can be configured. After that bootstrap, CD uses short-lived OIDC credentials for both registries.

Before the first registry publication, add the agreed licence files and Cargo/Python licence metadata. Registry publication is permanent; do not use the first release to settle licensing by accident.

## Publication

CD verifies the release tag and reruns the complete Python and Rust gates before either registry receives an artefact. Rust crates are then published in dependency order with `cargo-workspaces`; the Python job uploads the wheel and source distribution built during preflight.

A failed publication does not justify moving a tag or overwriting a package version. Rerun only the failed job after correcting registry configuration, or prepare a new patch release when the artefact itself is wrong.
