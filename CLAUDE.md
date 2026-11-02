# Project Context for Claude Code

This file exists so Claude Code (or any AI assistant working in this repo)
has full context without the user needing to re-explain the project. Read
this fully before making changes.

## What this is

A single-page Flask website for a custom cabinetry / home renovation
business. The business does no e-commerce — everything is custom,
quote-based work — so the site's only job is to showcase past projects
and drive visitors to submit a contact form for a quote. No shopping
cart, no pricing pages, no product listings.

The person building this is learning Python and specifically wanted to
build it in Flask (rather than a no-code builder or plain static HTML)
to get real backend practice — routes, form validation, etc. Keep that
in mind: prefer teaching-clear Python over clever-but-opaque Python when
making changes, and prefer extending the existing patterns over
introducing new frameworks/libraries unless asked.

## Commands

```bash
python3 -m venv venv
source venv/bin/activate          # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py                    # runs on http://127.0.0.1:5000, debug mode on (auto-reload)
```

There is no test suite and no linter/formatter configured in this repo — don't
assume `pytest`, `flake8`, `black`, etc. are available unless you add them.

## Stack

- **Backend**: Flask (Python), Jinja2 templates
- **Frontend**: vanilla HTML/CSS/JS — no React, no build step, no npm
- **Data**: contact form submissions are appended to `data/submissions.csv`
  via Python's `csv` module — there is no database
- **Deployment target**: Render.com as a **Web Service** (not Static Site),
  using `gunicorn app:app` as the start command

## File structure and what each thing does

```
app.py              Flask routes + contact form validation logic.
                     `home()` renders the page. `contact()` validates
                     and saves submissions, then redirects with a
                     flash message. Also loads `.env` via `load_dotenv()`,
                     configures Flask-Mail from env vars, and (if mail
                     credentials are set) calls `send_contact_email()`
                     to notify the business owner of new submissions.

content.py           ALL editable site text lives here as one Python
                     dict called CONTENT. This is intentionally the
                     single place to edit copy without touching HTML.

requirements.txt     Flask, gunicorn, Flask-Mail (contact form email
                     delivery), python-dotenv (loads `.env` locally).

.env.example         Template listing every environment variable the
                     app reads (SECRET_KEY + Flask-Mail settings).
                     Tracked in git. Copy to `.env` (gitignored) and
                     fill in real values — see README for step-by-step
                     Gmail app-password instructions.

static/css/style.css
                     The entire design system. CSS custom properties
                     (colors, fonts) are defined at the top in :root.
                     Organized in commented sections matching the page
                     sections (hero, about, services, process, gallery,
                     contact, footer).

static/js/script.js  Three small vanilla JS behaviors: mobile nav
                     toggle, gallery category filtering, and an
                     IntersectionObserver-based scroll-reveal effect.
                     No frameworks, no build step.

static/images/gallery/
                     Real project photos, organized under
                     <Kitchen|built-in|cabinet>/ subfolders.

templates/index.html The whole page, broken into sections via HTML
                     comments (HERO, ABOUT, SERVICES, PROCESS, GALLERY,
                     CONTACT). Pulls text from `content` (passed in from
                     app.py) via Jinja.

templates/macros.html
                     Two reusable Jinja macros:
                     - joinery_divider(variant): the signature dovetail/
                       finger-joint SVG divider between sections
                     - tool_icon(name): small line-art SVG icons for
                       service cards ("chisel", "plane", "square",
                       "hammer")

templates/_nav.html, templates/_footer.html
                     Included partials for the nav bar and footer.
```

## Design system (for consistency if extending the UI)

- **Palette**: deep walnut/espresso dark (`--color-bg-dark: #1E140D`)
  alternating with a sawdust cream light section (`--color-bg-light:
  #F4ECDC`), with a brass/copper accent (`--color-accent: #C08A4E`).
  All defined as CSS custom properties at the top of style.css — change
  values there, not inline.
- **Type**: Fraunces (serif, headings) + Inter (body) + JetBrains Mono
  (used for small uppercase labels/eyebrows, styled like spec/measurement
  tags — ties into the carpentry theme). Loaded from Google Fonts in the
  `<head>` of index.html.
- **Signature element**: the dovetail/finger-joint divider
  (`joinery_divider` macro) used between Hero→About and
  Gallery→Contact. This is intentional and on-brand (real joinery
  shape) — don't replace with a generic wave/blob divider.
- **Layout**: single scrolling page, sticky nav, alternating dark/light
  section backgrounds, CSS Grid for multi-column layouts (services cards,
  gallery masonry, contact split layout).

## Known issues already found and fixed — don't reintroduce these

1. **Scroll-reveal content must stay visible without JS.** The `.reveal`
   class only animates from `opacity: 0` when the `<html>` element has a
   `.js-enabled` class, which is added via a synchronous inline `<script>`
   in the `<head>`. If JS fails to load, content must still be visible by
   default. If you touch `.reveal` CSS or the reveal script, preserve this
   no-JS fallback.
2. **Nav brand text must not wrap.** `.nav-brand` has
   `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;`
   because the nav bar has a fixed height — if the business name is long
   and wraps to two lines, it breaks out of the nav and overlaps the hero
   content below it. Keep this constraint if changing nav markup.
3. **Render.com deployment**: must be a Web Service, not a Static Site
   (Static Site has no Python backend — the "Publish Directory" field
   the user got stuck on is a Static Site setting and doesn't apply here).
   Build command: `pip install -r requirements.txt`. Start command:
   `gunicorn app:app`.

## Current content state

Real business details are filled into `content.py`: business name
(G.Kannemeyer Interior Design), owner name/quote, phone/WhatsApp/email/
address, and years in business are all real, not placeholders.

Real project photos are in use, organized under
`static/images/gallery/<Kitchen|built-in|cabinet>/` and referenced from
`content.py` as `.png` paths, each with a real `title`. The original
`.jpeg` duplicates and the wood-tone placeholder SVGs (plus
`generate_placeholders.py`) have been deleted now that real photos are
in place.

Email delivery for the contact form is scaffolded but not yet filled
in with real credentials (added 2026-07-31). `app.py` reads
`SECRET_KEY` plus `MAIL_SERVER`/`MAIL_PORT`/`MAIL_USE_TLS`/
`MAIL_USERNAME`/`MAIL_PASSWORD`/`MAIL_DEFAULT_SENDER`/
`CONTACT_RECIPIENT_EMAIL` from environment variables (via `.env`
locally, Render dashboard env vars in production) — see
`.env.example` for the full list. Until the user fills in real Gmail
(or other SMTP) credentials, the `/contact` route detects that mail
isn't configured and just skips sending — the CSV save still happens
every time regardless. **No code changes are needed to turn email on**
— only `.env` needs real values, following the Gmail app-password
steps in README.md.

## Deferred / removed features

These were deliberately removed rather than left as placeholders — not
needed for launch, but easy to bring back the same way if there's real
content for them later:

- **Testimonials** — removed 2026-07-28. `content.py` had a
  `testimonials` list with placeholder quotes, and `templates/index.html`
  had a (commented-out) testimonials `<section>`; both were deleted
  outright, along with the `.testimonial-*` CSS in `style.css`. To bring
  it back: add a `testimonials` list to `content.py` (each entry:
  `quote`, `author`, `project`), re-add a `<section id="testimonials">`
  block in `index.html` between Gallery and Contact (check git history
  for the original markup), and restore the matching CSS.
- **Social links** — `instagram_url` / `facebook_url` were removed from
  `content.py`. They were never actually wired into any template (no
  icon or link ever rendered them), so re-adding them is just adding the
  keys back plus a footer or nav element to display them.

## Outstanding tasks

- **Fill in real `.env` values.** Copy `.env.example` to `.env`, set a
  real `SECRET_KEY`, and (when the Gmail app password is ready) fill in
  `MAIL_USERNAME`/`MAIL_PASSWORD`/`MAIL_DEFAULT_SENDER`/
  `CONTACT_RECIPIENT_EMAIL` — see README.md's "Setting up email
  delivery" section for the exact steps. **This is the only file that
  needs editing to turn on real email delivery — `app.py` doesn't need
  any code changes**, it already reads whatever is in `.env`.
- **Set the same env vars on Render** before/at deploy time (Render
  dashboard → service → Environment tab), since `.env` itself is
  gitignored and never gets uploaded there.

## Things NOT to change without asking

- Don't introduce e-commerce / shopping cart / pricing-list patterns —
  explicitly out of scope for this business (everything is custom-quoted).
- Don't swap the stack to React/Next/a static site generator — the user
  is using this project specifically to practice Python/Flask.
- Don't replace the joinery-divider signature element with a generic
  section divider.
