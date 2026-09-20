"""
update_image_category_size.py

Repo ROOT se chalao:
    python update_image_category_size.py

Yeh /image wale prompt mein category-jaise shabd dhoondhta hai aur
sahi size khud chunta hai:
  - "youtube thumbnail" / "thumbnail" -> 1280x720
  - "reel" / "shorts" / "story" / "status" -> 1080x1920
  - "instagram post" / "square" -> 1080x1080
  - "banner" / "cover photo" -> 1200x630
  - "poster" -> 1080x1350
  - kuch na mile to default 1024x1024

Prompt mein category ka naam likhna hoga (jaise "/image youtube
thumbnail for a cooking channel..."), tabhi sahi size chunega.
"""

from pathlib import Path
import sys

INDEX_HTML = Path("index.html")

OLD_BLOCK = '''                    const imageMatch = /^\\/image\\s+([\\s\\S]+)/i.exec(combinedText.trim());
                    if (imageMatch) {
                        const imgPrompt = imageMatch[1].trim();
                        const SAATHI_IMAGE_URL = 'https://saathi-ai-y48j.onrender.com/v1/image';
                        fetch(SAATHI_IMAGE_URL, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-API-Key': SAATHI_KEY
                            },
                            body: JSON.stringify({
                                prompt: imgPrompt,
                                model: currentModel
                            })
                        })'''

NEW_BLOCK = '''                    const imageMatch = /^\\/image\\s+([\\s\\S]+)/i.exec(combinedText.trim());
                    if (imageMatch) {
                        const imgPrompt = imageMatch[1].trim();
                        const _detectImageSize = (p) => {
                            const t = p.toLowerCase();
                            if (t.includes('thumbnail')) return { width: 1280, height: 720 };
                            if (t.includes('reel') || t.includes('shorts') || t.includes('story') || t.includes('status')) return { width: 1080, height: 1920 };
                            if (t.includes('instagram post') || t.includes('square')) return { width: 1080, height: 1080 };
                            if (t.includes('banner') || t.includes('cover photo') || t.includes('facebook cover')) return { width: 1200, height: 630 };
                            if (t.includes('poster')) return { width: 1080, height: 1350 };
                            return { width: 1024, height: 1024 };
                        };
                        const _imgSize = _detectImageSize(imgPrompt);
                        const SAATHI_IMAGE_URL = 'https://saathi-ai-y48j.onrender.com/v1/image';
                        fetch(SAATHI_IMAGE_URL, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-API-Key': SAATHI_KEY
                            },
                            body: JSON.stringify({
                                prompt: imgPrompt,
                                model: currentModel,
                                width: _imgSize.width,
                                height: _imgSize.height
                            })
                        })'''


def main():
    if not INDEX_HTML.exists():
        sys.exit(f"{INDEX_HTML} nahi mila. Repo ROOT se chalao.")

    source = INDEX_HTML.read_text(encoding="utf-8")

    if "_detectImageSize" in source:
        print("Category-size detection already lagi hai — kuch nahi badla.")
        return

    if OLD_BLOCK not in source:
        sys.exit("Expected /image block nahi mila. Fresh index.html bhejo.")

    source = source.replace(OLD_BLOCK, NEW_BLOCK, 1)
    INDEX_HTML.write_text(source, encoding="utf-8")
    print("Category-based image size detection add ho gayi. OK")
    print("Ab: git add . && git commit -m 'auto-detect image size by category' && git push")


if __name__ == "__main__":
    main()
