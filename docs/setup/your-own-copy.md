# Your own copy (optional)

Cloning is enough to do the course. A **fork** gives you your own copy of the repo on GitHub. You can commit your notes, exercise answers and capstone work, publish your own version of this site as a portfolio, and still pull in course updates.

## 1. Fork and clone

1. Signed in to GitHub, open <https://github.com/darolution/FDE-Training> and click **Fork** → **Create fork**.
2. Clone **your** fork (replace `<your-username>`):

    ```bash
    git clone https://github.com/<your-username>/FDE-Training.git
    cd FDE-Training
    ```

3. Tell git where course updates come from:

    ```bash
    git remote add upstream https://github.com/darolution/FDE-Training.git
    ```

If you already cloned the original, you can point it at your fork instead: `git remote rename origin upstream`, then `git remote add origin https://github.com/<your-username>/FDE-Training.git`.

## 2. Save your work

Commit whenever you finish a piece of work, and push when you want it on GitHub:

```bash
git status                     # labs/.env must NOT appear
git add .
git commit -m "L3: finish loops exercises"
git push
```

Small, clear commits make a good history, and you can push several at once. Don't leave work unpushed for weeks, though: until you push, it exists only on your computer.

Put your own writing (notes, capstone discovery, security reviews, handovers) in `docs/notes/`, and add those pages to the `nav:` section of `mkdocs.yml` so they appear on your site.

## 3. Get course updates

```bash
git fetch upstream
git merge upstream/main
```

If git reports a conflict, it means you and the course changed the same lines. Open the file, keep what you want, then `git add` it and `git commit`.

## 4. Publish your own site (optional)

The repo includes a GitHub Actions workflow that tests the labs, builds the site and publishes it to GitHub Pages.

1. In `mkdocs.yml`, change `site_url`, `repo_url` and `repo_name` to your username, then commit and push.
2. On GitHub, open your fork → **Settings** → **Pages** → **Build and deployment** → **Source: GitHub Actions**.
3. Open the **Actions** tab. If GitHub asks, click to enable workflows for your fork. Then open **Publish site** → **Run workflow**.

When both jobs are green, your site is at `https://<your-username>.github.io/FDE-Training/`. Every push to `main` updates it.

!!! warning "A Pages site is public"
    On free GitHub plans, Pages sites are public even if the repo is private. Don't publish anything personal or confidential.

## 5. Protect against leaked keys

On your fork: **Settings → Advanced Security** (under *Security and quality*), click **Enable** next to *Secret Protection*, then **Enable** next to *Push protection*. GitHub then blocks pushes that contain a recognisable API key.

## Preview the site on your computer

```bash
python -m pip install -r requirements-docs.txt
mkdocs serve -a 127.0.0.1:8001
```

Open <http://127.0.0.1:8001>. Pages reload as you edit. Run `mkdocs build --strict` before pushing: it fails on broken links, just like the publish workflow does.
