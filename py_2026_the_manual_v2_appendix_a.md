## Appendix A: Retrospective Git-ification (Legacy Upgrades)
*The "Clean Upgrade" path for transitioning loose, legacy Python scripts into professional, version-controlled, and `uv`-managed repositories.*

### A.1 Environment Standardisation & `uv` Initialisation
Before applying version control, the environment must be modernised to ensure reproducibility.
1. **Navigate to the legacy folder** in PowerShell.
2. **Initialise the Engine:** Run `uv init`. *(Note: This automatically creates a `pyproject.toml`, a default `.gitignore`, a `.git` tracking folder, and a `hello.py` file).*
3. **Clean Up & Lock Dependencies:** 
   * Delete the auto-generated `hello.py` file.
   * Run `uv add rich` (mandatory for CLI formatting).
   * Run `uv add <library>` for every external dependency your legacy script uses (e.g., `requests`, `pandas`).

### A.2 Code & Configuration Hygiene
Prepare the legacy code to meet modern architectural standards.

**1. The Mandatory Boilerplate:** Open your legacy script and insert this exact header to standardize path resolution:
```python
import os
import glob
from pathlib import Path

# Absolute paths for environment stability
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure output directory exists gracefully
OUTPUT_DIR.mkdir(exist_ok=True)
```

**2. Refactor I/O (Drop-and-Go):** If the legacy script hardcodes input filenames, refactor it to automatically pick the newest file from the `input/` folder using this standard:
```python
input_files = glob.glob(str(INPUT_DIR / "*.*"))
if not input_files:
    print("[Error] No files found in input/ directory.")
    import sys
    sys.exit(1)
latest_file = max(input_files, key=os.path.getmtime)
```

**3. Environment Variables:** Create a `.env` file for API keys or private system paths. Create a `.env.example` file. Replace hardcoded sensitive strings in the script with `os.getenv("VAR_NAME")`.

**4. The Gatekeeper:** Overwrite the default `uv` generated `.gitignore`. Ensure `.env`, `__pycache__/`, `.venv/`, and legacy data folders are explicitly ignored.

### A.3 Metadata & Language Statistics
Ensure the repository is correctly identified by its primary logic (Python) rather than being skewed by legacy data outputs.
* **Implement `.gitattributes`:** Create this file in the root directory and map data-heavy exports or HTML snapshots as documentation.
```text
# .gitattributes
markdown_exports/* linguist-documentation
*.html linguist-documentation
```

### A.4 The Foundational Git Pivot (Remote & Branching)
Ensure the local git state aligns with modern repository standards.
1. **Promote the Branch:** Ensure the primary branch is named `main`.
```powershell
git branch -M main
```
2. **Remote Bifurcation (If applicable):** If this legacy folder *already* had a messy remote connection that you wish to preserve as an archive:
```powershell
git remote rename origin legacy
git remote add origin https://github.com/[username]/[new-repo].git
```

### A.5 The Professional Commit & Tag
Establish the new "Golden State" with a highly descriptive commit that follows the **50/72 rule**, tag it, and push.

1. **Stage files:** `git add .`
2. **Commit:** Run `git commit` (which opens your VS Code editor) and paste this exact template:
```text
feat: Modernise legacy project with uv and Git

Architecture & Environment:
- Initialised uv for strict dependency and environment management.
- Implemented .env for hardcoded path and credential isolation.
- Standardised primary branch to 'main'.

Hygiene & Metadata:
- Added strict .gitignore for environment and local data protection.
- Added .gitattributes to correct repository language statistics.
- Refactored script I/O to use standard pathlib routing.
```
3. **Tag and Push:**
```powershell
git tag -a v1.0.0 -m "Modernised legacy codebase into standard uv architecture"
git push -u origin main --follow-tags
```

***