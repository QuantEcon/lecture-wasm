# QuantEcon WASM Lectures

[![Build Status](https://github.com/QuantEcon/lecture-wasm/workflows/Build%20and%20Deploy%20to%20GitHub%20Pages/badge.svg)](https://github.com/QuantEcon/lecture-wasm/actions)

A browser-based version of [A First Course in Quantitative Economics with Python](https://intro.quantecon.org/intro.html) powered by Pyodide and JupyterLite.

## Overview

This repository contains a WASM-compatible subset of the QuantEcon lecture series. Using Pyodide kernel and JupyterLite, these lectures run entirely in your browser without requiring any local Python installation.

**Key Features:**
- 🌐 **Browser-based execution** - No installation required
- 🚀 **Powered by Pyodide** - Full Python environment in WebAssembly
- 📚 **Interactive learning** - Execute code cells directly in the browser
- 🔄 **Synchronized content** - Maintained in sync with the main lecture repository

## Getting Started

### View the Lectures

Visit the live site: [QuantEcon WASM Lectures](https://quantecon.github.io/lecture-wasm/)

### Local Development

#### Prerequisites
- Python 3.8 or higher
- Node.js 18.x or higher

#### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/QuantEcon/lecture-wasm.git
   cd lecture-wasm
   ```

2. Install Node.js dependencies:
   ```bash
   npm install -g mystmd thebe-core thebe thebe-lite
   ```

   **Note:** Python dependencies in `requirements.txt` are legacy from the old build system and not required for `mystmd` builds.

#### Build and Serve

Build the lecture series:
```bash
cd lectures
myst build --html
```

Start the local development server:
```bash
cd lectures
myst start
```

The lectures will be available at `http://localhost:3000` by default.

To stop the server, press `Ctrl+C` in the terminal.

## Content Management

### Updating Lectures

⚠️ **Important**: Do not edit lectures directly in this repository!

To update lecture content:

1. Make your changes in the [wasm branch of lecture-python-intro](https://github.com/QuantEcon/lecture-python-intro/tree/wasm)
2. Run the synchronization script in this repository:
   ```bash
   python update_lectures.py
   ```

This workflow ensures all lectures stay synchronized with the main repository and maintains WASM compatibility.

### What the Sync Script Does

The `update_lectures.py` script:
- Downloads the latest content from the `wasm` branch
- Copies lecture files to the `lectures/` directory  
- Converts `!pip install` to `%pip install` for WASM compatibility
- Removes `--upgrade` flags from pip commands
- Fixes MyST directive syntax for solutions and exercises
- Cleans up temporary files

### WASM-Unsupported Lectures

The following lectures are excluded due to WASM/Pyodide limitations:

- `business_cycle` - Requires packages not available in Pyodide
- `inequality` - Complex data processing dependencies
- `prob_dist` - Statistical packages with C extensions
- `heavy_tails` - Advanced statistical libraries
- `commod_price` - Financial data dependencies
- `lp_intro` - Linear programming solvers
- `short_path` - Graph algorithms requiring native code
- `input_output` - Matrix computation dependencies

## Project Structure

```
lecture-wasm/
├── .github/
│   ├── workflows/
│   │   └── ci.yml                 # CI/CD pipeline
│   └── copilot-instructions.md    # GitHub Copilot guidelines
├── lectures/
│   ├── myst.yml                   # MyST configuration
│   ├── *.md                       # Lecture content (MyST Markdown)
│   ├── _static/                   # Static assets
│   ├── _admonition/               # Reusable admonitions
│   ├── datasets/                  # Data files
│   └── figures/                   # Generated figures
├── update_lectures.py             # Content sync script
├── requirements.txt               # Python build dependencies
├── README.md                      # This file
└── LICENSE                        # CC-BY-4.0 License
```

## Technology Stack

- **[MyST Markdown](https://mystmd.org/)** - Markdown flavor for technical documentation and build system
- **[JupyterLite](https://jupyterlite.readthedocs.io/)** - Browser-based Jupyter environment
- **[Pyodide](https://pyodide.org/)** - Python runtime in WebAssembly
- **[Thebe](https://thebe.readthedocs.io/)** - Executable code cells
- **GitHub Actions** - Automated builds and deployment
- **Netlify** - PR preview deployments

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

### On Push to `main`
- Builds MyST HTML with GitHub Pages base URL
- Deploys to GitHub Pages at https://quantecon.github.io/lecture-wasm/

### On Pull Requests  
- Builds preview version
- Deploys to Netlify with PR-specific URL
- Posts preview link as PR comment

### Build Process
- Uses Node.js 18.x
- Installs MyST CLI and Thebe dependencies
- Builds from `lectures/` directory
- Outputs to `lectures/_build/html/`

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make changes in the [upstream wasm branch](https://github.com/QuantEcon/lecture-python-intro/tree/wasm)
4. Sync to this repository using `update_lectures.py`
5. Submit a pull request

For detailed contribution guidelines, see [CONTRIBUTING.md](docs/CONTRIBUTING.md).

For major changes, please open an issue first to discuss what you would like to change.

## Documentation

- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute to this project
- **[Architecture](docs/ARCHITECTURE.md)** - System architecture and technical design
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Common commands and troubleshooting
- **[Project Review](docs/PROJECT_REVIEW.md)** - Comprehensive project review and improvements

## Authors

- **Thomas J. Sargent** - Professor of Economics, New York University; Senior Fellow, Hoover Institution
- **John Stachurski** - Professor, Research School of Economics, ANU

See [about.md](lectures/about.md) for a complete list of contributors.

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](LICENSE) (CC-BY-4.0).

## Support and Resources

- **Documentation**: https://intro.quantecon.org/
- **Main Repository**: https://github.com/QuantEcon/lecture-python-intro  
- **Issue Tracker**: https://github.com/QuantEcon/lecture-wasm/issues
- **QuantEcon Website**: https://quantecon.org/

## Acknowledgments

This project builds upon the excellent work of the QuantEcon team and numerous contributors. Special thanks to all research assistants who helped develop and maintain these lectures.

For detailed credits, see the [About page](lectures/about.md).
