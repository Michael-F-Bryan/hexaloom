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
uv sync
uv run python -c "import hexaloom"
cargo metadata --no-deps
```
