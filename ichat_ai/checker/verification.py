"""Antim satyapan: khaali ya kharab jawab kabhi user tak nahi jayega, tab asli jawab lautta hai."""


def approve(original, final):
    if not isinstance(final, str) or not final.strip():
        return original
    return final
