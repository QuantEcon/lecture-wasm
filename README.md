# QuantEcon WASM Project

This repository contains the WASM-enabled version of [QuantEcon's Introduction to Quantitative Economics with Python](https://intro.quantecon.org/intro.html) lecture series.

**Live Site**: [interactive.quantecon.org](https://interactive.quantecon.org)

This project uses **Pyodide** to run Python code directly in the browser, allowing users to interact with lectures without any local installation.

## Overview

- **Source Content**: Synchronized from the [`wasm` branch of lecture-python-intro](https://github.com/QuantEcon/lecture-python-intro/tree/wasm)
- **Build System**: TeachBooks (built on Jupyter Book)
- **Execution**: Pyodide (Python + scientific stack in WebAssembly)
- **Hosting**: GitHub Pages
- **Domain**: interactive.quantecon.org

## Quick Start

### Prerequisites

- Python 3.11 or later
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/QuantEcon/project.lecture-wasm.git
cd project.lecture-wasm

# Install dependencies
pip install -r requirements.txt
```

### Build and Serve Locally

```bash
# Build the book
teachbooks build book

# Serve locally (default: http://localhost:8000)
teachbooks serve

# Stop the server
teachbooks serve stop
```

## Content Management

### Editing Lectures in This Repository

**For most edits**, you can work directly in this repository using the standard GitHub workflow:

1. Create a feature branch: `git checkout -b fix/my-edit`
2. Make your changes to files in `book/` (e.g., `book/long_run_growth.md`)
3. Build and test locally: `teachbooks build book`
4. Commit and push: `git push origin fix/my-edit`
5. Open a Pull Request to merge into `main`
6. Once merged, changes automatically deploy to interactive.quantecon.org

### Synchronizing from Source Repository

This repository mirrors content from the [`wasm` branch of lecture-python-intro](https://github.com/QuantEcon/lecture-python-intro/tree/wasm). The `wasm` branch contains WASM-compatible versions of lectures that exist in the main QuantEcon lecture series.

**When to sync**: Run this when upstream lectures are updated in the source repository:

```bash
python update_lectures.py
```

This script:
- Downloads the latest lectures from the `wasm` branch of `lecture-python-intro`
- Transforms `!pip install` to `%pip install` (WASM-compatible)
- Updates lecture files in the `book/` directory

**Note**: Most contributors should edit files directly in this repo. The sync script is mainly used by maintainers to pull in updates from the broader QuantEcon lecture series.

## Deployment

### GitHub Pages Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

#### Deployment Workflow

1. **Push to main**: Commits trigger the deployment workflow
2. **Build**: GitHub Actions builds the book using TeachBooks
3. **Deploy**: Static HTML is deployed to the `gh-pages` branch
4. **Live**: Changes appear at interactive.quantecon.org

#### Manual Deployment

To trigger a deployment manually:

1. Go to the **Actions** tab on GitHub
2. Select the **Build and Deploy** workflow
3. Click **Run workflow** → Select `main` branch → **Run**

#### Custom Domain Setup

The site is configured to use **interactive.quantecon.org**:

1. **DNS Configuration**: CNAME record pointing to `quantecon.github.io`
2. **Repository Settings**: 
   - Settings → Pages
   - Custom domain: `interactive.quantecon.org`
   - Enforce HTTPS: ✓ Enabled
3. **CNAME file**: Automatically maintained in `gh-pages` branch

#### Deployment Files

- `.github/workflows/deploy.yml` - Production deployment workflow
- `.github/workflows/ci_pr.yml` - PR preview deployment (Netlify)

## Project Structure

```
project.lecture-wasm/
├── book/                    # Lecture content
│   ├── _config.yml         # Book configuration
│   ├── _toc.yml            # Table of contents
│   ├── *.md                # Lecture files (MyST markdown)
│   ├── _static/            # Static assets (CSS, bibliography)
│   ├── datasets/           # Data files
│   └── figures/            # Images
├── .github/
│   └── workflows/          # CI/CD workflows
├── requirements.txt        # Python dependencies
├── update_lectures.py      # Content sync script
└── README.md              # This file
```

## Technology Stack

- **TeachBooks**: Static site generator (extends Jupyter Book)
- **Pyodide**: WebAssembly Python runtime
- **MyST Markdown**: Enhanced markdown for technical content
- **Sphinx**: Documentation engine
- **Thebe-lite**: Browser-based code execution

## Contributing

We welcome contributions! Here's the standard workflow:

1. **Fork** this repository
2. **Create a branch**: `git checkout -b feature/my-improvement`
3. **Make changes** to files in `book/` directory
4. **Test locally**: 
   ```bash
   teachbooks build book
   teachbooks serve
   ```
5. **Commit**: `git commit -m "Description of changes"`
6. **Push**: `git push origin feature/my-improvement`
7. **Open a Pull Request** to merge into `main`

Once your PR is merged, GitHub Actions will automatically deploy the changes to interactive.quantecon.org.

## Troubleshooting

### Build Errors

```bash
# Clean build
rm -rf book/_build
teachbooks build book
```

### Port Already in Use

```bash
# Use a different port
teachbooks serve --port 8080
```

### Package Installation Issues

```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## License

This project is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**. See [LICENSE](LICENSE) for details.

## Authors

- **Thomas J. Sargent** - http://www.tomsargent.com/
- **John Stachurski** - https://johnstachurski.net/

## Links

- **Live Site**: https://interactive.quantecon.org
- **Source Lectures**: https://github.com/QuantEcon/lecture-python-intro/tree/wasm
- **QuantEcon**: https://quantecon.org/
- **Pyodide**: https://pyodide.org/
