"""
update_image_generation.py

Repo ROOT se chalao:
    python update_image_generation.py

Yeh /v1/image endpoint ko Pollinations.ai (bilkul free, koi API key
nahi chahiye) se jod deta hai. Prompt bhejo, image ka URL wapas milta
hai.

Baaki kuch nahi badalta.
"""

from pathlib import Path
import sys

MAIN_PY = Path("app/main.py")

OLD_BLOCK = '''@app.post("/v1/image")
def image(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "image")
    raise HTTPException(501, "Image model/provider अभी connect नहीं है")'''

NEW_BLOCK = '''@app.post("/v1/image")
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


def main():
    if not MAIN_PY.exists():
        sys.exit(f"{MAIN_PY} nahi mila. Repo ROOT se chalao.")

    source = MAIN_PY.read_text(encoding="utf-8")

    if "image.pollinations.ai" in source:
        print("Image generation already jud chuka hai — kuch nahi badla.")
        return

    if OLD_BLOCK not in source:
        sys.exit("Expected /v1/image block nahi mila. Fresh cat bhejo.")

    source = source.replace(OLD_BLOCK, NEW_BLOCK, 1)
    MAIN_PY.write_text(source, encoding="utf-8")
    print("Image generation (/v1/image) jud gaya. OK")
    print("Ab: git add . && git commit -m 'wire up free image generation' && git push")


if __name__ == "__main__":
    main()
