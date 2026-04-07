import os
import re
import yaml

# Get repository info from environment variables (GitHub Actions provides these)
github_repository = os.environ.get('GITHUB_REPOSITORY',
                                   '')  # e.g. "chandraveshchaudhari/Jupyterbook_with_lite_template"

# Construct URL from repository name
if github_repository:
    username, repo_name = github_repository.split('/')
    base_url = f"https://{username.lower()}.github.io/{repo_name}"
    print(f"📦 Repository: {github_repository}")
else:
    # Final fallback - extract from git remote (if running locally)
    import subprocess

    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                                capture_output=True, text=True, check=True)
        remote_url = result.stdout.strip()
        if 'github.com' in remote_url:
            # Extract from git URL: git@github.com:user/repo.git or https://github.com/user/repo.git
            if remote_url.startswith('git@'):
                repo_part = remote_url.split(':')[1].replace('.git', '')
            else:
                repo_part = remote_url.split('github.com/')[1].replace('.git', '')
            username, repo_name = repo_part.split('/')
            base_url = f"https://{username.lower()}.github.io/{repo_name}"
        else:
            raise Exception("Not a GitHub repository")
    except:
        print("❌ Could not determine repository URL. Please set GITHUB_REPOSITORY environment variable.")
        exit(1)

jupyterlite_url = f"{base_url}/jupyterlite/lab/index.html"
print(f"🌐 Base URL: {base_url}")
print(f"🚀 JupyterLite URL: {jupyterlite_url}")

# Paths
toc_path = "notebooks/_toc.yml"
notebooks_dir = "notebooks"
html_dir = "docs"  # Work on docs/ directory
docs_dir = "docs"

repo_slug = github_repository
if not repo_slug:
    try:
        repo_slug = f"{username}/{repo_name}"
    except NameError:
        repo_slug = ""

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
print(f"🔍 Looking for HTML files in: {html_dir}")

# Step 3: Regex patterns
colab_regex = re.compile(
    r'(<a[^>]+href="https://colab\.research\.google\.com/[^"]+/(?P<filename>[^/"]+\.ipynb)"[^>]*>.*?</a>)',
    re.DOTALL
)

dropdown_menu_regex = re.compile(r'(<ul[^>]+class="[^"]*dropdown-menu[^"]*"[^>]*>)', re.DOTALL)

# Step 4: Dynamic JupyterLite button template
jupyterlite_template = f"""
<li>
  <a href="{jupyterlite_url}?path={{filename}}" target="_blank"
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

# Step 5: Check if HTML directory exists
if not os.path.exists(html_dir):
    print(f"❌ HTML directory {html_dir} does not exist!")
    print("Available directories:")
    for item in os.listdir("."):
        if os.path.isdir(item):
            print(f"  - {item}")
    exit(1)

# Step 6: Loop through HTML files, fix placeholder links, and inject buttons
files_processed = 0
buttons_added = 0
links_fixed = 0


def replace_placeholder_links(html_text):
    """Replace common template placeholder links with current fork URLs."""
    replacements = 0

    candidates = [
        "https://<yourusername>.github.io/my-book",
        "https://yourusername.github.io/my-book",
    ]
    for old in candidates:
        if old in html_text:
            html_text = html_text.replace(old, base_url)
            replacements += 1

    if repo_slug:
        # Replace placeholder Colab repository/path variants.
        html_text, n1 = re.subn(
            r"https://colab\.research\.google\.com/github/yourusername/my-book/blob/main/content/files/([^\"']+\.ipynb)",
            rf"https://colab.research.google.com/github/{repo_slug}/blob/main/notebooks/\\1",
            html_text,
        )
        replacements += n1

        html_text, n2 = re.subn(
            r"https://colab\.research\.google\.com/github/yourusername/my-book/blob/main/notebooks/([^\"']+\.ipynb)",
            rf"https://colab.research.google.com/github/{repo_slug}/blob/main/notebooks/\\1",
            html_text,
        )
        replacements += n2

    return html_text, replacements

for root, _, files in os.walk(html_dir):
    for file in files:
        if file.endswith(".html"):
            files_processed += 1
            path = os.path.join(root, file)
            print(f"🔍 Processing: {path}")

            with open(path, "r", encoding="utf-8") as f:
                html = f.read()

            # Fix common placeholder links from starter notebook content.
            html, fixed_count = replace_placeholder_links(html)
            links_fixed += fixed_count

            if "JupyterLite</span>" in html:
                if fixed_count:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(html)
                print(f"  ℹ️ JupyterLite button already present in {file}")
                continue

            match = colab_regex.search(html)
            if match:
                filename = match.group("filename")
                notebook_name = filename.replace(".ipynb", "")
                print(f"  📝 Found Colab button for: {filename}")

                if notebook_name in valid_notebooks:
                    jl_button = jupyterlite_template.format(filename=filename)
                    new_html = html.replace(match.group(1), match.group(1) + "\n" + jl_button)

                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_html)
                    print(f"  ✅ Added JupyterLite button to {file}")
                    buttons_added += 1
                else:
                    print(f"  ⏭ Skipped {file} (not in TOC notebooks)")
            else:
                # Fallback path: infer notebook filename from HTML page name.
                page_name = os.path.splitext(file)[0]
                if page_name in valid_notebooks:
                    filename = f"{page_name}.ipynb"
                    jl_button = jupyterlite_template.format(filename=filename)
                    menu_match = dropdown_menu_regex.search(html)
                    if menu_match:
                        new_html = html.replace(menu_match.group(1), menu_match.group(1) + "\n" + jl_button, 1)
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_html)
                        print(f"  ✅ Added JupyterLite button to {file} (fallback mode)")
                        buttons_added += 1
                    else:
                        # Still persist placeholder link fixes when dropdown is missing.
                        if fixed_count:
                            with open(path, "w", encoding="utf-8") as f:
                                f.write(html)
                        print(f"  ⚠️ Could not find launch dropdown in {file}")
                else:
                    if fixed_count:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(html)
                    print(f"  ℹ️ No Colab button and page is not a TOC notebook: {file}")

print(f"\n📊 Summary:")
print(f"  - HTML files processed: {files_processed}")
print(f"  - JupyterLite buttons added: {buttons_added}")
print(f"  - Placeholder links fixed: {links_fixed}")
print(f"  - Valid notebooks from TOC: {len(valid_notebooks)}")
print(f"  - Generated JupyterLite URL: {jupyterlite_url}")