"""
All editable website text lives here.

This file is intentionally separate from app.py (the logic) and the
templates (the layout). When the real business details are ready,
this is the only file that needs to change for 90% of the content.

Everything is plain Python dicts and lists, so you can edit values,
add another service, add another testimonial, etc. without touching
HTML at all.
"""

CONTENT = {

    # ---- Brand basics ----
    "business_name": "G.Kannemeyer Interior Design",
    "tagline": "Custom Cabinetry & Home Renovations",
    "location_short": "Serving [City, Region]",
    "phone": "(555) 555-5555",
    "email": "hello@example.com",
    "address": "123 Workshop Lane, [City, State]",
    "years_in_business": 15,
    "instagram_url": "#",
    "facebook_url": "#",

    # ---- Hero section ----
    "hero_eyebrow": "Custom Cabinetry  ·  Kitchens  ·  Built-Ins  ·  Full Renovations",
    "hero_heading": "Built by hand. Built to last.",
    "hero_subheading": (
        "We design and build custom cabinetry and home renovations "
        "around how you actually live — not a catalog."
    ),
    "hero_cta": "Request a Quote",

    # ---- About section ----
    "about_eyebrow": "The Workshop",
    "about_heading": "Every project starts with a conversation, not a catalog.",
    "about_body": (
        "G.Kannemeyer Interior Design is a one-stop shop for custom "
        "interior design and home renovations. For over {years} years, we've worked "
        "directly with homeowners to design and build pieces that fit their "
        "space, their style, and their budget — from a single built-in "
        "bookshelf to a full kitchen remodel."
    ).format(years=25),
    "owner_name": "Ghiyaath Kannemeyer",
    "owner_title": "Owner & Master Carpenter",
    "owner_quote": (
        "I don't build from a catalog. I build what you actually need, "
        "the way it should have been built the first time."
    ),

    # ---- Services ----
    "services_eyebrow": "What We Build",
    "services_heading": "Every project is custom. These are the shapes it usually takes.",
    "services": [
        {
            "title": "Custom Cabinetry",
            "description": (
                "Kitchen cabinets, vanities, and storage built to your exact "
                "measurements, materials, and finish."
            ),
            "icon": "chisel",
        },
        {
            "title": "Kitchen Renovations",
            "description": (
                "Full kitchen overhauls — layout, cabinetry, counters, and "
                "finishes — planned and built end to end."
            ),
            "icon": "plane",
        },
        {
            "title": "Built-Ins & Millwork",
            "description": (
                "Bookshelves, window seats, mudroom benches, and other "
                "fitted woodwork designed for an exact space."
            ),
            "icon": "square",
        },
        {
            "title": "Whole-Home Renovations",
            "description": (
                "Larger renovation projects coordinated from first sketch "
                "to final walkthrough."
            ),
            "icon": "hammer",
        },
    ],

    # ---- Process ----
    "process_eyebrow": "How It Works",
    "process_heading": "From idea to install.",
    "process_steps": [
        {
            "number": "01",
            "title": "Consult",
            "description": "We walk the space, talk through what you need, and take measurements.",
        },
        {
            "number": "02",
            "title": "Design",
            "description": "You get a clear plan — materials, layout, and a real quote before any wood is cut.",
        },
        {
            "number": "03",
            "title": "Build",
            "description": "Everything is built in the workshop and fitted on site, with updates along the way.",
        },
        {
            "number": "04",
            "title": "Install",
            "description": "Final fit, finish, and a walkthrough to make sure it's right.",
        },
    ],

    # ---- Gallery ----
    "gallery_eyebrow": "Recent Work",
    "gallery_heading": "A few projects from the shop floor.",
    "gallery_items": [
        {
            "title": "Oak Kitchen Remodel",
            "category": "Kitchens",
            "image": "/static/images/gallery/placeholder-1.svg",
        },
        {
            "title": "Walnut Built-In Bookshelf",
            "category": "Built-Ins",
            "image": "/static/images/gallery/placeholder-2.svg",
        },
        {
            "title": "Maple Vanity & Storage",
            "category": "Cabinetry",
            "image": "/static/images/gallery/placeholder-3.svg",
        },
        {
            "title": "Mudroom Bench & Lockers",
            "category": "Built-Ins",
            "image": "/static/images/gallery/placeholder-4.svg",
        },
        {
            "title": "Full Kitchen Renovation",
            "category": "Renovations",
            "image": "/static/images/gallery/placeholder-5.svg",
        },
        {
            "title": "Cherry Wood Pantry Cabinets",
            "category": "Cabinetry",
            "image": "/static/images/gallery/placeholder-6.svg",
        },
    ],

    # ---- Testimonials ----
    "testimonials_eyebrow": "From Past Clients",
    "testimonials_heading": "What it's like to work with us.",
    "testimonials": [
        {
            "quote": "Replace this with a real quote from a happy client once you have one.",
            "author": "[Client Name]",
            "project": "Kitchen Renovation",
        },
        {
            "quote": "Replace this with a real quote from a happy client once you have one.",
            "author": "[Client Name]",
            "project": "Custom Built-Ins",
        },
    ],

    # ---- Contact ----
    "contact_eyebrow": "Get In Touch",
    "contact_heading": "Have a project in mind? Let's talk about it.",
    "contact_subheading": (
        "Tell us a bit about what you're looking for and we'll get back "
        "to you to set up a time to walk through it."
    ),
    "project_types": [
        "Custom Cabinetry",
        "Kitchen Renovation",
        "Built-Ins / Millwork",
        "Whole-Home Renovation",
        "Other",
    ],

    # ---- Footer ----
    "footer_note": "Custom cabinetry and home renovations, built to last.",
}
