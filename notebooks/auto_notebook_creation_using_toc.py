import os
import nbformat
import yaml

# Path to your _toc.yml
TOC_FILE = "_toc.yml"

# Where to create notebooks (can be same as where _toc.yml is)
OUTPUT_DIR = "."

# Template notebook content
def make_notebook(title):
    nb = nbformat.v4.new_notebook()
    nb["cells"] = [
        nbformat.v4.new_markdown_cell(f"# {title}"),
        nbformat.v4.new_code_cell("# Your code here")
    ]
    return nb

def create_notebook(path, title):
    """Create an .ipynb file if it doesn't exist."""
    if not path.endswith(".ipynb"):
        path += ".ipynb"
    full_path = os.path.join(OUTPUT_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    if not os.path.exists(full_path):
        nb = make_notebook(title)
        with open(full_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"Created: {full_path}")
    else:
        print(f"Exists:  {full_path}")

def process_entry(entry):
    """Recursively process toc entries."""
    if isinstance(entry, dict):
        if "file" in entry:
            title = entry.get("title", entry["file"])
            create_notebook(entry["file"], title)
        if "sections" in entry:
            for sec in entry["sections"]:
                process_entry(sec)
    elif isinstance(entry, list):
        for e in entry:
            process_entry(e)

def main():
    with open(TOC_FILE, "r", encoding="utf-8") as f:
        toc = yaml.safe_load(f)

    if "root" in toc:
        create_notebook(toc["root"], toc.get("title", toc["root"]))

    if "chapters" in toc:
        process_entry(toc["chapters"])

if __name__ == "__main__":
    main()
