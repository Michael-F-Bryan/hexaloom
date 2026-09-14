# Hexaloom

Typed grammars for binary data.

Hexaloom uses a typed Python authoring DSL to describe binary formats and emit a portable instruction stream for interpreters, native parser generators, and inspection tools.

## Repository layout

- `hexaloom/` contains the Python authoring package.
- `crates/` contains the Rust workspace crates.

The Cargo workspace and uv project both live at the repository root.

## Development

```console
uv sync
uv run python -c "import hexaloom"
cargo metadata --no-deps
```
