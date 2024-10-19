import datetime


class SickNote(object):

    def __init__(
        self,
        start: datetime.date,
        end: datetime.date,
        comment: str,
    ):

        self.start: datetime.date = start
        self.end: datetime.date = end
        self.comment: str = comment
