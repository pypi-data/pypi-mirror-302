import datetime

class Letter(object):

    def __init__(
        self,
        letter_id: int,
        number: str,
        sent: datetime.datetime,
        new: bool,
        attachment: bool,
        subject: str,
        distribution: str,
        description: str,
    ):

        self.letter_id: str = letter_id
        self.number: str = number
        self.sent: datetime.datetime = sent
        self.new: bool = new
        self.attachment: bool = attachment
        self.subject: str = subject
        self.distribution: str = distribution
        self.description: str = description
