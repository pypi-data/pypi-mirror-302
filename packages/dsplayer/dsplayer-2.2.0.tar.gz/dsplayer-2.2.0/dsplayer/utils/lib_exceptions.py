class VoiceChaneError(Exception):
    def __init__(self, message: str = "Voice channel error"):
        self.message = message
        super().__init__(self.message)


class VoiceChaneNotFound(VoiceChaneError):
    pass


class VoiceChaneNotConnected(VoiceChaneError):
    pass


class VoiceChaneNotPlaying(VoiceChaneError):
    pass


class ConectionError(Exception):
    def __init__(self, message="Conection error"):
        self.message = message
        super().__init__(self.message)


class TrackError(Exception):
    def __init__(self, message: str = "Track error"):
        self.message = message
        super().__init__(self.message)


class TrackNotFound(TrackError):
    pass


class LibraryNotFound(Exception):
    def __init__(self, message: str = "Library not found"):
        self.message = message
        super().__init__(self.message)
