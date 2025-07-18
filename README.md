# Rippy

My opinionated workflow for [MakeMKV] and [Handbrake].

# Tests

``` sh 
uv run pytest
```

## Marks

- `cli`: run tests for cli.
- `core`: run tests for core library.

Example:

``` sh 
uv run pytest -m cli
```

[Handbrake]:https://handbrake.fr/
[MakeMKV]:https://www.makemkv.com/
