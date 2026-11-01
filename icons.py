"""Inline SVG icon set, exposed to templates as `icon('name')`.

Keeping icons as inline SVG (no icon-font dependency) keeps the site fast and
fully self-contained. Each value is the inner markup of a 24x24 stroked icon.
"""
from markupsafe import Markup

_PATHS = {
    "pulse": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "syringe": '<path d="M18 2l4 4-9 9-4 1 1-4 8-8z"/><path d="M2 22l6-2"/><circle cx="6" cy="18" r="2"/>',
    "tooth": '<path d="M12 5.5c-2-2.5-6-2-7 1s1 7 3 9c1 1 2 0 2-1.5 0 1.5 1 2.5 2 1.5 2-2 4-6 3-9s-1-3.5-3-1z"/>',
    "cross": '<path d="M8 2v4M16 2v4M12 6v12M6 12h12M9 22h6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "heart-pulse": '<path d="M12 21C7 17 3 13 3 8.5A4.5 4.5 0 0 1 12 6a4.5 4.5 0 0 1 9 2.5C21 13 17 17 12 21z"/><path d="M12 8v5M9.5 10.5h5"/>',
    "shield": '<path d="M12 2a3 3 0 0 0-3 3c0 1 .5 2 1 3-2 1-4 3-4 6a6 6 0 0 0 12 0c0-3-2-5-4-6 .5-1 1-2 1-3a3 3 0 0 0-3-3z"/>',
    "scissors": '<path d="M3 6h18M6 6v14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V6M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><circle cx="12" cy="13" r="3"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "alert": '<path d="M12 9v4M12 17h.01M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "check": '<path d="M20 6L9 17l-5-5"/>',
    "heart": '<path d="M12 21C7 17 3 13 3 8.5A4.5 4.5 0 0 1 12 6a4.5 4.5 0 0 1 9 2.5C21 13 17 17 12 21z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "logout": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5M21 12H9"/>',
}


def icon(name: str, cls: str = "") -> Markup:
    inner = _PATHS.get(name, "")
    cls_attr = f' class="{cls}"' if cls else ""
    return Markup(
        f'<svg{cls_attr} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
    )
