class SaathiVoiceEngine:
    def __init__(self):
        self.name = "Saathi Voice"

    def status(self):
        return {
            "name": self.name,
            "status": "ready",
            "model": "custom"
        }


if __name__ == "__main__":
    engine = SaathiVoiceEngine()
    print(engine.status())
