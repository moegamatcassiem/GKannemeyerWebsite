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
                     flash message.

content.py           ALL editable site text lives here as one Python
                     dict called CONTENT. This is intentionally the
                     single place to edit copy without touching HTML.
                     Currently filled with PLACEHOLDER content (see
                     "What's still a placeholder" below).

requirements.txt     Flask + gunicorn.

generate_placeholders.py
                     One-off script that generated the 6 wood-tone SVG
                     gallery placeholders. Not needed at runtime — only
                     re-run this if you want to regenerate placeholders.
                     Safe to delete once real photos are in use.

static/css/style.css
                     The entire design system. CSS custom properties
                     (colors, fonts) are defined at the top in :root.
                     Organized in commented sections matching the page
                     sections (hero, about, services, process, gallery,
                     testimonials, contact, footer).

static/js/script.js  Three small vanilla JS behaviors: mobile nav
                     toggle, gallery category filtering, and an
                     IntersectionObserver-based scroll-reveal effect.
                     No frameworks, no build step.

static/images/gallery/
                     6 placeholder SVGs (wood-tone gradients with a
                     label). Swap for real project photos — see
                     "What's still a placeholder" below.

templates/index.html The whole page, broken into sections via HTML
                     comments (HERO, ABOUT, SERVICES, PROCESS, GALLERY,
                     TESTIMONIALS, CONTACT). Pulls text from `content`
                     (passed in from app.py) via Jinja.

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
  Testimonials→Contact. This is intentional and on-brand (real joinery
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

## What's still a placeholder (the main outstanding work)

Everything in `content.py` is placeholder text and needs the real
business details: business name, owner name/quote, phone/email/address,
years in business, real service descriptions if they differ, and real
testimonials once available.

The 6 gallery images in `static/images/gallery/` are generated SVG
wood-tone swatches, not real photos. Once real project photos exist:
1. Add them to `static/images/gallery/` (jpg/png fine).
2. Update each `gallery_items` entry's `"image"` path in `content.py`.
3. Delete the placeholder SVGs and `generate_placeholders.py`.

No email delivery is wired up yet — contact form submissions just save
to a local CSV. Flask-Mail or a service like SendGrid would be the next
step if/when the user wants real email notifications instead.

## Things NOT to change without asking

- Don't introduce e-commerce / shopping cart / pricing-list patterns —
  explicitly out of scope for this business (everything is custom-quoted).
- Don't swap the stack to React/Next/a static site generator — the user
  is using this project specifically to practice Python/Flask.
- Don't replace the joinery-divider signature element with a generic
  section divider.
