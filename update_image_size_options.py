"""
update_image_size_options.py

Repo ROOT se chalao:
    python update_image_size_options.py

Yeh /v1/image mein width/height (optional) add karta hai, taaki alag
formats maange ja sakein — jaise:
  - YouTube thumbnail: width=1280, height=720
  - Instagram square: width=1080, height=1080
  - Reels/Shorts: width=1080, height=1920
Kuch na diya jaye to default 1024x1024 (square) rahega.

Prompt mein koi bhi category/topic likh sakte hain — "YouTube
thumbnail for a cooking channel, bold red text" jaisa kuch bhi —
koi restriction nahi hai category par.
"""

from pathlib import Path
import sys

MAIN_PY = Path("app/main.py")

OLD_MODEL = '''class GenericRequest(BaseModel):
    prompt: str'''

NEW_MODEL = '''class GenericRequest(BaseModel):
    prompt: str
    width: int = 1024
    height: int = 1024'''

OLD_IMAGE_BLOCK = '''@app.post("/v1/image")
def image(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "image")
    import urllib.parse
    prompt = (body.prompt or "").strip()
    if not prompt:
        raise HTTPException(400, "Prompt khaali nahi ho sakta")
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    return {
        "service": "image",
        "image_url": image_url,
        "prompt": prompt,
        "model": "saathi-image"
    }'''

NEW_IMAGE_BLOCK = '''@app.post("/v1/image")
def image(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "image")
    import urllib.parse
    prompt = (body.prompt or "").strip()
    if not prompt:
        raise HTTPException(400, "Prompt khaali nahi ho sakta")
    width = body.width or 1024
    height = body.height or 1024
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}"
    )
    return {
        "service": "image",
        "image_url": image_url,
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": "saathi-image"
    }'''


def main():
    if not MAIN_PY.exists():
        sys.exit(f"{MAIN_PY} nahi mila. Repo ROOT se chalao.")

    source = MAIN_PY.read_text(encoding="utf-8")

    if "width: int = 1024" in source:
        print("Size options already lagi hain — kuch nahi badla.")
        return

    if OLD_MODEL not in source:
        sys.exit("GenericRequest model ka expected text nahi mila. Fresh cat bhejo.")
    source = source.replace(OLD_MODEL, NEW_MODEL, 1)

    if OLD_IMAGE_BLOCK not in source:
        sys.exit("/v1/image block ka expected text nahi mila. Fresh cat bhejo.")
    source = source.replace(OLD_IMAGE_BLOCK, NEW_IMAGE_BLOCK, 1)

    MAIN_PY.write_text(source, encoding="utf-8")
    print("Image size options add ho gaye. OK")
    print("Ab: git add . && git commit -m 'add image size options' && git push")


if __name__ == "__main__":
    main()
