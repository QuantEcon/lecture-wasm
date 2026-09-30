# QuantEcon WASM Lectures

A browser-based version of [A First Course in Quantitative Economics with Python](https://intro.quantecon.org/intro.html) powered by [Pyodide](https://pyodide.org/) and [JupyterLite](https://jupyterlite.readthedocs.io/).

**Live site:** https://quantecon.github.io/lecture-wasm/

This repository contains a WASM-compatible subset of the QuantEcon lecture series. Using the Pyodide kernel, these lectures run entirely in the browser without requiring any local Python installation.

## Development

### Prerequisites

- [Node.js](https://nodejs.org/) 20.x or higher

### Build and serve locally

```bash
# Install dependencies
npm install -g mystmd@1.9.1 thebe-core thebe thebe-lite

# Build
cd lectures
myst build --html

# Serve locally (http://localhost:3000)
myst start
```

### Updating lectures

Edit lectures directly in `lectures/` and open a pull request. CI builds the site without running any code, so check a change by running the lecture's code in the browser on the pull request's preview.

The old sync from the [`wasm` branch of lecture-python-intro](https://github.com/QuantEcon/lecture-python-intro/tree/wasm) is retired: that branch has not changed since 2025-04-24, and `update_lectures.py` would copy its lectures over the ones here.

### CI/CD

- **Push to `main`** — Builds and deploys to [GitHub Pages](https://quantecon.github.io/lecture-wasm/)
- **Pull requests** — Builds and deploys a preview to Netlify

### WASM-unsupported lectures

The following lectures are excluded due to Pyodide/WASM package limitations:

- `inequality`
- `prob_dist`
- `heavy_tails`
- `commod_price`
- `lp_intro`
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
