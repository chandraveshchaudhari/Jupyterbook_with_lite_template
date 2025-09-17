import os
import re
import yaml

# Paths
toc_path = "notebooks/_toc.yml"
notebooks_dir = "notebooks"
html_dir = "docs"

# Step 1: Read TOC file
with open(toc_path, "r", encoding="utf-8") as f:
    toc_data = yaml.safe_load(f)

toc_files = []

def extract_files(entries):
    """Extract all 'file' entries from TOC, ignoring extension for now."""
    for item in entries:
        if isinstance(item, dict):
            if "file" in item:
                toc_files.append(os.path.basename(item["file"]))
            if "sections" in item:
                extract_files(item["sections"])
        elif isinstance(item, list):
            extract_files(item)

if "chapters" in toc_data:
    extract_files(toc_data["chapters"])
elif "parts" in toc_data:
    for part in toc_data["parts"]:
        if "chapters" in part:
            extract_files(part["chapters"])

# Step 2: Match only actual notebook files from directory
valid_notebooks = []
for name in toc_files:
    no_ext, _ = os.path.splitext(name)
    ipynb_path = os.path.join(notebooks_dir, no_ext + ".ipynb")
    if os.path.exists(ipynb_path):
        valid_notebooks.append(no_ext)

print(f"📚 Valid notebooks from TOC: {valid_notebooks}")

# Step 3: Regex to find Colab button
colab_regex = re.compile(
    r'(<a[^>]+href="https://colab\.research\.google\.com/[^"]+/(?P<filename>[^/"]+\.ipynb)"[^>]*>.*?</a>)',
    re.DOTALL
)

# Step 4: JupyterLite button template
jupyterlite_template = """
<li>
  <a href="https://chandraveshchaudhari.github.io/BusinessML_web/jupyterlite/lab/index.html?path={filename}" target="_blank"
     class="btn btn-sm dropdown-item"
     title="Launch on JupyterLite"
     data-bs-placement="left" data-bs-toggle="tooltip">
    <span class="btn__icon-container" style="display:inline-block; width:20px; height:20px;">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
        <circle cx="128" cy="128" r="128" fill="#f37726"/>
        <ellipse cx="128" cy="128" rx="110" ry="40" fill="white" transform="rotate(-25, 128, 128)"/>
        <ellipse cx="128" cy="128" rx="110" ry="40" fill="white" transform="rotate(25, 128, 128)"/>
        <circle cx="200" cy="60" r="18" fill="white"/>
        <circle cx="60" cy="200" r="18" fill="white"/>
      </svg>
    </span>
    <span class="btn__text-container">JupyterLite</span>
  </a>
</li>
"""

# Step 5: Loop through HTML files and inject buttons
for root, _, files in os.walk(html_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()

            match = colab_regex.search(html)
            if match:
                filename = match.group("filename")
                notebook_name = filename.replace(".ipynb", "")

                if notebook_name in valid_notebooks:
                    jl_button = jupyterlite_template.format(filename=filename)
                    new_html = html.replace(match.group(1), match.group(1) + "\n" + jl_button)

                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_html)
                    print(f"✅ Added JupyterLite button to {file}")
                else:
                    print(f"⏭ Skipped {file} (not in TOC notebooks)")
