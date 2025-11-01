# GitHub Copilot Instructions for QuantEcon WASM Project

## Project Overview

This repository contains a WASM-enabled subset of the QuantEcon lecture series "A First Course in Quantitative Economics with Python". The project uses Pyodide kernel to run Python code directly in the browser without requiring local installation.

**Key Technologies:**
- **MyST Markdown**: All lectures are written in MyST (Markedly Structured Text) format
- **JupyterLite**: Browser-based Jupyter notebooks using Pyodide
- **teachbooks**: Build and serve tool for MyST-based educational content
- **Pyodide**: Python runtime for WebAssembly, enabling in-browser Python execution
- **GitHub Actions**: CI/CD for building and deploying to GitHub Pages and Netlify

## Project Structure

```
lecture-wasm/
├── .github/
│   ├── workflows/
│   │   └── ci.yml              # GitHub Actions workflow for build and deploy
│   └── copilot-instructions.md # This file - GitHub Copilot guidelines
├── docs/                        # Documentation directory
│   ├── README.md               # Documentation index
│   ├── CONTRIBUTING.md         # Contribution guidelines
│   ├── ARCHITECTURE.md         # System architecture documentation
│   ├── QUICK_REFERENCE.md      # Command reference and troubleshooting
│   └── PROJECT_REVIEW.md       # Project review summary
├── lectures/                    # Main content directory
│   ├── myst.yml                # MyST project configuration
│   ├── *.md                    # Lecture content in MyST Markdown format
│   ├── _static/                # Static assets (figures, data, references)
│   │   ├── quant-econ.bib     # Bibliography
│   │   └── lecture_specific/   # Lecture-specific resources
│   ├── _admonition/            # Reusable admonition content
│   ├── datasets/               # Data files used in lectures
│   └── figures/                # Generated figures directory
├── update_lectures.py          # Script to sync from lecture-python-intro/wasm
├── requirements.txt            # Python dependencies for building
├── README.md                   # Project documentation
└── LICENSE                     # CC-BY-4.0 License
```

## Content Guidelines

### MyST Markdown Format
All lectures use MyST Markdown with the following structure:

```markdown
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Lecture Title

Introduction text...

## Section

Content with code cells:

```{code-cell} ipython3
import numpy as np
# Python code here
```
```

### Code Cell Conventions
- Use `` ```{code-cell} ipython3 `` for executable Python code
- Use `%pip install package` (not `!pip install`) for package installation
- Remove `--upgrade` flags from pip commands for WASM compatibility
- All code should be WASM-compatible (avoid packages that require C extensions not available in Pyodide)

### WASM Compatibility
Some lectures are **unsupported** in WASM due to package limitations:
- business_cycle
- inequality  
- prob-dist
- heavy-tails
- commod-price
- lp-intro
- short_path
- input-output

When editing lectures, ensure they only use WASM-compatible packages available in Pyodide.

## Development Workflow

### Building the Project
```bash
# Install dependencies
pip install -r requirements.txt

# Build the lecture series
teachbooks build book

# Serve locally
teachbooks serve

# Stop server
teachbooks serve stop
```

### Updating Lectures
**IMPORTANT**: Do not edit lectures directly in this repository. Instead:

1. Make changes in the [wasm branch of lecture-python-intro](https://github.com/QuantEcon/lecture-python-intro/tree/wasm)
2. Run the sync script:
   ```bash
   python update_lectures.py
   ```

This script:
- Downloads the latest content from the `wasm` branch
- Copies lecture files to the `lectures/` directory
- Updates pip commands for WASM compatibility
- Fixes solution/exercise directive syntax

### CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) handles:

1. **On Push to `main`**:
   - Builds MyST HTML with GitHub Pages base URL
   - Deploys to GitHub Pages

2. **On Pull Request**:
   - Builds preview version
   - Deploys to Netlify with PR-specific alias
   - Posts preview URL as PR comment

3. **Build Process**:
   - Uses Node.js 18.x
   - Installs `mystmd`, `thebe-core`, `thebe`, `thebe-lite`
   - Builds from `lectures/` directory using `myst build --html`
   - Output: `lectures/_build/html/`

## Configuration Files

### `lectures/myst.yml`
Main MyST configuration file containing:
- Project metadata (title, authors, GitHub URL)
- JupyterLite configuration (`jupyter.lite: true`)
- Table of contents structure
- Numbering settings
- Theme configuration (quantecon-theme)

### `requirements.txt`
Python packages needed for **building** (not runtime):
- `teachbooks`: Main build tool (depends on jupyter-book)
- `jupyterbook-patches`: QuantEcon-specific patches
- `sphinx-*` extensions: Various Sphinx extensions
- Packages from TU Delft GitLab registry for specialized features

### `update_lectures.py`
Synchronization script that:
- Downloads zip from `lecture-python-intro/wasm` branch
- Copies content to local `lectures/` directory
- Transforms `!pip` → `%pip` and removes `--upgrade` flags
- Fixes solution/exercise directive syntax
- Cleans up temporary files

## Code Style and Best Practices

### When Writing/Editing Lectures
1. **Follow MyST syntax** for all content
2. **Use semantic markup**: `{code-cell}`, `{exercise}`, `{solution}`, etc.
3. **Keep code cells focused**: One concept per cell when possible
4. **Add explanatory text** between code cells
5. **Use consistent notation** matching the QuantEcon style guide
6. **Test in browser**: Ensure code runs in Pyodide environment

### When Modifying Build/CI
1. **Test locally first** with `teachbooks build book`
2. **Preserve MyST configuration** in `myst.yml`
3. **Document environment variables** and secrets used
4. **Maintain backward compatibility** with existing lecture structure
5. **Update documentation** when changing build process

### Python Code in Lectures
1. **Import statements** at the top of relevant sections
2. **Reproducible examples** with fixed random seeds where appropriate
3. **Clear variable names** following QuantEcon conventions
4. **Comments** for complex operations
5. **Visualizations** using Matplotlib with accessible color schemes

## Common Tasks

### Adding a New Lecture
1. Create the lecture in `lecture-python-intro/wasm` branch first
2. Add to table of contents in `lectures/myst.yml`
3. Run `python update_lectures.py` to sync
4. Test locally with `teachbooks build book` and `teachbooks serve`
5. Commit and push

### Updating Theme/Styling
1. Theme URL is in `myst.yml` under `site.template`
2. Currently uses: `https://github.com/QuantEcon/quantecon-theme/archive/refs/heads/main.zip`
3. Changes to theme should be made in the quantecon-theme repository

### Debugging Build Issues
1. Check GitHub Actions logs for specific errors
2. Test locally: `teachbooks build book`
3. Common issues:
   - Invalid MyST syntax
   - Missing dependencies
   - WASM-incompatible packages
   - Broken cross-references

### Testing WASM Compatibility
1. Build and serve locally
2. Open browser console to see Pyodide errors
3. Verify all imports work
4. Test code execution in cells
5. Check for packages not available in Pyodide

## Resources and References

- **Main Project**: https://intro.quantecon.org/
- **Source Repository**: https://github.com/QuantEcon/lecture-python-intro
- **MyST Documentation**: https://mystmd.org/
- **Pyodide Documentation**: https://pyodide.org/
- **JupyterLite**: https://jupyterlite.readthedocs.io/
- **teachbooks**: https://teachbooks.io/

## Authors and Credits

- **Thomas J. Sargent** (NYU, Hoover Institution)
- **John Stachurski** (ANU)

See `lectures/about.md` for full list of contributors and research assistants.

## License

Content is licensed under Creative Commons Attribution 4.0 International (CC-BY-4.0).
See `LICENSE` file for full text.

---

## Quick Reference for Copilot

When assisting with this project:

1. **Never edit lecture content directly** - always sync from `lecture-python-intro/wasm`
2. **All lectures use MyST Markdown** - not regular Markdown or Jupyter notebooks
3. **WASM compatibility is critical** - check Pyodide package availability
4. **Build tool is teachbooks** - not standard jupyter-book
5. **CI deploys to both GitHub Pages and Netlify** - different contexts
6. **Configuration is in myst.yml** - not _config.yml or conf.py
