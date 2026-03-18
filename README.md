# QuantEcon WASM Lectures

A browser-based version of [A First Course in Quantitative Economics with Python](https://intro.quantecon.org/intro.html) powered by [Pyodide](https://pyodide.org/) and [JupyterLite](https://jupyterlite.readthedocs.io/).

**Live site:** https://quantecon.github.io/lecture-wasm/

This repository contains a WASM-compatible subset of the QuantEcon lecture series. Using the Pyodide kernel, these lectures run entirely in the browser without requiring any local Python installation.

## Development

### Prerequisites

- [Node.js](https://nodejs.org/) 18.x or higher

### Build and serve locally

```bash
# Install dependencies
npm install -g mystmd thebe-core thebe thebe-lite

# Build
cd lectures
myst build --html

# Serve locally (http://localhost:3000)
myst start
```

### Updating lectures

> **Do not edit lectures directly in this repository.**

Lectures are synced from the [wasm branch of lecture-python-intro](https://github.com/QuantEcon/lecture-python-intro/tree/wasm). To update:

1. Make changes in the [wasm branch](https://github.com/QuantEcon/lecture-python-intro/tree/wasm) of `lecture-python-intro`
2. Run the sync script:
   ```bash
   python update_lectures.py
   ```

The sync script downloads the latest content, converts `!pip` to `%pip`, removes `--upgrade` flags, and fixes MyST directive syntax for WASM compatibility.

### CI/CD

- **Push to `main`** — Builds and deploys to [GitHub Pages](https://quantecon.github.io/lecture-wasm/)
- **Pull requests** — Builds and deploys a preview to Netlify

### WASM-unsupported lectures

The following lectures are excluded due to Pyodide/WASM package limitations:

- `business_cycle`
- `inequality`
- `prob_dist`
- `heavy_tails`
- `commod_price`
- `lp_intro`
- `short_path`
- `input_output`

## Technology

- [MyST Markdown](https://mystmd.org/) — Content format and build system
- [Pyodide](https://pyodide.org/) — Python runtime in WebAssembly
- [JupyterLite](https://jupyterlite.readthedocs.io/) — Browser-based Jupyter
- [Thebe](https://thebe.readthedocs.io/) — Executable code cells
- [QuantEcon Theme](https://github.com/QuantEcon/quantecon-theme) — MyST site theme

## Authors

- **Thomas J. Sargent** — New York University; Hoover Institution
- **John Stachurski** — Research School of Economics, ANU

## License

[Creative Commons Attribution 4.0 International (CC-BY-4.0)](LICENSE)
