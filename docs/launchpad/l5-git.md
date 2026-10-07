# L5 · Git and GitHub

**Goal:** save versions of your work, try ideas safely on branches, publish to GitHub, and keep secrets out.
**Time:** about 8 hours.

## Why version control?

**Git** records snapshots of a project over time. With it you can:

- go back to any earlier version when something breaks,
- try an idea on a **branch** without touching the working version,
- work with other people on the same files,
- show your history to employers. A GitHub profile with steady, well-described work is part of an FDE's portfolio.

**GitHub** is a website that hosts git repositories online.

## Key words

| Word | Meaning |
|---|---|
| **Repository (repo)** | A project folder whose history git tracks (it has a hidden `.git` folder) |
| **Commit** | A saved snapshot, with a message saying what changed |
| **Staging** | Choosing which changes go into the next commit (`git add`) |
| **Branch** | A separate line of commits. `main` is the usual default |
| **Remote** | A copy of the repo somewhere else, usually GitHub, often called `origin` |
| **Push / pull** | Send commits to the remote / bring new commits down |
| **Clone** | Download a repo, with its whole history |
| **Fork** | Your own copy of someone else's repo on GitHub |

## One-time setup

Tell git who you are. These details are written into every commit:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

!!! tip "Keep your email private"
    GitHub can give you a private "noreply" address (Settings → Emails on github.com). Use it here if you'd rather your personal email didn't appear in public commit history.

Then check:

```bash
python labs/launchpad/l5/check_git.py
```

## Lab: a practice repository

Do this **outside** the course folder, so you can't break the course.

**1. Create a repo and make commits**

```bash
cd ~/Projects
mkdir git-practice
cd git-practice
git init
code README.md             # opens VS Code: type "# Git practice", save, come back
git status                 # README.md is "untracked"
git add README.md          # stage it
git commit -m "Add README"
git log --oneline          # your history so far
```

Edit `README.md` in VS Code (add a line about what you're learning), then:

```bash
git status
git diff                   # exactly what changed
git add README.md
git commit -m "Describe what I'm learning"
```

Commit messages say **what changed and why**, in a few words: `Add price formatting to receipts`, not `stuff` or `update`.

!!! note "Creating files from the terminal on Windows"
    In Windows PowerShell, `echo "text" > file` saves the file in an encoding (UTF-16) that some tools, including GitHub's page view, display badly. That's fine for the throwaway files below; for real files, create them in VS Code.

**2. Branch, change, merge**

```bash
git switch -c add-plan                 # create a branch and move to it
echo "Week plan: L5 git, L6 APIs" > plan.txt
git add plan.txt
git commit -m "Add study plan"
git switch main                        # plan.txt disappears: it lives on the branch
git merge add-plan                     # bring the branch's work into main
git branch                             # list branches
```

**3. Publish to GitHub**

1. On github.com click **New repository**, name it `git-practice`, leave every "initialize" box **unticked**, and create it.
2. GitHub shows commands under "…push an existing repository". They look like:

    ```bash
    git remote add origin https://github.com/<your-username>/git-practice.git
    git push -u origin main
    ```

3. The first push asks you to sign in. Follow the browser prompt (Git Credential Manager) or create a **personal access token** if asked for a password. GitHub no longer accepts your account password here.
4. Refresh the page on GitHub: your files and commits are there.

**4. Check it**

```bash
python ~/Projects/FDE-Training/labs/launchpad/l5/check_git.py ~/Projects/git-practice
```

(Adjust the paths if you put things elsewhere.) You're aiming for every box ticked.

## Keeping secrets out

Anything you push to a public repo can be read, copied and archived by anyone, **immediately and permanently**. Bots scan GitHub for leaked keys within minutes.

- Put secrets in a `.env` file and list `.env` in **`.gitignore`**. Git then ignores the file. The course repo already does this.
- Check `git status` before every commit. If you see `.env`, stop.
- If a secret is ever pushed: **revoke it at the provider first** (that's what actually protects you), then remove it from the repo. Deleting the file in a new commit isn't enough: it's still in the history.

Try it in your practice repo:

```bash
echo "API_KEY=pretend-secret" > .env
git status                    # .env appears, ready to be added by mistake
echo ".env" > .gitignore
git status                    # now .env is ignored; .gitignore itself should be committed
git add .gitignore
git commit -m "Ignore .env files"
```

## Forks

A **fork** is your own copy of someone else's GitHub repo. It's how you'll keep your course work and notes online. Follow [Your own copy](../setup/your-own-copy.md) when you're ready. It uses exactly the commands from this lesson.

## Exercises

1. **Core.** Complete the lab and get every check ticked.
2. **Core.** Make a mistake on purpose: change a line, commit it, then use `git log --oneline` and `git revert <commit-id>` to undo it with a new commit. Look at the log again.
3. **Stretch.** Create a branch, change the same line of `README.md` on both the branch and `main`, commit both, and merge. Git reports a **conflict**. Open the file, pick the version you want, remove the `<<<<<<<` / `>>>>>>>` markers, then `git add` and `git commit`.

## Checkpoint

- [ ] I can init, add, commit, branch, merge and push
- [ ] I write commit messages that say what changed
- [ ] I know how `.gitignore` keeps secrets out, and what to do if one leaks
- [ ] `check_git.py` passes on my practice repo
