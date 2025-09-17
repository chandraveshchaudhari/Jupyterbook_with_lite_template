---

# Welcome to *JupyterBook + JupyterLite integration Template* 🚀📊

This repository is a **template** for building your own interactive **JupyterBook** with:

* ✅ **JupyterLite integration** (run notebooks directly in the browser, no installation needed)
* ✅ **Google Colab option** (open notebooks in Colab with one click)

It is designed for **teaching, self-study, or research projects**, especially where **business + machine learning** intersect.
You can fork this repo and customize it for your own course, project, or book.

---

## 📖 Features of This Template

* **Interactive Book** built with [JupyterBook](https://jupyterbook.org)
* **In-browser execution** via [JupyterLite](https://jupyterlite.readthedocs.io/)
* **Colab badges** to open notebooks directly in Google Colab
* **Pre-configured GitHub Actions** for automatic deployment to GitHub Pages
* **Organized structure** with `lecture_notebooks/`, `_config.yml`, and `_toc.yml` already set up

---

## ⚡ How to Use This Template

1. **Create your repo**

   * Click **“Use this template”** (green button on top of GitHub)
   * Give your new repo a name, e.g. `my-ml-book`

2. **Clone your repo locally**

   ```bash
   git clone https://github.com/yourusername/my-ml-book.git
   cd my-ml-book
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Build the book locally**

   ```bash
   jupyter-book build .
   ```

   Preview the site in `_build/html/`.

5. **Deploy to GitHub Pages**
   Push your changes to GitHub—deployment is automatic with GitHub Actions.

---

## 🖥️ Running Notebooks

You have **three options** to run notebooks:

1. **In the browser (no install needed)**
   Every notebook has a **“Launch in JupyterLite”** badge → click and run instantly in your browser.

2. **On Google Colab**
   Look for the **“Open in Colab”** badge at the top of each notebook.

3. **Locally**
   Run with JupyterLab or VS Code after installing requirements.

---

## 👨‍🏫 About the Author (Template Maintainer)

**Dr. Chandravesh Chaudhari**
Assistant Professor, School of Business and Management
Christ (Deemed to be University), India

📧 [chandravesh.chaudhari@christuniversity.in](mailto:chandravesh.chaudhari@christuniversity.in)
🌐 [Personal Website](https://github.com/chandraveshchaudhari/website)
🔗 [LinkedIn](https://www.linkedin.com/in/chandraveshchaudhari)

---

## 🚀 Get Started Now

* Use the sidebar (📑 Table of Contents) to navigate through chapters
* Try out the examples directly in **JupyterLite** or **Google Colab**
* Customize the content and publish your own book

```{tableofcontents}
```
