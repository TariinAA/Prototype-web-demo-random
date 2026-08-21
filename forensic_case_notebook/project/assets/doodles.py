"""
doodles.py
----------
Small hand-drawn-style SVG illustrations used to decorate the notebook UI
(microscope, DNA strand, droplet, test tube, magnifying glass, cell).

Kept as plain strings (no external image files needed) so the whole app
stays lightweight and easy to deploy -- nothing extra to upload besides
the model file.
"""

MICROSCOPE = """
<svg width="120" height="130" viewBox="0 0 120 130" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" stroke="#3A3226" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
    <line x1="25" y1="118" x2="95" y2="118"/>
    <path d="M40 118 C40 100 45 95 55 92"/>
    <rect x="30" y="112" width="55" height="9" rx="3" fill="#AEE3F0"/>
    <path d="M55 92 C55 60 60 40 78 26"/>
    <circle cx="78" cy="22" r="7" fill="#F7D6E0"/>
    <path d="M60 55 L85 40" />
    <rect x="45" y="55" width="22" height="10" rx="2" transform="rotate(-28 45 55)" fill="#BFEEDD"/>
    <path d="M50 78 C46 70 46 62 52 56" />
  </g>
</svg>
"""

DNA = """
<svg width="90" height="140" viewBox="0 0 90 140" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" stroke="#3A3226" stroke-width="3" stroke-linecap="round">
    <path d="M20 5 C60 25 20 45 60 65 C20 85 60 105 20 125 C60 105 20 85 60 65 C20 45 60 25 20 5" opacity="0"/>
    <path d="M25 8 C55 28 55 48 25 68 C55 88 55 108 25 128" />
    <path d="M65 8 C35 28 35 48 65 68 C35 88 35 108 65 128" />
    <line x1="28" y1="18" x2="62" y2="18" stroke="#AEE3F0" stroke-width="4"/>
    <line x1="30" y1="38" x2="60" y2="38" stroke="#F7D6E0" stroke-width="4"/>
    <line x1="28" y1="58" x2="62" y2="58" stroke="#BFEEDD" stroke-width="4"/>
    <line x1="30" y1="78" x2="60" y2="78" stroke="#AEE3F0" stroke-width="4"/>
    <line x1="28" y1="98" x2="62" y2="98" stroke="#F7D6E0" stroke-width="4"/>
    <line x1="30" y1="118" x2="60" y2="118" stroke="#BFEEDD" stroke-width="4"/>
  </g>
</svg>
"""

DROPLET = """
<svg width="70" height="90" viewBox="0 0 70 90" xmlns="http://www.w3.org/2000/svg">
  <path d="M35 6 C50 32 62 46 62 60 C62 76 50 86 35 86 C20 86 8 76 8 60 C8 46 20 32 35 6Z"
        fill="#AEE3F0" stroke="#3A3226" stroke-width="3" stroke-linejoin="round"/>
  <ellipse cx="27" cy="55" rx="6" ry="9" fill="#ffffff" opacity="0.55"/>
</svg>
"""

TEST_TUBE = """
<svg width="60" height="130" viewBox="0 0 60 130" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#3A3226" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M20 8 L20 90 C20 108 40 108 40 90 L40 8" />
    <line x1="14" y1="8" x2="46" y2="8"/>
    <path d="M20 62 L40 62 C40 100 20 100 20 62 Z" fill="#BFEEDD"/>
  </g>
</svg>
"""

MAGNIFIER = """
<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" stroke="#3A3226" stroke-width="3.5" stroke-linecap="round">
    <circle cx="33" cy="33" r="22" fill="#F7D6E0" opacity="0.5"/>
    <circle cx="33" cy="33" r="22"/>
    <line x1="49" y1="49" x2="72" y2="72"/>
  </g>
</svg>
"""

CELL = """
<svg width="70" height="70" viewBox="0 0 70 70" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#3A3226" stroke-width="2.5" fill="none">
    <ellipse cx="35" cy="35" rx="28" ry="24" fill="#BFEEDD" opacity="0.6"/>
    <ellipse cx="35" cy="35" rx="28" ry="24" />
    <circle cx="33" cy="33" r="9" fill="#F7D6E0"/>
    <circle cx="18" cy="22" r="3" fill="#AEE3F0" stroke="none"/>
    <circle cx="50" cy="45" r="2.5" fill="#AEE3F0" stroke="none"/>
  </g>
</svg>
"""

PAPERCLIP_EMOJI = "\U0001F4CE"
STAMP_STARS = "\u2605"
