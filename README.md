# PELIVET Veterinary Clinic — Website

[![CI](https://github.com/malcolmbuluku/pelivet/actions/workflows/ci.yml/badge.svg)](https://github.com/malcolmbuluku/pelivet/actions/workflows/ci.yml)
[![Deploy](https://github.com/malcolmbuluku/pelivet/actions/workflows/deploy.yml/badge.svg)](https://github.com/malcolmbuluku/pelivet/actions/workflows/deploy.yml)

A professional, multi-page veterinary clinic website with a Flask backend,
database-backed content and bookings, an admin dashboard, and page-view
analytics. Same stack as **pabesh.online**: Flask + Gunicorn + Nginx + Certbot
+ SQLite on a DigitalOcean droplet.

**Repository:** `github.com/malcolmbuluku/pelivet` · **Live:** pelivet.co.ke

---

## What's inside

**Public pages**

| Route | Page |
|---|---|
| `/` | Home |
| `/services` | All services |
| `/services/<slug>` | Individual service detail (dynamic) |
| `/about` | About, values & team |
| `/team` | Full team |
| `/first-visit` | First-visit steps + FAQ |
| `/reviews` | All testimonials |
| `/contact` | Booking form + contact form + map + hours |
| `/sitemap.xml`, `/robots.txt` | SEO |

**Admin** (`/admin`) — session login, bookings table with status controls,
incoming messages, newsletter count, and a 7-day page-views panel.

**Dynamic bits**
- Services, team and testimonials are stored in the database and seeded from
  `content.py` — edit that file and re-run `python seed.py` to update the site.
- Booking and contact forms are validated server-side (WTForms) with CSRF
  protection, saved to SQLite, and optionally emailed to the clinic.
- Every public page view is logged for the analytics panel.

---

## Project layout

```
pelivet/
├── app.py                 # application factory + page-view tracking + errors
├── wsgi.py                # Gunicorn entry point (wsgi:app)
├── config.py              # env-driven config
├── extensions.py          # db, csrf, mail
├── models.py              # SQLAlchemy models
├── forms.py               # WTForms (booking, contact, newsletter, admin login)
├── content.py             # EDIT ME: services, team, testimonials, FAQs
├── icons.py               # inline SVG icon set
├── emails.py              # optional email notifications
├── seed.py                # create + seed the database
├── gunicorn_config.py
├── requirements.txt
├── .python-version        # 3.12
├── .env.example           # copy to .env
├── .github/
│   ├── workflows/
│   │   ├── ci.yml         # compile + seed + route smoke test (push & PR)
│   │   └── deploy.yml     # SSH deploy to the droplet (push to main)
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── routes/
│   ├── public.py          # all public pages + forms
│   └── admin.py           # login + dashboard
├── templates/             # Jinja templates (base + partials + pages)
├── static/{css,js,img}/   # styles.css, main.js, logo + favicon
└── deploy/                # systemd unit + nginx config
```

---

## Where things run

Two environments, two different sets of commands — don't mix them:

| | **Local (your Windows machine)** | **Production (DigitalOcean droplet)** |
|---|---|---|
| Purpose | Develop & preview | Serve the live site |
| Run with | `./run.sh` or `python app.py` | Gunicorn + systemd + Nginx |
| Server | Flask dev server (`:5000`) | Gunicorn behind Nginx (`:443`) |
| `sudo` / `systemctl` / `nginx` / `certbot`? | **No** — these don't exist on Windows | **Yes** — only here, over SSH |

Rule of thumb: on Windows you only ever run `./run.sh` (or `python app.py`).
Everything with `sudo` runs on the droplet.

---

## Run locally

Fastest — one command creates the venv, installs deps, seeds the DB and starts
the server (works in Git Bash on Windows and on Linux/macOS):

```bash
./run.sh
```

Or do it by hand:

### Windows (your machine — use `py -3`)

```powershell
cd pelivet
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env          # then edit .env
python seed.py                  # creates instance\pelivet.db and seeds content
python app.py                   # http://127.0.0.1:5000
```

In Git Bash the activate line is `source .venv/Scripts/activate`.

### Linux / macOS

```bash
cd pelivet
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then edit .env
python seed.py
python app.py                   # http://127.0.0.1:5000
```

**Admin:** http://127.0.0.1:5000/admin — default `admin` / `pelivet-admin`
(change `ADMIN_PASSWORD` in `.env`).

---

## Push to GitHub (first time)

This project is already a Git repository with an initial commit on `main`.
To publish it to `github.com/malcolmbuluku/pelivet`:

```bash
# Create the empty repo on GitHub first (via the website or `gh`):
gh repo create malcolmbuluku/pelivet --private --source=. --remote=origin --push

# …or, if the repo already exists, just point origin at it and push:
git remote add origin https://github.com/malcolmbuluku/pelivet.git
git branch -M main
git push -u origin main
```

`.env`, the SQLite database and caches are already git-ignored, so no secrets
or data leave your machine. After the first push, add the three Actions secrets
(see **CI/CD** below) and every push to `main` deploys automatically.

---

## Editing content

- **Services, team, testimonials, FAQs** → edit `content.py`, then
  `python seed.py` (re-running is safe — it updates content and never touches
  bookings, messages or subscribers).
- **Clinic name, phone, email, address, map** → set in `.env` (no code change).
- **Look & feel** → `static/css/styles.css` (design tokens live at the top in
  `:root`).

---

## Deploy to the DigitalOcean droplet

> ⚠️ **Run this block on the droplet, over SSH (`ssh thebuluku@138.68.185.223`)
> — not on your Windows machine.** systemd, nginx and certbot are Linux-only;
> on Windows these commands fail with "sudo is disabled". On Windows you only
> run the site locally (see **Run locally**).

Same pattern as pabesh. On the droplet (`138.68.185.223`, user `thebuluku`):

```bash
# One-time setup
cd ~
git clone https://github.com/malcolmbuluku/pelivet.git
cd pelivet
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # set SECRET_KEY, ADMIN_PASSWORD, clinic details
python seed.py

# Gunicorn service
sudo cp deploy/pelivet.service /etc/systemd/system/pelivet.service
sudo systemctl daemon-reload
sudo systemctl enable --now pelivet

# Nginx + HTTPS
sudo cp deploy/nginx.conf /etc/nginx/sites-available/pelivet
sudo ln -s /etc/nginx/sites-available/pelivet /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d pelivet.co.ke -d www.pelivet.co.ke
```

**CI/CD:** the workflows are already in `.github/workflows/`. `ci.yml` runs on
every push and PR (compiles, seeds a throwaway DB, checks routes). `deploy.yml`
runs on every push to `main` — it SSHes into the droplet, pulls, reseeds and
restarts. Just add three repository secrets (Settings → Secrets and variables →
Actions): `DROPLET_HOST` = `138.68.185.223`, `DROPLET_USER` = `thebuluku`, and
`SSH_KEY` = the matching private deploy key.

---

## Going-live checklist

- [ ] Set a strong `SECRET_KEY` and `ADMIN_PASSWORD` in `.env`
- [ ] Fill in real clinic phone, emergency line, email and address in `.env`
- [ ] Configure SMTP (`MAIL_*`) so bookings are emailed, or check the admin daily
- [ ] Replace placeholder team bios, stats and reviews in `content.py`
- [ ] Point `pelivet.co.ke` DNS at the droplet and run Certbot
- [ ] Back up `instance/pelivet.db` regularly (it holds bookings & messages)

---

## Notes

- SQLite is perfect for this traffic level and matches pabesh. To move to
  Postgres later, just set `DATABASE_URL` in `.env` — no code changes.
- Email is optional: with `MAIL_SERVER` blank, submissions are still saved and
  visible in the admin; nothing breaks.
