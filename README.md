# Hexaloom

Typed grammars for binary data.

Hexaloom uses a typed Python authoring DSL to describe binary formats and emit a portable instruction stream for interpreters, native parser generators, and inspection tools.

## Repository layout

- `hexaloom/` contains the Python authoring package.
- `crates/hexaloom-syntax/` owns the portable wire format shared by Python and Rust.
- `crates/hexaloom/` contains the compiler and code generators.
- `crates/hexaloom-interpreter/` contains the reference interpreter.
- `crates/hexaloom-lsp/` contains the Language Server Protocol implementation.
- `crates/hexaloom-cli/` provides the `hexaloom` command and drives the libraries above.

The Cargo workspace and uv project both live at the repository root.

## Development

```console
uv sync --locked
uv run scripts/check-versions.py
uv build
cargo fmt --all --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo nextest run --workspace --locked --no-tests=pass
cargo test --workspace --doc --locked
```

Release preparation, registry trust and publication are documented in [docs/releasing.md](docs/releasing.md).
