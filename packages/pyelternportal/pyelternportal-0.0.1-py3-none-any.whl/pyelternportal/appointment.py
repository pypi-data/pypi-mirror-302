import datetime

class Appointment(object):
    def __init__(
        self,
        appointment_id: str,
        title: str,
        short: str,
        classname: str,
        start: datetime.date,
        end: datetime.date,
    ):

        self.appointment_id: str = appointment_id
        self.title: str = title
        self.short: str = short
        self.classname: str = classname
        self.start: datetime.date = start
        self.end: datetime.date = end
