import datetime


class Poll(object):

    def __init__(
        self,
        title: str,
        href: str,
        attachment: bool,
        vote: datetime.date,
        end: datetime.date,
        detail: str,
    ):

        self.title: str = title
        self.href: str = href
        self.attachment: bool = attachment
        self.vote: datetime.datetime = vote
        self.end: datetime.datetime = end
        self.detail: str = detail
