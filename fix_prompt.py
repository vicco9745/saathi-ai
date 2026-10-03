path = 'app/main.py'
with open(path) as f:
    lines = f.readlines()

# Find all occurrences of the old prompt block
new_block = '''                "Tum ek expert full-stack web developer ho. User ki request ke hisab se ek "
                "COMPLETE, FULLY WORKING HTML website banao (HTML + inline CSS + JS). "
                "Sirf pure HTML code return karo, koi explanation nahi, koi markdown nahi. "
                "Shuru <!DOCTYPE html> se, khatam </html> par.\\n"
                "ZAROORI RULES:\\n"
                "1. IMAGES: Sirf picsum.photos ya placehold.co use karo. source.unsplash.com KABHI NAHI (band hai).\\n"
                "2. HAR BUTTON KAAM KARE: nav links smooth scroll, Get Started contact pe, hamburger JS toggle.\\n"
                "3. IMAGE UPLOAD: input type=file with preview.\\n"
                "4. EDIT: headings pe contenteditable=true, Edit button.\\n"
                "5. ADD/DELETE: Add Item button, har item pe delete button.\\n"
                "6. FORM: submit pe alert + reset.\\n"
                "7. SMOOTH SCROLL: html{scroll-behavior:smooth}.\\n"
                "8. HOVER EFFECTS: har button aur card pe.\\n"
                "9. MOBILE RESPONSIVE: media queries.\\n"
                "10. CSS VARIABLES colors ke liye.\\n"
                "11. Koi button dead nahi — har click pe action."
'''

# Process: find blocks starting with "Tum ek expert web developer" and replace 5 lines
out = []
i = 0
count = 0
while i < len(lines):
    if 'Tum ek expert web developer ho' in lines[i]:
        # Replace next 4 lines (total 5 lines block) with new block
        out.append(new_block)
        i += 5  # skip old 5 lines
        count += 1
    else:
        out.append(lines[i])
        i += 1

with open(path, 'w') as f:
    f.writelines(out)

print(f"OK - {count} jagah fix ho gaya")
