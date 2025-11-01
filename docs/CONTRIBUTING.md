# Contributing to QuantEcon WASM Lectures

Thank you for your interest in contributing to the QuantEcon WASM Lectures! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Content Contribution Workflow](#content-contribution-workflow)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
- [WASM Compatibility](#wasm-compatibility)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to the QuantEcon community guidelines. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Browser and OS information**
- **Screenshots** if applicable
- **Console errors** from browser developer tools

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear and descriptive title**
- **Detailed description** of the proposed functionality
- **Rationale** for why this enhancement would be useful
- **Examples** of how it would work

### Content Contributions

Content contributions include:

- Fixing typos or errors in lectures
- Improving explanations or examples
- Adding new exercises or solutions
- Updating outdated references or data

## Content Contribution Workflow

**⚠️ IMPORTANT: Do not edit lecture files directly in this repository!**

This repository is a mirror of content from the main lecture series. To contribute content:

### Step 1: Fork and Edit in the Source Repository

1. Fork the [lecture-python-intro](https://github.com/QuantEcon/lecture-python-intro) repository
2. Create a new branch from `wasm`:
   ```bash
   git checkout wasm
   git checkout -b your-feature-branch
   ```
3. Make your changes to the lecture files
4. Ensure WASM compatibility (see below)
5. Test your changes locally
6. Commit and push to your fork
7. Create a pull request to the `wasm` branch

### Step 2: Sync to This Repository

Once your changes are merged into `lecture-python-intro/wasm`:

1. Fork this repository (lecture-wasm)
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/lecture-wasm.git
   cd lecture-wasm
   ```
3. Run the synchronization script:
   ```bash
   python update_lectures.py
   ```
4. Verify the changes:
   ```bash
   teachbooks build book
   teachbooks serve
   ```
5. Commit and create a pull request

## Development Setup

### Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 18.x or higher
- **pip**: Latest version
- **npm**: Latest version

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/QuantEcon/lecture-wasm.git
   cd lecture-wasm
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies (global):
   ```bash
   npm install -g mystmd thebe-core thebe thebe-lite
   ```

4. Build the lectures:
   ```bash
   teachbooks build book
   ```

5. Serve locally:
   ```bash
   teachbooks serve
   ```

6. Open your browser to the URL shown (typically `http://localhost:8000`)

## Style Guidelines

### MyST Markdown

All lectures use MyST Markdown. Follow these conventions:

#### Code Cells

```markdown
```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt

# Your code here
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.show()
```
```

#### Math Equations

Use LaTeX syntax within dollar signs:

```markdown
Inline math: $f(x) = x^2$

Display math:

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

#### Admonitions

```markdown
```{note}
This is an important note.
```

```{warning}
This requires special attention.
```
```

#### Cross-references

```markdown
See {ref}`section-label` for more details.
```

### Python Code Style

- Follow [PEP 8](https://pep8.org/) conventions
- Use meaningful variable names
- Add comments for complex logic
- Keep code cells focused on one concept
- Use consistent import ordering:
  1. Standard library
  2. Third-party packages
  3. Local imports

Example:

```python
import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from local_module import helper_function
```

### Naming Conventions

- **Files**: Use lowercase with underscores (e.g., `long_run_growth.md`)
- **Functions**: Use lowercase with underscores (e.g., `calculate_mean`)
- **Classes**: Use CamelCase (e.g., `EconomicModel`)
- **Constants**: Use uppercase with underscores (e.g., `MAX_ITERATIONS`)

## WASM Compatibility

### Package Requirements

Only use packages available in Pyodide. Check the [Pyodide package list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).

**Commonly available:**
- numpy
- scipy
- matplotlib
- pandas
- statsmodels
- scikit-learn
- sympy

**NOT available or limited:**
- yfinance
- ortools
- Some packages with C extensions
- Packages requiring system libraries

### Installation in Lectures

Always use `%pip install` (NOT `!pip install`) for WASM compatibility:

```python
%pip install quantecon
```

Never use `--upgrade` flag:

```python
# ❌ Don't do this
%pip install --upgrade quantecon

# ✅ Do this
%pip install quantecon
```

### Testing WASM Compatibility

1. Build and serve locally:
   ```bash
   teachbooks build book
   teachbooks serve
   ```

2. Open the lecture in your browser

3. Try executing all code cells

4. Check browser console for Pyodide errors

5. Verify all imports succeed

## Pull Request Process

### Before Submitting

1. **Test locally**: Ensure all code runs in the browser
2. **Check for errors**: No MyST build errors
3. **Review changes**: Use `git diff` to verify your changes
4. **Update documentation**: If you change functionality
5. **WASM compatibility**: Verify all packages work in Pyodide

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Tested locally with `teachbooks serve`
- [ ] All code cells execute successfully in browser
- [ ] No MyST build errors
- [ ] WASM compatibility verified

## Related Issues
Closes #(issue number)

## Screenshots (if applicable)
```

### Review Process

1. Automated checks will run via GitHub Actions
2. A preview deployment will be created on Netlify
3. Maintainers will review your changes
4. Address any feedback
5. Once approved, changes will be merged

### After Merge

- Your changes will be automatically deployed to GitHub Pages
- Thank you for contributing! 🎉

## Questions?

If you have questions:

- Check existing [Issues](https://github.com/QuantEcon/lecture-wasm/issues)
- Review the [documentation](https://intro.quantecon.org/)
- Open a new issue with the `question` label

## Attribution

By contributing, you agree that your contributions will be licensed under the Creative Commons Attribution 4.0 International License (CC-BY-4.0), the same license as the project.

---

Thank you for helping make QuantEcon lectures better! 🙏
