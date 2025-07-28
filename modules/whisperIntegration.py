import whisper
class whisper:
    def __init__(self):
        self.model = whisper.load_model("turbo")

    