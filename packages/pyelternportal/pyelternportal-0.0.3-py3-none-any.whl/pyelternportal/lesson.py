class Lesson(object):

    def __init__(
        self,
        weekday: int,
        number: str,
        subject: str,
        room: str,
    ):

        self.weekday: int = weekday
        self.number: str = number
        self.subject: str = subject
        self.room: str = room
