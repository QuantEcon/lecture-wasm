# Project Architecture

## Overview

This document describes the architecture of the QuantEcon WASM Lectures project, explaining how different components work together to deliver browser-based interactive Python lectures.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User's Browser                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    JupyterLite Interface                    │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │ │
│  │  │   MyST HTML  │  │    Thebe     │  │   Pyodide    │     │ │
│  │  │   Content    │  │  (Execution) │  │   Kernel     │     │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Pages / CDN                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Static HTML, CSS, JS, and WASM files                      │ │
│  │  • Lecture content (HTML)                                  │ │
│  │  • Pyodide runtime (WASM)                                  │ │
│  │  • Python packages (wheels)                                │ │
│  │  • Thebe and JupyterLite assets                           │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              │ GitHub Actions Deploy
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      Build Pipeline (CI/CD)                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  GitHub Actions Workflow                                   │ │
│  │  1. Checkout source                                        │ │
│  │  2. Install Node.js & MyST CLI                            │ │
│  │  3. Build MyST HTML                                       │ │
│  │  4. Upload artifacts                                       │ │
│  │  5. Deploy to GitHub Pages                                │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              │ Content Sync
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    Source Repository                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  lecture-python-intro (wasm branch)                        │ │
│  │  • Original lecture content                                │ │
│  │  • MyST Markdown files                                     │ │
│  │  • Datasets and assets                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Content Layer (MyST Markdown)

**Location:** `lectures/*.md`

**Purpose:** Stores lecture content in MyST Markdown format

**Key Features:**
- Executable code cells marked with `` ```{code-cell} ipython3 ``
- Rich formatting with MyST directives
- Cross-references and citations
- Embedded exercises and solutions

**Example:**
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

```{code-cell} ipython3
import numpy as np
print("Hello from WASM!")
```
```

### 2. Build System

#### MyST CLI (`mystmd`)

**Purpose:** Converts MyST Markdown to executable HTML

**Key Responsibilities:**
- Parse MyST syntax
- Generate HTML output
- Integrate JupyterLite configuration
- Process cross-references and citations
- Handle static assets

**Commands:**
- `myst build --html` - Build HTML output
- `myst start` - Start local development server

**Note:** The project previously used `teachbooks` (a wrapper around Jupyter Book) but migrated to native `mystmd` in October 2025 for better MyST integration and performance.

### 3. Runtime Layer

#### Pyodide

**What:** Python interpreter compiled to WebAssembly

**Purpose:** Execute Python code entirely in the browser

**Key Features:**
- Full CPython 3.11 implementation
- Access to numpy, scipy, matplotlib, pandas, etc.
- No server required
- Runs entirely client-side

**Limitations:**
- Package availability (not all PyPI packages work)
- No file system access (virtual file system)
- Performance overhead vs native Python
- Limited threading support

#### JupyterLite

**What:** Browser-based Jupyter environment

**Purpose:** Provide notebook-like interface in the browser

**Components:**
- **Pyodide kernel**: Python execution backend
- **JupyterLab interface**: Optional full IDE
- **Content management**: Virtual file system

**Configuration:** `lectures/myst.yml`
```yaml
jupyter:
  lite: true
```

#### Thebe

**What:** JavaScript library for executable code cells

**Purpose:** Enable code execution in MyST HTML pages

**How it works:**
1. Identifies code cells in HTML
2. Connects to JupyterLite/Pyodide kernel
3. Sends code for execution
4. Displays output inline

### 4. CI/CD Pipeline

#### GitHub Actions Workflow

**File:** `.github/workflows/ci.yml`

**Triggers:**
- Push to `main` branch
- Pull request creation/update
- Manual workflow dispatch

**Jobs:**

##### Build Job
```yaml
- Checkout repository
- Setup Node.js 18.x
- Install MyST CLI and Thebe
- Build HTML (with appropriate base URL)
- Upload artifacts
```

##### Deploy Job (main branch)
```yaml
- Deploy to GitHub Pages
- Available at: quantecon.github.io/lecture-wasm
```

##### Preview Job (PRs)
```yaml
- Deploy to Netlify
- Create preview URL (pr-{number}.netlify.app)
- Post comment on PR with preview link
```

### 5. Content Synchronization

#### Update Script

**File:** `update_lectures.py`

**Purpose:** Sync content from source repository

**Process:**
1. Download latest ZIP from `lecture-python-intro/wasm` branch
2. Extract to temporary directory
3. Copy lecture files to `lectures/` directory
4. Transform content:
   - `!pip install` → `%pip install`
   - Remove `--upgrade` flags
   - Fix MyST directive syntax
5. Clean up temporary files

**Usage:**
```bash
python update_lectures.py
```

**Key Function:**
```python
def update_pip_line(line):
    # Convert !pip to %pip for WASM compatibility
    if ("!pip" in line_) and ("install" in line_):
        line_ = line_.replace("!", "").replace("pip", "%pip")
        line_ = line_.replace("--upgrade", "")
    return line_
```

## Data Flow

### Build Time

```
1. Source Content (lecture-python-intro/wasm)
   ↓ [update_lectures.py]
2. Local Content (lectures/*.md)
   ↓ [myst build --html]
3. HTML Output (lectures/_build/html/)
   ↓ [GitHub Actions]
4. GitHub Pages / Netlify
```

### Runtime (User Visit)

```
1. User requests page
   ↓
2. CDN serves static HTML/CSS/JS
   ↓
3. Browser loads Pyodide WASM runtime
   ↓
4. Thebe initializes JupyterLite kernel
   ↓
5. User clicks "Run" on code cell
   ↓
6. Thebe sends code to Pyodide kernel
   ↓
7. Python executes in browser (WASM)
   ↓
8. Output rendered inline in HTML
```

## Configuration Files

### `lectures/myst.yml`

**Purpose:** Main MyST project configuration

**Key Sections:**

```yaml
project:
  title: Project title
  authors: [...]
  github: Repository URL
  jupyter:
    lite: true  # Enable JupyterLite

site:
  template: Theme URL

toc:
  - file: intro.md
  - title: Section
    children:
      - file: lecture1.md
      - file: lecture2.md
```

### `requirements.txt`

**Purpose:** Legacy Python dependencies (no longer required for builds)

**Note:** This file contains dependencies from the old `teachbooks`/`jupyter-book` build system. The project now uses `mystmd` which only requires Node.js dependencies. This file is kept for historical reference but is not used in the current build process.

**Historical Contents:**
- `teachbooks` - Old build tool (replaced by mystmd)
- `jupyterbook-patches` - QuantEcon-specific patches
- `sphinx-*` extensions - Various Sphinx extensions

**Current Build Dependencies:** Only Node.js packages are required:
```bash
npm install -g mystmd thebe-core thebe thebe-lite
```

### `.gitignore`

**Purpose:** Exclude build artifacts and temporary files

**Key Exclusions:**
- `_build/` - Build output
- `.teachbooks/` - Teachbooks cache
- `*.doit.db` - Build database
- Python bytecode and cache

## Deployment Environments

### Production (GitHub Pages)

- **URL:** https://quantecon.github.io/lecture-wasm/
- **Trigger:** Push to `main` branch
- **Base URL:** `/lecture-wasm`
- **CDN:** GitHub's CDN

### Preview (Netlify)

- **URL:** `https://deploy-preview-{PR#}--{site}.netlify.app`
- **Trigger:** Pull request
- **Base URL:** `/`
- **Features:** PR comments with preview links

## Package Management

### Build-time (Node.js)

```bash
npm install -g mystmd thebe-core thebe thebe-lite
```

**Purpose:** Build tools and frontend libraries

**Components:**
- `mystmd` - MyST Markdown build system
- `thebe-core` - Core Thebe functionality
- `thebe` - Executable code cells
- `thebe-lite` - JupyterLite integration

### Build-time (Python) - DEPRECATED

The `requirements.txt` file is legacy from the old `teachbooks` build system and is no longer required. All build dependencies are now Node.js-based.

### Runtime (Pyodide)

Packages are loaded from Pyodide CDN when needed:
- Pre-built wheels for common packages
- Downloaded on-demand in browser
- Cached by browser after first load

**Installation in lectures:**
```python
%pip install quantecon
```

## Security Considerations

### Client-side Execution

- All Python code runs in browser sandbox
- No server-side execution
- No access to user's file system (virtual FS only)
- Safe for untrusted code execution

### Static Assets

- All content served as static files
- No dynamic server-side processing
- CDN caching for performance
- HTTPS enforced

### Dependencies

- Pyodide packages from official CDN
- npm packages from registry
- Python packages from TU Delft registry (verified)

## Performance Characteristics

### Initial Load

- **First visit:** 5-15 seconds (Pyodide download)
- **Return visit:** <2 seconds (browser cache)
- **Pyodide size:** ~30 MB (compressed)

### Code Execution

- **Startup:** 1-3 seconds (kernel initialization)
- **Simple operations:** Near-native speed
- **NumPy/SciPy:** 2-5x slower than native
- **Matplotlib:** First plot slower, subsequent faster

### Optimization Strategies

1. **Lazy loading:** Pyodide loads only when needed
2. **Package caching:** Browser caches downloaded packages
3. **Code splitting:** Load packages on-demand
4. **CDN delivery:** Fast content delivery globally

## Development Workflow

### Local Development Cycle

```bash
# 1. Sync content (if needed)
python update_lectures.py

# 2. Navigate to lectures directory
cd lectures

# 3. Build
myst build --html

# 4. Serve
myst start

# 5. Test in browser
# Visit http://localhost:3000

# 6. Make changes (in source repo)
# 7. Repeat from step 1
```

### CI/CD Cycle

```
1. Create PR
   ↓
2. GitHub Actions builds
   ↓
3. Deploy to Netlify preview
   ↓
4. Review preview
   ↓
5. Merge PR
   ↓
6. Deploy to GitHub Pages
```

## Troubleshooting Architecture

### Build Failures

**Check:**
1. MyST syntax errors in markdown
2. Node.js version (must be 18.x)
3. Missing dependencies
4. Invalid cross-references

### Runtime Failures

**Check:**
1. Browser console for Pyodide errors
2. Package availability in Pyodide
3. WASM support in browser
4. Network connectivity (for package downloads)

### Deployment Issues

**Check:**
1. GitHub Actions logs
2. Secrets configuration (NETLIFY_*)
3. GitHub Pages settings
4. Base URL configuration

## Future Enhancements

Potential architectural improvements:

1. **Service Worker:** Offline support
2. **WebWorkers:** Background computation
3. **IndexedDB:** Persistent storage
4. **Progressive Web App:** Install to desktop
5. **CDN optimization:** Custom CDN for Pyodide packages

---

For questions about this architecture, please open an issue on GitHub.
