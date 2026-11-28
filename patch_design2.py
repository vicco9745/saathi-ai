p = 'app/main.py'
s = open(p, encoding='utf-8').read()
OLD = '''        "DESIGN: a bold, modern, professional look that a person would be proud of: a strong colour palette of 3 or 4 colours, a large headline, "
        "clear hierarchy between headline, subheading and body, generous spacing and aligned blocks. "
'''
LINES = [
"DESIGN BRIEF. First choose one clear concept and mood that fits the request (for example warm and friendly for a tea shop, elegant and gold for a wedding, clean and corporate for a business, playful for kids).",
"COLOUR: pick exactly 4 colours as CSS variables on :root: --main (dominant), --accent (bright highlight), --light (background) and --ink (text). Text must have strong contrast with its background. Use gradients between the main and accent colours for hero areas.",
"LAYOUT: keep an outer margin of about 7 percent of the page width. Build the page from clear zones: a hero or header area (about 35 to 45 percent of the height), a content area with aligned blocks or columns, and a footer strip with contact details as [fill in]. Use CSS grid or flexbox, equal gaps, and one repeated corner radius.",
"TYPOGRAPHY: one font family (sans-serif), at most 3 sizes plus the headline. Headline very large and heavy (font-weight 800), tagline lighter, body regular with line-height 1.5. For Hindi or other Indian scripts never use letter-spacing or uppercase, use line-height 1.7 and font-weight 700 at most.",
"DECORATION: use big soft circles, diagonal cut shapes with clip-path, thick accent bars, badges, ribbons, dividers, simple inline SVG icons and subtle repeating-linear-gradient patterns. Layer shapes behind the text with z-index so text stays readable. Keep it clean with plenty of white space.",
"CONTENT: write short punchy lines, a strong headline, a one-line tagline, 3 to 6 key points or sections with a small icon or number each, one clear call-to-action box, and a footer. For a poster use one dominant headline. For a menu use two columns with category headings, dotted leaders and prices only if given.",
"For a certificate use a double border, centred text, a round seal and signature lines. For an invitation centre everything, add an ornament line, and show date, time and place. For a brochure use a cover page, inside pages with columns, and a back page with contact details. For a resume use a side column for contact and skills and a main column for experience.",
"Keep every element inside the page, nothing smaller than 3mm text, and nothing overlapping by accident.",
]
NEW = ''.join('        "' + l + ' "\n' for l in LINES)
if 'DESIGN BRIEF' in s:
    print('design2: pehle se laga hai')
elif s.count(OLD) != 1:
    print('design2: jagah nahi mili', s.count(OLD))
else:
    s = s.replace(OLD, NEW, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('design2: laga diya')
