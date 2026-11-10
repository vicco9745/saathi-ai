p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "_transcribe_video" in s:
    print("audio: pehle se laga hai")
    raise SystemExit

helper = r'''# AUDIO helpers
def _transcribe_video(video):
    import base64, requests
    key = os.environ.get("GROQ_API_KEY")
    url = getattr(video, "dataUrl", "") or ""
    if not key or "," not in url:
        return ""
    try:
        raw = base64.b64decode(url.split(",", 1)[1])
    except Exception:
        return ""
    if len(raw) > 24 * 1024 * 1024:
        return ""
    for model in ("whisper-large-v3-turbo", "whisper-large-v3"):
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": "Bearer " + key},
                files={"file": ("video.mp4", raw, "video/mp4")},
                data={"model": model, "response_format": "json", "temperature": "0"},
                timeout=60,
            )
            if r.status_code == 200:
                return (r.json().get("text") or "").strip()[:3000]
            print("WHISPER", model, r.status_code, r.text[:150])
        except Exception as e:
            print("WHISPER error", model, repr(e)[:150])
    return ""

'''

a = "# VIDNATIVE helpers"
oldA = '    videos = [a for a in (body.attachments or []) if a.kind == "video" and a.dataUrl]\n'
newA = oldA + r'''    _vmsg = body.message
    _tr = ""
    if videos:
        try:
            _tr = _transcribe_video(videos[0])
        except Exception:
            _tr = ""
        print("VIDEO: transcript chars =", len(_tr))
        if _tr:
            _vmsg = (body.message or "Is video mein kya ho raha hai, poori detail se batao.") + "\n\nAAWAAZ KA TRANSCRIPT (video ki aawaaz Whisper se likhi gayi; galtiyan ho sakti hain, music ya shor ho to bekaar ho sakta hai): " + _tr + "\nIse 'Jo likha ya bola dikha' hisse mein bola hua maan kar use karo. Agar yeh video se match na kare ya bekaar lage to ignore karo."
'''
oldB = "_call_video_native(body.message, videos[0])"
newB = "_call_video_native(_vmsg, videos[0])"
oldC = "        raw = _call_vision_v2(body.message, images)"
newC = "        raw = _call_vision_v2(_vmsg if videos else body.message, images)"
oldD = "Tum aawaaz nahi sun sakte, isliye bola hua sirf tab batao jab woh likha dikhe."
newD = "Tum aawaaz seedha nahi sun sakte; bola hua sirf tab batao jab woh likha dikhe, ya jab 'AAWAAZ KA TRANSCRIPT' diya gaya ho (tab use bola hua maano)."

cnt = [s.count(x) for x in (a, oldA, oldB, oldC, oldD)]
if cnt != [1, 1, 1, 1, 1]:
    print("audio: lines nahi mili, kuch nahi badla", cnt)
    raise SystemExit
s = s.replace(a, helper + a).replace(oldA, newA).replace(oldB, newB).replace(oldC, newC).replace(oldD, newD)
open(p, "w", encoding="utf-8").write(s)
print("audio: patch lag gaya")
