# Whitebox Plugin - GPS Display

This is a plugin for [whitebox](https://gitlab.com/whitebox-aero) that displays the GPS data using leaflet.js.

## Installation

Simply install the plugin to whitebox:

```
poetry add whitebox-plugin-gps-display
```

## Adding Plugin to Whitebox Locally (For Development)

1. Set up whitebox locally.
2. Clone this repository.
3. Add plugin to whitebox (editable mode): `poetry add -e path/to/plugin.`
4. Run the whitebox server.

## Running Plugin Tests Locally

1. Ensure you have the plugin installed in whitebox like mentioned above.
2. Install playwright to whitebox: `poetry add playwright`.
3. Run: `poetry run playwright install`.
4. Run: `poetry run playwright install-deps` (optional, for Linux only).
5. Run the tests: `make test`.

This would load the plugin in whitebox, discover its tests and run them.

## Contribution Guidelines

1. Write tests for each new feature.
2. Ensure coverage is 90% or more.
3. [Google style docstrings](https://mkdocstrings.github.io/griffe/docstrings/#google-style)
   should be used for all functions and classes.
