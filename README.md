# Resume — GitHub Pages Site

A static personal resume website hosted on GitHub Pages. All content lives in a single `resume.json` file. Edit the file, run the build script, push — done.

## Tech Stack

- **Build**: Python + Jinja2 (one-time script, no server)
- **Frontend**: Bootstrap 5, Font Awesome, Chart.js, Vanilla JavaScript
- **Hosting**: GitHub Pages

## Updating Your Resume

1. Edit `resume.json` with your real info (personal, experience, education, skills, projects)
2. Run the build script:
   ```bash
   python build.py
   ```
3. Commit and push `index.html` (and `static/` if changed):
   ```bash
   git add index.html static/
   git commit -m "Update resume"
   git push
   ```

## Local Preview

Open `index.html` directly in your browser — no server needed.

## Contact Form

The contact form uses [Formspree](https://formspree.io) (free):

1. Sign up at formspree.io
2. Create a new form
3. Replace `YOUR_FORMSPREE_ENDPOINT` in `templates/index.html` with your form URL
4. Rebuild: `python build.py`

## GitHub Pages Setup

1. Create a repo named `<your-github-username>.github.io`
2. Push `index.html` and `static/` to it
3. Go to repo **Settings → Pages → Source**: branch `main`, folder `/root`
4. Your site goes live at `https://<your-github-username>.github.io`

## GitHub Profile README

`PROFILE_README.md` is the profile README for [github.com/SusanoKevin](https://github.com/SusanoKevin). It uses a "Data Phantom" cyberpunk theme with electric cyan branding, a YAML dossier bio, Unicode skill bars, collapsible experience sections, and GitHub stats widgets.

To deploy it to your GitHub profile:

1. Go to your `SusanoKevin/SusanoKevin` repository (create it if it doesn't exist — it must match your username exactly)
2. Copy the contents of `PROFILE_README.md` into `README.md` in that repo
3. Commit and push — GitHub renders it live at `github.com/SusanoKevin`

## Dependencies

```bash
pip install jinja2
```
