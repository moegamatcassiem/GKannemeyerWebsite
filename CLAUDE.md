# Project Context for Claude Code

This file exists so Claude Code (or any AI assistant working in this repo)
has full context without the user needing to re-explain the project. Read
this fully before making changes.

## Always ask before making any change

**Before changing anything in this project, describe exactly what you
plan to change (which files and what the edits are) and wait for the
user's OK.** This covers code, content, CSS, templates, this file,
deleting or renaming files, installing packages, and git operations
(commits, pushes, untracking files). Reading and inspecting files
without changing them is fine.

- A general request like "let's fix X" means "propose the changes for
  X", not "go ahead and make them".
- Approval covers only what was proposed. If something new comes up
  partway through, stop and ask again.
- The user wants to review every change because they're using this
  project to learn, so explain what each change does.

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
  using `gunicorn app:app` as the start command. **Render is temporary** —
  the user plans to move to a different, permanent host once the site is
  finished (not chosen yet). Keep deployment advice host-agnostic: the
  final host must run Python/WSGI apps and allow outbound SMTP on port 587.

## File structure and what each thing does

```
app.py              Flask routes + contact form validation logic.
                     `home()` renders the page (with an empty
                     `form_data`). `contact()` validates the form:
                     - name, email, message required; email must match
                       `EMAIL_PATTERN` (name@domain.tld)
                     - phone optional, but if filled in may only use
                       digits/spaces/+/-/brackets and must have 9–15
                       digits (`PHONE_PATTERN`, `PHONE_MIN_DIGITS`,
                       `PHONE_MAX_DIGITS`)
                     On errors it re-renders index.html with
                     `form_data=request.form` so the visitor's answers
                     stay filled in. On success it saves to CSV, emails
                     the owner, and redirects to `/#contact` with a
                     flash message. Also loads `.env` via
                     `load_dotenv()` and configures Flask-Mail from env
                     vars. `send_contact_email()` sends both a plain-text
                     body and a styled HTML version, with `reply_to` set
                     to the customer's email so the owner's Reply goes
                     straight to the customer.

content.py           ALL editable site text lives here as one Python
                     dict called CONTENT. This is intentionally the
                     single place to edit copy without touching HTML.
                     `YEARS_IN_BUSINESS` is a constant above the dict
                     (used by both the hero stat and the About text).
                     `phone_link` / `whatsapp_link` are digits-only
                     copies of the numbers, used for the clickable
                     tel: and wa.me links — keep them in sync with
                     `phone` / `whatsapp`.

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
                     app.py) via Jinja. The contact form refills fields
                     from `form_data`, has `pattern` attributes on email
                     and phone that mirror the server rules, and shows a
                     `.field-hint` under those fields when invalid.

templates/email/contact_notification.html
                     HTML version of the "new enquiry" email sent to the
                     owner, styled to match the site (espresso header,
                     cream body, mono labels, brass "Reply to" button).
                     Rendered by `send_contact_email()` in app.py.

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
4. **The email template must use inline styles and tables.** Many email
   apps (Gmail included) strip `<style>` blocks, ignore CSS variables, and
   don't load web fonts. So `contact_notification.html` has the palette
   hex values copied in by hand, a table layout, and safe font fallbacks
   (Georgia / Arial / Consolas). Don't "clean it up" to use style.css or
   CSS variables — it will break in the owner's inbox. If the site
   palette changes, update the hex values there too.
5. **Field hints use `:user-invalid`, not `:invalid`.** `:invalid` would
   show the red hint/border on the empty required email field as soon as
   the page loads. `:user-invalid` only applies after the visitor types
   or tries to submit. There are no `title` attributes on the fields on
   purpose — the hint was moved out of the hover tooltip and under the
   field instead.
6. **Server validation is the real check.** The HTML `pattern`
   attributes are only for instant feedback (and can be bypassed), so
   any rule change must be made in `validate_contact_form()` in app.py
   and mirrored in the `pattern` attribute in index.html.
7. **User-typed text is escaped by Jinja** in both the re-rendered form
   and the email template. Don't add `|safe` to anything from the form.

## Current content state

Real business details are filled into `content.py`: business name
(G.Kannemeyer Interior Design), owner name/quote, phone/WhatsApp/email/
address, and years in business are all real, not placeholders.

Real project photos are in use, organized under
`static/images/gallery/<Kitchen|built-in|cabinet>/` and referenced from
`content.py` as `.jpg` paths, each with a real `title`. The original
`.jpeg` duplicates and the wood-tone placeholder SVGs (plus
`generate_placeholders.py`) have been deleted now that real photos are
in place.

The gallery photos were converted from PNG to compressed JPEG
(quality 82, longest side capped at 1600px) on 2026-11-02, which cut
the gallery from ~25.8 MB to ~3.5 MB. When adding new photos, save
them the same way (JPEG, ≤1600px longest side) to keep the page fast
on mobile. The two unused PNGs (`built-in (2).png`, `built-in.png`)
were deleted rather than converted.

Email delivery for the contact form is **working and tested locally**
(2026-11-03). The local `.env` has real values: notifications are sent
from a dedicated Gmail account (set in `MAIL_USERNAME`, via an app
password) with the display name "GK Interior Designs Website", to the
owner's inbox set in `CONTACT_RECIPIENT_EMAIL`. Reply-To is the
customer, and the styled HTML email was confirmed to render correctly.
`app.py` reads `SECRET_KEY` plus `MAIL_SERVER`/`MAIL_PORT`/
`MAIL_USE_TLS`/`MAIL_USERNAME`/`MAIL_PASSWORD`/`MAIL_DEFAULT_SENDER`/
`CONTACT_RECIPIENT_EMAIL` from environment variables (`.env` locally,
the host's env var settings in production) — see `.env.example`. If
`MAIL_USERNAME` or `CONTACT_RECIPIENT_EMAIL` is missing, sending is
skipped. The CSV save always happens either way, and an SMTP failure is
only printed, never shown to the visitor.

Note: on Render the filesystem is temporary, so `data/submissions.csv`
is wiped on each deploy/restart there. Email is the reliable record in
production. On a host with a persistent disk, the CSV becomes a useful
backup.

The contact details on the page are clickable (tel:, wa.me, mailto:).
The first notification email landed in the owner's spam folder, which is
normal for a brand-new Gmail sender. The owner should mark it "Not spam"
and add the sender to their contacts.

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

- **Commit and push** the 2026-11-02/03 work (small content fixes, JPG
  images, styled email, form validation/hints, this file).
- **Set the 8 env vars on Render** (dashboard → service → Environment
  tab), since `.env` is gitignored and never gets uploaded. Use a freshly
  generated `SECRET_KEY` (`python -c "import secrets;
  print(secrets.token_hex(32))"`) — the local one is short/hand-typed.
  Then submit a test enquiry on the live URL and confirm the email
  arrives.
- **Choose the permanent host** and update the deployment notes in this
  file (Stack section and Known issue #3) once it's decided.
- **Optional:** `GET /contact` (e.g. pressing Enter in the address bar
  after a form error, when the URL is `/contact#contact`) currently
  returns 405 Method Not Allowed. It could redirect to `/` instead.

## Things NOT to change without asking

- Don't introduce e-commerce / shopping cart / pricing-list patterns —
  explicitly out of scope for this business (everything is custom-quoted).
- Don't swap the stack to React/Next/a static site generator — the user
  is using this project specifically to practice Python/Flask.
- Don't replace the joinery-divider signature element with a generic
  section divider.
