# Welcome to *JupyterBook + JupyterLite Integration Template*

This repository is a **template** for building your own interactive **JupyterBook** with:

-  **JupyterLite integration** (run notebooks directly in the browser, no installation needed)
-  **Google Colab option** (open notebooks in Colab with one click)

It is designed for **teaching, self-study, or research projects**, especially where **business + machine learning** intersect. You can fork this repo and customize it for your own course, project, or book.

---

##  Features of This Template

- **Interactive Book** built with [JupyterBook](https://jupyterbook.org)
- **In-browser execution** via [JupyterLite](https://jupyterlite.readthedocs.io/)
- **Colab badges** to open notebooks directly in Google Colab
- **Pre-configured GitHub Actions** for automatic deployment to GitHub Pages
- **Organized structure** with `content/files/` for notebooks, `_config.yml`, and `_toc.yml` already set up

---

##  How to Use This Template

Follow these steps to set up and customize your own JupyterBook with JupyterLite:

1. **Create Your Repository**
   - Click the **"Use this template"** button (green button at the top of this repository on GitHub).
   - Give your new repository a name, e.g., `my-ml-book`.
   - Choose whether to make it public or private, then click **"Create repository from template"**.

2. **Clone Your Repository Locally**
   - Clone the repository to your local machine:
     ```bash
     git clone https://github.com/yourusername/my-ml-book.git
     cd my-ml-book
     ```

3. **Update Configuration Files**
   - Edit `_config.yml` to customize your book’s metadata:
     ```yaml
     title: Your Course or Book Title
     author: Your Name
     logo: path/to/your/logo.png  # Optional: Add a logo image
     execute:
       execute_notebooks: 'off'  # Set to 'auto' if you want to execute notebooks during build
     ```
   - Edit `_toc.yml` to define your table of contents. For example:
     ```yaml
     format: jb-book
     root: intro
     chapters:
       - file: content/files/course_introduction
       - file: content/files/how_to_use
       - file: content/files/roadmap_prereqs
     ```
   - Ensure notebook filenames in `_toc.yml` match those in `content/files/` (without the `.ipynb` extension).

4. **Generate Notebooks from `_toc.yml`**
   - Run the `auto_notebook_creation_using_toc.py` script to generate empty notebooks based on `_toc.yml`:
     ```bash
     python notebooks/auto_notebook_creation_using_toc.py
     ```
   - This script creates empty `.ipynb` files in `content/files/` for each entry in `_toc.yml` (e.g., `course_introduction.ipynb`, `how_to_use.ipynb`).
   - Verify the generated notebooks in `content/files/`:
     ```bash
     ls content/files/*.ipynb
     ```

5. **Customize Notebooks**
   - Edit the notebooks in `content/files/` (e.g., `content/files/roadmap_prereqs.ipynb`) to add your content.
   - Use Markdown cells for text, code cells for Python examples, and include JupyterLite/Colab badges (see examples in the provided notebooks).

6. **Set Up GitHub Pages**
   - Go to your repository on GitHub > **Settings** > **Pages**.
   - Under **Source**, select **GitHub Actions** as the deployment source.
   - The workflow (`.github/workflows/jupyterlite.yml`) will automatically deploy to the `gh-pages` branch when you push changes.

7. **Commit and Push Changes**
   - Stage, commit, and push your changes to the `main` branch:
     ```bash
     git add _config.yml _toc.yml content/files/*.ipynb
     git commit -m "Customize config and notebooks"
     git push origin main
     ```
   - The GitHub Actions workflow will automatically build and deploy your site to GitHub Pages.

8. **Access Your Website**
   - Once the workflow completes, visit `https://<yourusername>.github.io/my-ml-book/jupyterlite/lab/index.html?path=files/roadmap_prereqs.ipynb`.
   - Any changes to notebooks in `content/files/` will trigger the workflow, rebuilding and deploying the site automatically.

---

##  Running Notebooks

You have **three options** to run notebooks:

1. **In the Browser (No Installation Needed)**
   - Click the **"Launch in JupyterLite"** badge in any notebook to run it instantly in your browser via JupyterLite.

2. **On Google Colab**
   - Click the **"Open in Colab"** badge at the top of each notebook to run it in Google Colab.

3. **Locally**
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the build and serve locally:
     ```bash
     chmod +x build_jupyterlite.sh
     ./build_jupyterlite.sh
     ```
   - Access at `http://localhost:8000/jupyterlite/lab/index.html?path=files/roadmap_prereqs.ipynb`.

---

##  About the Author (Template Maintainer)

**Dr. Chandravesh Chaudhari**

📧 [chandraveshchaudhari@gmail.com](mailto:chandraveshchaudhari@gmail.com)  
🌐 [Personal Website](https://github.com/chandraveshchaudhari/website)  
🔗 [LinkedIn](https://www.linkedin.com/in/chandraveshchaudhari)

---

##  Get Started Now

- Use the sidebar (📑 Table of Contents) to navigate through chapters.
- Try out the examples directly in **JupyterLite** or **Google Colab**.
- Customize the content and publish your own book.

```{tableofcontents}
```
