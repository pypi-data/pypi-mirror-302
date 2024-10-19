import datetime

class Register(object):

    def __init__(
        self,
        subject: str,
        short: str,
        teacher: str,
        lesson: str,
        substitution: bool,
        type: str,
        start: datetime.date,
        completion: datetime.date,
        description: str,
    ):

        self.subject: str = subject
        self.short: str = short
        self.teacher: str = teacher
        self.lesson: str = lesson
        self.substitution: bool = substitution
        self.type: str = type
        self.start: datetime.date = start
        self.completion: datetime.date = completion
        self.description: str = description
