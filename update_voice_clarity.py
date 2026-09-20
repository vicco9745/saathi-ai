"""
update_voice_clarity.py

Repo ROOT se chalao:
    python update_voice_clarity.py

Yeh phone ke available voices mein se sabse achhi wali (Google/online
voice, jo saaf aur natural sunayi deti hai) khud chunta hai — default
robotic/offline voice ki jagah. Saath hi thodi si slow speed set karta
hai (0.95x) jisse shabd zyada clear sunayi dete hain.
"""

from pathlib import Path
import sys

INDEX_HTML = Path("index.html")

# ── 1) Voice-picking helper ──

OLD_ANCHOR = '''            let recognition = null;
            let callActive = false;'''

NEW_ANCHOR = '''            let _cachedVoices = [];
            function _loadVoicesCache() {
                _cachedVoices = window.speechSynthesis.getVoices();
            }
            if ('speechSynthesis' in window) {
                _loadVoicesCache();
                window.speechSynthesis.onvoiceschanged = _loadVoicesCache;
            }
            function pickBestVoice(langCode) {
                const voices = _cachedVoices.length ? _cachedVoices : window.speechSynthesis.getVoices();
                const prefix = (langCode || 'hi-IN').split('-')[0].toLowerCase();
                const matching = voices.filter(v => v.lang && v.lang.toLowerCase().startsWith(prefix));
                if (matching.length === 0) return null;
                const google = matching.find(v => /google/i.test(v.name) && !/local/i.test(v.name));
                if (google) return google;
                const online = matching.find(v => v.localService === false);
                if (online) return online;
                return matching[0];
            }

            let recognition = null;
            let callActive = false;'''

# ── 2) Apply best voice + slower rate in the "Listen" button handler ──

OLD_LISTEN = '''                listenBtn.addEventListener('click', () => {
                    if (!('speechSynthesis' in window) || !message.text) return;
                    window.speechSynthesis.cancel();
                    const utter = new SpeechSynthesisUtterance(message.text);
                    utter.lang = 'hi-IN';
                    window.speechSynthesis.speak(utter);
                });'''

NEW_LISTEN = '''                listenBtn.addEventListener('click', () => {
                    if (!('speechSynthesis' in window) || !message.text) return;
                    window.speechSynthesis.cancel();
                    const utter = new SpeechSynthesisUtterance(message.text);
                    utter.lang = 'hi-IN';
                    const _bestVoice1 = pickBestVoice('hi-IN');
                    if (_bestVoice1) utter.voice = _bestVoice1;
                    utter.rate = 0.95;
                    utter.pitch = 1;
                    window.speechSynthesis.speak(utter);
                });'''

# ── 3) Apply best voice + slower rate in the call-mode speak() function ──

OLD_SPEAK_FN = '''            function speak(text, onEnd) {
                if (!('speechSynthesis' in window)) { if (onEnd) onEnd(); return; }
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance(text);
                utter.lang = 'hi-IN';
                utter.onend = () => { if (onEnd) onEnd(); };
                utter.onerror = () => { if (onEnd) onEnd(); };
                window.speechSynthesis.speak(utter);
            }'''

NEW_SPEAK_FN = '''            function speak(text, onEnd) {
                if (!('speechSynthesis' in window)) { if (onEnd) onEnd(); return; }
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance(text);
                utter.lang = 'hi-IN';
                const _bestVoice2 = pickBestVoice('hi-IN');
                if (_bestVoice2) utter.voice = _bestVoice2;
                utter.rate = 0.95;
                utter.pitch = 1;
                utter.onend = () => { if (onEnd) onEnd(); };
                utter.onerror = () => { if (onEnd) onEnd(); };
                window.speechSynthesis.speak(utter);
            }'''


def main():
    if not INDEX_HTML.exists():
        sys.exit(f"{INDEX_HTML} nahi mila. Repo ROOT se chalao.")

    source = INDEX_HTML.read_text(encoding="utf-8")

    if "pickBestVoice" in source:
        print("Voice clarity fix already lagi hai — kuch nahi badla.")
        return

    steps = [
        (OLD_ANCHOR, NEW_ANCHOR, "voice helper insert"),
        (OLD_LISTEN, NEW_LISTEN, "Listen button handler"),
        (OLD_SPEAK_FN, NEW_SPEAK_FN, "call-mode speak() function"),
    ]

    for old, new, label in steps:
        if old not in source:
            sys.exit(f"'{label}' anchor nahi mila. Mujhe fresh index.html bhejo.")

    for old, new, label in steps:
        source = source.replace(old, new, 1)

    INDEX_HTML.write_text(source, encoding="utf-8")
    print("Voice clarity fix add ho gayi. OK")
    print("Ab: git add . && git commit -m 'use clearer TTS voice' && git push")


if __name__ == "__main__":
    main()
