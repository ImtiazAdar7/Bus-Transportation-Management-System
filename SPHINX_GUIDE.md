# Sphinx Documentation Generation Guide

This guide will help you generate automatic documentation for the Bus Transportation Management System using Sphinx.

## Prerequisites

1. **Install Sphinx and required extensions:**
   ```bash
   pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
   ```

2. **Verify installation:**
   ```bash
   sphinx-build --version
   ```

## Step 1: Initialize Sphinx Documentation

1. **Navigate to your project root directory:**
   ```bash
   cd F:\gith\Bus-Transportation-Management-System-main
   ```

2. **Create a `docs` directory:**
   ```bash
   mkdir docs
   cd docs
   ```

3. **Run Sphinx Quickstart:**
   ```bash
   sphinx-quickstart
   ```

   When prompted, use these settings:
   - **Separate source and build directories:** `y` (yes)
   - **Name prefix for templates and static files:** `_` (default)
   - **Project name:** `Bus Transportation Management System`
   - **Author name(s):** `Your Name`
   - **Project release:** `1.0.0`
   - **Project language:** `en` (English)
   - **Source file suffix:** `.rst` (default)
   - **Master document:** `index` (default)
   - **Use epub builder:** `n` (no, unless you need it)
   - **autodoc:** `y` (yes - IMPORTANT!)
   - **doctest:** `y` (yes)
   - **intersphinx:** `y` (yes)
   - **todo:** `y` (yes)
   - **coverage:** `y` (yes)
   - **imgmath:** `n` (no, unless you need math)
   - **mathjax:** `n` (no, unless you need math)
   - **ifconfig:** `y` (yes)
   - **viewcode:** `y` (yes - shows source code)
   - **githubpages:** `n` (no)

## Step 2: Configure Sphinx

1. **Edit `docs/source/conf.py`** and make the following changes:

   **Add the project root to the Python path:**
   ```python
   import os
   import sys
   sys.path.insert(0, os.path.abspath('../..'))
   ```

   **Update the extensions list:**
   ```python
   extensions = [
       'sphinx.ext.autodoc',
       'sphinx.ext.viewcode',
       'sphinx.ext.todo',
       'sphinx.ext.coverage',
       'sphinx.ext.intersphinx',
       'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
       'sphinx_autodoc_typehints',  # For type hints
   ]
   ```

   **Set the theme (optional, but recommended):**
   ```python
   html_theme = 'sphinx_rtd_theme'
   ```

   **Configure Napoleon settings (for docstring parsing):**
   ```python
   napoleon_google_docstring = True
   napoleon_numpy_docstring = True
   napoleon_include_init_with_doc = False
   napoleon_include_private_with_doc = False
   napoleon_include_special_with_doc = True
   napoleon_use_admonition_for_examples = False
   napoleon_use_admonition_for_notes = False
   napoleon_use_admonition_for_references = False
   napoleon_use_ivar = False
   napoleon_use_param = True
   napoleon_use_rtype = True
   napoleon_preprocess_types = False
   napoleon_type_aliases = None
   napoleon_attr_annotations = True
   ```

## Step 3: Create Documentation Structure

1. **Create `docs/source/index.rst`** (or edit the existing one):

   ```rst
   Bus Transportation Management System Documentation
   ===================================================

   Welcome to the Bus Transportation Management System documentation!

   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      modules
      controllers
      models
      routes

   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
   ```

2. **Create `docs/source/modules.rst`:**

   ```rst
   Modules
   =======

   .. automodule:: app
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: config
      :members:
      :undoc-members:
      :show-inheritance:
   ```

3. **Create `docs/source/controllers.rst`:**

   ```rst
   Controllers
   ===========

   .. automodule:: controllers.admin_controllers
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: controllers.passenger_controller
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: controllers.driver_controllers
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: controllers.route_controller
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: controllers.analytics_controller
      :members:
      :undoc-members:
      :show-inheritance:
   ```

4. **Create `docs/source/models.rst`:**

   ```rst
   Models
   ======

   .. automodule:: models.admin_model
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: models.passenger_model
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: models.driver_model
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: models.booking_model
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: models.bus_route_model
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: models.assigned_driver_model
      :members:
      :undoc-members:
      :show-inheritance:
   ```

5. **Create `docs/source/routes.rst`:**

   ```rst
   Routes
   ======

   .. automodule:: routes.passenger_routes
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: routes.admin_routes
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: routes.driver_routes
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: routes.route_routes
      :members:
      :undoc-members:
      :show-inheritance:

   .. automodule:: routes.analytics_routes
      :members:
      :undoc-members:
      :show-inheritance:
   ```

## Step 4: Generate Documentation

1. **From the `docs` directory, build the HTML documentation:**
   ```bash
   cd docs
   sphinx-build -b html source build
   ```

   Or use the Makefile (on Linux/Mac):
   ```bash
   make html
   ```

   On Windows, you can create a `make.bat` file or use:
   ```bash
   sphinx-build -b html source build
   ```

2. **View the documentation:**
   Open `docs/build/html/index.html` in your web browser.

## Step 5: Auto-generate Documentation (Recommended)

Instead of manually creating `.rst` files, you can use `sphinx-apidoc`:

1. **From the project root, run:**
   ```bash
   sphinx-apidoc -o docs/source .
   ```

   This will automatically generate `.rst` files for all Python modules.

2. **Then build the documentation:**
   ```bash
   cd docs
   sphinx-build -b html source build
   ```

## Step 6: Update Documentation

Whenever you make changes to your code:

1. **Regenerate the API documentation (if using sphinx-apidoc):**
   ```bash
   sphinx-apidoc -f -o docs/source .
   ```
   (The `-f` flag forces overwriting existing files)

2. **Rebuild the HTML:**
   ```bash
   cd docs
   sphinx-build -b html source build
   ```

## Step 7: Create a Build Script (Optional)

Create a `build_docs.bat` file (Windows) or `build_docs.sh` (Linux/Mac) in your project root:

**Windows (`build_docs.bat`):**
```batch
@echo off
echo Generating Sphinx documentation...
sphinx-apidoc -f -o docs/source .
cd docs
sphinx-build -b html source build
echo Documentation built successfully!
echo Open docs\build\html\index.html in your browser.
pause
```

**Linux/Mac (`build_docs.sh`):**
```bash
#!/bin/bash
echo "Generating Sphinx documentation..."
sphinx-apidoc -f -o docs/source .
cd docs
sphinx-build -b html source build
echo "Documentation built successfully!"
echo "Open docs/build/html/index.html in your browser."
```

## Additional Tips

1. **Include README in documentation:**
   Add to `index.rst`:
   ```rst
   .. include:: ../../README.md
      :parser: myst_parser
   ```
   (Requires `myst-parser` package)

2. **Add custom pages:**
   Create `.rst` files in `docs/source/` and add them to the `toctree` in `index.rst`.

3. **Customize the theme:**
   Edit `docs/source/conf.py` to change colors, logos, etc.

4. **Generate PDF documentation:**
   ```bash
   sphinx-build -b latex source build
   cd build
   make latexpdf
   ```

5. **Generate EPUB:**
   ```bash
   sphinx-build -b epub source build
   ```

## Troubleshooting

- **Import errors:** Make sure the project root is in `sys.path` in `conf.py`
- **Missing modules:** Check that all Python files have proper `__init__.py` files
- **Docstring not showing:** Ensure docstrings follow Google or NumPy style
- **Type hints not showing:** Install `sphinx-autodoc-typehints` and add to extensions

## Quick Reference Commands

```bash
# Generate API documentation
sphinx-apidoc -f -o docs/source .

# Build HTML documentation
cd docs && sphinx-build -b html source build

# Build PDF documentation
cd docs && sphinx-build -b latex source build && cd build && make latexpdf

# Clean build directory
cd docs && sphinx-build -b html -E source build  # -E forces rebuild
```

## Next Steps

1. Run `sphinx-quickstart` in a `docs` directory
2. Configure `conf.py` as shown above
3. Run `sphinx-apidoc` to auto-generate documentation files
4. Build with `sphinx-build`
5. View your documentation in `docs/build/html/index.html`

Your documentation will automatically include all the docstrings you've added to your functions!

