# JupyterBook + JupyterLite Template

A professional fork-first template to publish notebook-based docs on GitHub Pages.

## What You Need To Do

Nothing in the template file system is required to make deployment work.

1. Click `Use this template` (or fork this repository).
2. Clone your new repository.
3. For local setup only: `pip install -r requirements.txt`.

## GitHub Deployment (No Local Build Required)

After creating your repo from this template:

1. Go to `Settings -> Actions -> General` and allow workflows to run.
2. Go to `Settings -> Pages` and set source to `GitHub Actions`.
3. Push to `main`.

GitHub Actions will automatically build and deploy your site.

Your site URL will be:

- `https://<your-github-username>.github.io/<your-repo-name>/`

## Local Preview (Optional)

```bash
pip install -r requirements.txt
jupyter-book build notebooks/
```

Then open `notebooks/_build/html/index.html`.

## Where To Put Content

- Add notebooks in `notebooks/`.
- Update `notebooks/_toc.yml` with page names (without `.ipynb`).
- Update `notebooks/_config.yml` with your repository URL, title, and author.

## Notes

- `extensions/forced_jupyterlite_button.py` ensures reliable JupyterLite launch links in generated pages.
- `.github/workflows/build_and_deploy.yml` is preconfigured for GitHub Pages deployment.
