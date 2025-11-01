"""
Synchronize lectures from the lecture-python-intro repository (wasm branch).

This script downloads and syncs lecture content from the main QuantEcon
lecture-python-intro repository's wasm branch, ensuring WASM compatibility
by transforming pip install commands and fixing MyST directive syntax.

Usage:
    python update_lectures.py

Requirements:
    - gdown: pip install gdown

What it does:
    1. Downloads latest wasm branch content from lecture-python-intro
    2. Extracts and copies lecture files to local lectures/ directory
    3. Transforms content for WASM compatibility:
       - Converts !pip to %pip
       - Removes --upgrade flags
       - Fixes solution/exercise directive syntax
    4. Cleans up temporary files

Author: QuantEcon Development Team
License: CC-BY-4.0
"""

import os
import zipfile
import glob
import shutil

try:
    import gdown
except ImportError:
    print("ERROR: The gdown package is required.")
    print("Install it using: pip install gdown")
    raise

# Source URL for lecture content (wasm branch)
LECTURE_INTRO_URL = "https://github.com/QuantEcon/lecture-python-intro/archive/refs/heads/wasm.zip"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def download_lectures(
    url=None,
    output=None,
    quiet=False,
    unzip=True,
    overwrite=False,
    subfolder=False,
):
    """
    Download lecture folder from GitHub repository.

    Args:
        url (str): URL to download from
        output (str): Output file path
        quiet (bool): Suppress progress messages
        unzip (bool): Extract zip file after download
        overwrite (bool): Overwrite existing files
        subfolder (bool): Extract to subfolder

    Returns:
        str: Absolute path to downloaded/extracted content
    """

    if output is None:
        if isinstance(url, str) and url.startswith("http"):
            output = os.path.basename(url)

    out_dir = os.path.abspath(os.path.dirname(output))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if isinstance(url, str):
        if os.path.exists(os.path.abspath(output)) and (not overwrite):
            print(
                f"{output} already exists. Skip downloading. "
                "Set overwrite=True to overwrite."
            )
            return os.path.abspath(output)

    output = gdown.download(url, output)

    if unzip and output.endswith(".zip"):
        with zipfile.ZipFile(output, "r") as zip_ref:
            if not quiet:
                print("Extracting files...")
            if subfolder:
                basename = os.path.splitext(os.path.basename(output))[0]

                output = os.path.join(out_dir, basename)
                if not os.path.exists(output):
                    os.makedirs(output)
                zip_ref.extractall(output)
            else:
                zip_ref.extractall(os.path.dirname(output))

    return os.path.abspath(output)


def update_pip_line(line):
    """
    Transform line for WASM compatibility.

    Changes:
        - !pip install -> %pip install (Jupyter magic command)
        - Removes --upgrade flags
        - Fixes solution/exercise directive syntax

    Args:
        line (str): Line of text to transform

    Returns:
        str: Transformed line
    """
    line_ = line
    
    # Convert !pip to %pip for WASM/Jupyter compatibility
    if ("!pip" in line_) and ("install" in line_):
        line_ = line_.replace("!", "").replace("pip", "%pip")
        line_ = line_.replace("--upgrade", "")

    # Fix MyST directive syntax for solutions and exercises
    # Convert {solution-start}/{solution-end} to {solution}
    if "```{solution-end}" or "```{solution-start}" in line_:
        line_ = line_.replace("```{solution-end}", "```{solution}")
        line_ = line_.replace("```{solution-start}", "```{solution}")
    elif "```{exercise-end}" or "```{exercise-start}" in line_:
        line_ = line_.replace("```{exercise-end}", "```{exercise}")
        line_ = line_.replace("```{exercise-start}", "```{exercise}")
    
    return line_


def update_lectures():
    """
    Main function to sync lectures from source repository.

    Process:
        1. Download latest content from wasm branch
        2. Extract to temporary directory
        3. Copy lecture files to lectures/ directory
        4. Transform all .md files for WASM compatibility
        5. Clean up temporary files

    Raises:
        Exception: If download or file operations fail
    """
    print("=" * 60)
    print("QuantEcon WASM Lectures - Content Sync")
    print("=" * 60)
    print(f"Source: {LECTURE_INTRO_URL}")
    print()

    # Download and extract lectures
    out_zip = 'qe-lecture-intro-wasm.zip'
    print("Downloading lectures...")
    out_zip = download_lectures(LECTURE_INTRO_URL, out_zip)

    # Define source and destination directories
    in_dir_1 = os.path.abspath(os.path.join(ROOT_DIR, 'lecture-python-intro-wasm'))
    in_dir_2 = os.path.abspath(os.path.join(in_dir_1, 'lectures'))
    out_dir = os.path.abspath(os.path.join(ROOT_DIR, 'lectures'))

    print(f"Copying files from: {in_dir_2}")
    print(f"              to: {out_dir}")
    print()

    # Copy directory tree, overwriting existing files
    shutil.copytree(in_dir_2, out_dir, dirs_exist_ok=True)
    
    # Get current working directory
    cwd = os.getcwd()
    os.chdir(cwd)

    # Get all markdown lecture files
    lectures = glob.glob(os.path.abspath(os.path.join(out_dir, '*.md')))
    
    print(f"Processing {len(lectures)} lecture files...")

    # Update each lecture file for WASM compatibility
    for file in lectures:
        base_name = os.path.basename(file)
        
        # Read file content
        with open(file, 'r') as f:
            lines = f.readlines()

        # Transform each line
        out_lines = []
        for index, line in enumerate(lines):
            line_ = update_pip_line(line)
            out_lines.append(line_)

        # Write transformed content back
        with open(file, 'w') as f:
            f.writelines(out_lines)
        
        print(f"  ✓ Processed: {base_name}")

    print()
    print("Cleaning up temporary files...")
    
    # Remove downloaded folder and zip file
    shutil.rmtree('lecture-python-intro-wasm')
    os.remove(out_zip)
    
    print()
    print("=" * 60)
    print("✓ Sync completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Review changes: git diff")
    print("  2. Test locally: teachbooks build book && teachbooks serve")
    print("  3. Commit changes: git add lectures/ && git commit")
    print()


if __name__ == '__main__':
    try:
        update_lectures()
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ ERROR: Sync failed!")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Please check:")
        print("  - Internet connection")
        print("  - gdown package is installed (pip install gdown)")
        print("  - Write permissions in current directory")
        print()
        raise