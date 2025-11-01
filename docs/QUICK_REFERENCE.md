# Quick Reference Guide

Quick commands and solutions for common tasks in the QuantEcon WASM Lectures project.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/QuantEcon/lecture-wasm.git
cd lecture-wasm
pip install -r requirements.txt

# Build and serve
teachbooks build book
teachbooks serve
```

## 📝 Common Commands

### Building

```bash
# Full build
teachbooks build book

# Build with MyST directly
cd lectures
myst build --html

# Clean build (remove cache)
rm -rf lectures/_build
teachbooks build book
```

### Local Development

```bash
# Start server
teachbooks serve

# Server will typically run on http://localhost:8000

# Stop server
teachbooks serve stop

# Check if server is running
ps aux | grep teachbooks
```

### Content Sync

```bash
# Sync from source repository
python update_lectures.py

# This downloads from:
# https://github.com/QuantEcon/lecture-python-intro/tree/wasm
```

## 🔧 Troubleshooting

### Build Issues

**Problem:** MyST build fails with syntax error

```bash
# Check specific file syntax
cd lectures
myst build --html 2>&1 | grep -A 5 "error"

# Validate a single file
myst build filename.md --html
```

**Problem:** Missing dependencies

```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# Update npm packages
npm install -g mystmd@latest thebe-core thebe thebe-lite
```

**Problem:** Port already in use

```bash
# Find process using port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port (if supported)
teachbooks serve --port 8080
```

### Runtime Issues

**Problem:** Code cells not executing in browser

1. Open browser DevTools (F12)
2. Check Console for errors
3. Common issues:
   - Pyodide failed to load
   - Package not available in WASM
   - Network blocking Pyodide CDN

**Problem:** Package import fails in browser

```python
# Check if package is available in Pyodide
# Visit: https://pyodide.org/en/stable/usage/packages-in-pyodide.html

# Try micropip to install from PyPI
import micropip
await micropip.install('package-name')
```

### Git Issues

**Problem:** Merge conflicts after sync

```bash
# Reset to match remote
git fetch origin
git reset --hard origin/main

# Re-run sync
python update_lectures.py
```

## 📚 File Locations

### Key Files

```
Configuration:
  lectures/myst.yml           # MyST config
  requirements.txt            # Python dependencies
  .github/workflows/ci.yml    # CI/CD pipeline

Content:
  lectures/*.md               # Lecture files
  lectures/_static/           # Static assets
  lectures/datasets/          # Data files

Build Output:
  lectures/_build/html/       # Generated HTML
  lectures/.teachbooks/       # Build cache

Documentation:
  README.md                   # Main documentation
  CONTRIBUTING.md             # Contribution guide
  .github/ARCHITECTURE.md     # System architecture
```

### Important URLs

```
Production:      https://quantecon.github.io/lecture-wasm/
Source Repo:     https://github.com/QuantEcon/lecture-python-intro
Source Branch:   https://github.com/QuantEcon/lecture-python-intro/tree/wasm
This Repo:       https://github.com/QuantEcon/lecture-wasm
Issues:          https://github.com/QuantEcon/lecture-wasm/issues
```

## 🎨 MyST Syntax Quick Reference

### Code Cells

```markdown
```{code-cell} ipython3
import numpy as np
print(np.pi)
```
```

### Math

```markdown
Inline: $E = mc^2$

Display:
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

### Admonitions

```markdown
```{note}
Important information
```

```{warning}
Caution required
```

```{tip}
Helpful suggestion
```

```{exercise}
:label: ex-label
Exercise content
```

```{solution} ex-label
:class: dropdown
Solution content
```
```

### Cross-references

```markdown
See {ref}`section-label` for details.

As shown in {eq}`equation-label`.

{cite}`AuthorYear` discusses this.
```

### Figures

```markdown
```{figure} path/to/image.png
:name: fig-label
:width: 80%

Caption text here
```
```

## 🔍 Searching and Finding

### Find text in lectures

```bash
# Search all lectures
grep -r "search term" lectures/*.md

# Case-insensitive search
grep -ri "search term" lectures/*.md

# Search with context
grep -C 3 "search term" lectures/*.md
```

### Find specific MyST elements

```bash
# Find all code cells
grep -n "code-cell" lectures/*.md

# Find all exercises
grep -n "{exercise}" lectures/*.md

# Find all math blocks
grep -n "\$\$" lectures/*.md
```

## 🧪 Testing

### Test Single Lecture

```bash
# Build single file
cd lectures
myst build intro.md --html

# Check for errors
myst build intro.md --html 2>&1 | grep -i error
```

### Test WASM Compatibility

```bash
# 1. Build and serve
teachbooks build book
teachbooks serve

# 2. Open in browser
# 3. Open DevTools Console (F12)
# 4. Try running code cells
# 5. Check console for errors
```

### Validate Links

```bash
# Check for broken internal links (requires linkchecker)
pip install linkchecker
linkchecker http://localhost:8000
```

## 📦 Package Management

### Check Package Availability

```python
# In browser console (after Pyodide loads)
import pyodide_js
print(pyodide_js.loadedPackages)
```

### Install Packages in Lectures

```python
# Correct way (WASM compatible)
%pip install quantecon

# WRONG - don't use these
!pip install quantecon          # ❌
!pip install --upgrade quantecon # ❌
```

## 🔄 Update Workflow

### Update from Source (Recommended)

```bash
# 1. Update source repository first
# (In lecture-python-intro/wasm branch)

# 2. Sync to this repository
python update_lectures.py

# 3. Test locally
teachbooks build book
teachbooks serve

# 4. Commit and push
git add lectures/
git commit -m "Sync lectures from source"
git push
```

### Emergency Direct Edit (Not Recommended)

```bash
# Only for urgent fixes!
# Edit files in lectures/

# Build and test
teachbooks build book
teachbooks serve

# Commit
git add lectures/modified-file.md
git commit -m "Hotfix: description"
git push

# IMPORTANT: Update source repository ASAP
# to avoid losing changes on next sync!
```

## 🚨 Emergency Procedures

### Rollback to Previous Version

```bash
# Find commit to rollback to
git log --oneline

# Reset to specific commit
git reset --hard COMMIT_HASH

# Force push (use with caution!)
git push --force
```

### Clear All Build Artifacts

```bash
# Remove all build outputs
rm -rf lectures/_build
rm -rf lectures/.teachbooks
rm -f lectures/*.doit.db

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Rebuild from scratch
teachbooks build book
```

### Fix Corrupted Sync

```bash
# Remove downloaded content
rm -rf lecture-python-intro-wasm
rm -f qe-lecture-intro-wasm.zip

# Re-run sync
python update_lectures.py
```

## 📊 Monitoring

### Check Build Size

```bash
# Size of build output
du -sh lectures/_build/html/

# Size by component
du -h lectures/_build/html/ | sort -rh | head -20
```

### Check Build Time

```bash
# Time the build
time teachbooks build book
```

### Monitor CI/CD

```bash
# View GitHub Actions status
gh run list

# View specific run
gh run view RUN_ID

# Watch run in real-time
gh run watch
```

## 🛠️ Development Tools

### Recommended VS Code Extensions

- MyST Markdown
- Python
- YAML
- GitHub Actions
- GitLens

### Browser Extensions for Testing

- React DevTools (for debugging Thebe)
- Vue DevTools (for MyST)

### CLI Tools

```bash
# Install useful tools
pip install linkchecker        # Check links
pip install pycodestyle         # Python style
npm install -g markdownlint-cli # Markdown linting
```

## 💡 Tips and Tricks

### Speed Up Builds

```bash
# Build only changed files (if supported)
teachbooks build book --incremental

# Use parallel builds (if available)
teachbooks build book --jobs 4
```

### Preview on Mobile

```bash
# Get local IP
ipconfig getifaddr en0  # macOS
hostname -I             # Linux

# Start server
teachbooks serve

# Access from mobile
# http://YOUR_IP:8000
```

### Debug MyST Rendering

```bash
# Increase verbosity
export MYST_LOG_LEVEL=DEBUG
myst build --html

# Check intermediate AST
myst build --export md-ast
```

## 🔗 Useful Links

- [MyST Documentation](https://mystmd.org/)
- [Pyodide Packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)
- [JupyterLite Docs](https://jupyterlite.readthedocs.io/)
- [Teachbooks](https://teachbooks.io/)
- [QuantEcon](https://quantecon.org/)

---

**Need more help?** Open an issue: https://github.com/QuantEcon/lecture-wasm/issues
