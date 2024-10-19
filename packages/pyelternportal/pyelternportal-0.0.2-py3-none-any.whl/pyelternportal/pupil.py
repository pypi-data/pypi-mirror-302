import re
from typing import Dict, Sequence

from .appointment import Appointment
from .lesson import Lesson
from .letter import Letter
from .poll import Poll
from .register import Register
from .sicknote import SickNote


class Pupil(object):
    def __init__(self, pupil_id: str, fullname: str):

        try:
            match = re.search(r"^(\S+)\s+(.*)\s+\((\S+)\)$", fullname)
            firstname = match[1]
            lastname = match[2]
            classname = match[3]
        except:
            firstname = f"PID{pupil_id}"
            lastname = None
            classname = None

        self.pupil_id: str = pupil_id
        self.fullname: str = fullname
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.classname: str = classname

        self.appointments: Sequence = []
        self.lessons: Sequence = []
        self.letters: Sequence = []
        self.polls: Sequence = []
        self.registers: Sequence = []
        self.sicknotes: Sequence = []

    def get_id(self) -> str:
        return self.pupil_id

    def get_fullname(self) -> str:
        return self.fullname

    def get_firstname(self) -> str:
        return self.firstname

    def get_count(self) -> int:
        return (
            len(self.appointments)
            + len(self.lessons)
            + len(self.letters)
            + len(self.polls)
            + len(self.registers)
            + len(self.sicknotes)
        )

    def set_appointments(self, appointments: Sequence[Appointment]) -> None:
        self.appointments = appointments

    def get_appointments(self) -> Sequence[Appointment]:
        return self.appointments

    def set_lessons(self, lessons: Sequence[Lesson]) -> None:
        self.lessons = lessons

    def get_lessons(self) -> Sequence[Lesson]:
        return self.lessons

    def set_letters(self, letters: Sequence[Letter]) -> None:
        self.letters = letters

    def get_letters(self) -> Sequence[Letter]:
        return self.letters

    def set_polls(self, polls: Sequence[Poll]) -> None:
        self.polls = polls

    def get_polls(self) -> Sequence[Poll]:
        return self.polls

    def set_registers(self, registers: Sequence[Register]) -> None:
        self.registers = registers

    def get_registers(self) -> Sequence[Register]:
        return self.registers

    def set_sicknotes(self, sicknotes: Sequence[SickNote]) -> None:
        self.sicknotes = sicknotes

    def get_sicknotes(self) -> Sequence[SickNote]:
        return self.sicknotes


class Pupils(object):
    def __init__(self):
        self.pupils: Dict[Pupil] = {}

    def set_pupil(self, pupil: Pupil) -> None:
        self.pupils[pupil.pupil_id] = pupil

    def get_pupil(self, pupil_id: str) -> Pupil:
        return self.pupils[pupil_id]

    def set_pupil_appointments(
        self, pupil_id: str, appointments: Sequence[Appointment]
    ) -> None:
        self.pupils[pupil_id]["appointments"] = appointments

    def set_pupil_lessons(self, pupil_id: str, lessons: Sequence[Lesson]) -> None:
        self.pupils[pupil_id]["lessons"] = lessons

    def set_pupil_letters(self, pupil_id: str, letters: Sequence[Letter]) -> None:
        self.pupils[pupil_id]["letters"] = letters

    def set_pupil_polls(self, pupil_id: str, polls: Sequence[Poll]) -> None:
        self.pupils[pupil_id]["polls"] = polls

    def set_pupil_registers(self, pupil_id: str, registers: Sequence[Register]) -> None:
        self.pupils[pupil_id]["registers"] = registers

    def set_pupil_sicknotes(self, pupil_id: str, sicknotes: Sequence[SickNote]) -> None:
        self.pupils[pupil_id]["sicknotes"] = sicknotes
