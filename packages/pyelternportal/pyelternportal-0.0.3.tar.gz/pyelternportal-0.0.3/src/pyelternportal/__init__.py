"""Elternprotal API."""

from __future__ import annotations

import aiohttp
import bs4
import datetime
import logging
import pytz
import re
import socket
from typing import Any, Dict
import urllib.parse

from .const import (
    DEFAULT_REGISTER_START_MAX,
    DEFAULT_REGISTER_START_MIN,
    SCHOOL_SUBJECTS,
)

from .exception import (
    BadCredentialsException,
    CannotConnectException,
    PupilListException,
    ResolveHostnameException,
)

from .appointment import Appointment
from .lesson import Lesson
from .letter import Letter
from .poll import Poll
from .pupil import Pupil
from .register import Register
from .sicknote import SickNote

_LOGGER = logging.getLogger(__name__)

type ConfigType = Dict[str, str]
type OptionType = Dict[str, Any]
type PupilListType = Dict[Pupil]

class ElternPortalAPI:
    """API to retrieve the data."""

    def __init__(self):
        """Initialize the API."""

        self.timezone = pytz.timezone("Europe/Berlin")
        self.BeautifulSoupParser = "html5lib"

        # set_config
        self.school: str = None
        self.username: str = None
        self.password: str = None
        self.hostname: str = None
        self.base_url: str = None

        # set_option
        self.appointment: bool = False
        self.lesson: bool = False
        self.letter: bool = False
        self.poll: bool = False
        self.register: bool = False
        self.sicknote: bool = False

        # set_option_register
        self.register_start_min: int = DEFAULT_REGISTER_START_MIN
        self.register_start_max: int = DEFAULT_REGISTER_START_MAX

        # async_validate_config
        self.ip: str = None
        self.session: aiohttp.ClientSession = None
        self.csrf: str = None
        self.school_name: str = None

        self.pupils: PupilListType = {}

    def set_config(self, school: str, username: str, password: str):
        """Initialize the config."""
        school = (
            school.lower()
            .strip()
            .removeprefix("https://")
            .removeprefix("http://")
            .removesuffix("/")
            .removesuffix(".eltern-portal.org")
        )

        if not re.match(r"^[A-Za-z0-9]{1,10}$", school):
            message = '"school" is wrong: one to ten alpha-numeric characters'
            raise BadCredentialsException(message)

        username = username.lower().strip()
        password = password.strip()
        hostname = school + ".eltern-portal.org"
        base_url = "https://" + hostname + "/"

        self.school = school
        self.username = username
        self.password = password
        self.hostname = hostname
        self.base_url = base_url

    def set_config_data(self, config: ConfigType) -> None:
        """Initialize the config data."""

        school = config.get("school")
        username = config.get("username")
        password = config.get("password")
        self.set_config(school, username, password)

    def set_option(
        self,
        appointment: bool = False,
        lesson: bool = False,
        letter: bool = False,
        poll: bool = False,
        register: bool = False,
        sicknote: bool = False,
    ) -> None:
        """Initialize the option."""

        self.appointment: bool = appointment
        self.lesson: bool = lesson
        self.letter: bool = letter
        self.poll: bool = poll
        self.register: bool = register
        self.sicknote: bool = sicknote

    def set_option_register(
        self,
        register_start_min: int = DEFAULT_REGISTER_START_MIN,
        register_start_max: int = DEFAULT_REGISTER_START_MAX,
    ) -> None:
        """Initialize the option register."""

        self.register_start_min: int = register_start_min
        self.register_start_max: int = register_start_max

    def set_option_data(self, option: OptionType) -> None:
        """Initialize the option data."""

        appointment: bool = option.get("appointment", False)
        lesson: bool = option.get("lesson", False)
        letter: bool = option.get("letter", False)
        poll: bool = option.get("poll", False)
        register: bool = option.get("register", False)
        sicknote: bool = option.get("sicknote", False)

        register_start_min: int = option.get(
            "register_start_min", DEFAULT_REGISTER_START_MIN
        )
        register_start_max: int = option.get(
            "register_start_max", DEFAULT_REGISTER_START_MAX
        )

        self.set_option(appointment, lesson, letter, poll, register, sicknote)
        self.set_option_register(register_start_min, register_start_max)

    async def async_validate_config(self):

        _LOGGER.debug(f"Try to resolve hostname {self.hostname}")
        try:
            self.ip = socket.gethostbyname(self.hostname)
        except socket.gaierror:
            message = f"Cannot resolve hostname {self.hostname}"
            _LOGGER.exception(message)
            raise ResolveHostnameException(message)
        _LOGGER.debug(f"Ip address is {self.ip}")

        async with aiohttp.ClientSession(self.base_url) as self.session:
            await self.async_base()
            #await self.async_login()
            #await self.async_logout()

    async def async_update(self) -> None:
        """Elternportal start page."""

        async with aiohttp.ClientSession(self.base_url) as self.session:

            await self.async_base()
            await self.async_login()

            for pupil in self.pupils.values():
                self.pupil_id = pupil["id"]
                await self.async_set_child()

                count = 0
                if self.section_appointments:
                    await self.async_appointment()
                    count += len(pupil["appointments"])

                if self.section_lessons:
                    await self.async_lesson()
                    count += len(pupil["lessons"])

                if self.section_letters:
                    await self.async_letter()
                    count += len(pupil["letters"])

                if self.section_polls:
                    await self.async_poll()
                    count += len(pupil["polls"])

                if self.section_registers:
                    await self.async_register()
                    count += len(pupil["registers"])

                if self.section_sicknotes:
                    await self.async_sicknote()
                    count += len(pupil["sicknotes"])

                pupil["native_value"] = count
                pupil["last_update"] = datetime.datetime.now()

            await self.async_logout()
            self.last_update = datetime.datetime.now()

    async def async_base(self) -> None:
        """Elternportal base."""

        url = "/"
        _LOGGER.debug(f"base.url={url}")
        async with self.session.get(url) as response:
            if response.status != 200:
                message = f"base.status={response.status}"
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            html = await response.text()
            if "Dieses Eltern-Portal existiert nicht" in html:
                message = f"The elternportal {self.base_url} does not exist, most likely you have entered the name of the school incorrectly."
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            soup = bs4.BeautifulSoup(html, self.BeautifulSoupParser)

            try:
                tag = soup.find("input", {"name": "csrf"})
                csrf = tag["value"]
                self.csrf = csrf
            except TypeError:
                message = "The 'input' tag with the name 'csrf' could not be found."
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            try:
                tag = soup.find("h2", {"id": "schule"})
                school_name = tag.get_text()
                self.school_name = school_name
            except TypeError:
                message = "The 'h2' tag with the id 'schule' could not be found."
                _LOGGER.exception(message)
                raise CannotConnectException(message)

    async def async_login(self) -> None:
        """Elternportal login."""

        url = "/includes/project/auth/login.php"
        _LOGGER.debug(f"login.url={url}")
        login_data = {
            "csrf": self.csrf,
            "username": self.username,
            "password": self.password,
            "go_to": "",
        }
        async with self.session.post(url, data=login_data) as response:
            if response.status != 200:
                message = f"login.status={response.status}"
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            html = await response.text()
            soup = bs4.BeautifulSoup(html, self.BeautifulSoupParser)

            tag = soup.select_one(".pupil-selector")
            if tag is None:
                raise BadCredentialsException()

            pupils: PupilListType = {}
            tags = soup.select(".pupil-selector select option")
            if not tags:
                raise PupilListException()

            for tag in tags:
                try:
                    pupil_id = tag["value"]
                except:
                    message = (
                        "The 'value' atrribute of a pupil option could not be found."
                    )
                    raise PupilListException()

                try:
                    fullname = tag.get_text().strip()
                except:
                    message = "The 'text' of a pupil option could not be found."
                    raise PupilListException()

                pupil = Pupil(pupil_id, fullname)
                pupils[pupil_id] = pupil

            self.pupils = pupils

    async def async_set_child(self) -> None:
        """Elternportal set child."""

        url = "/api/set_child.php?id=" + self.pupil_id
        _LOGGER.debug(f"set_child.url={url}")
        async with self.session.post(url) as response:
            if response.status != 200:
                _LOGGER.debug(f"set_child.status={response.status}")

    async def async_appointment(self) -> None:
        """Elternportal appointment."""

        url = "/api/ws_get_termine.php"
        _LOGGER.debug(f"appointment.url={url}")
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug(f"appointment.status={response.status}")

            appointments = []
            # process malformed JSON response with parameter content_type
            json = await response.json(content_type="text/html")
            for result in json["result"]:
                start = int(str(result["start"])[0:-3])
                start = datetime.datetime.fromtimestamp(start, self.timezone).date()
                end = int(str(result["end"])[0:-3])
                end = datetime.datetime.fromtimestamp(end, self.timezone).date()

                appointment = Appointment(
                    result["id"],
                    result["title"],
                    result["title_short"],
                    result["class"],
                    start,
                    end,
                )
                appointments.append(appointment)

            self.pupils[self.pupil_id]["appointments"] = appointments
            
    async def async_lesson(self) -> None:
        """Elternportal lesson."""

        url = "/service/stundenplan"
        _LOGGER.debug(f"lesson.url={url}")
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug(f"lesson.status={response.status}")
            html = await response.text()
            soup = bs4.BeautifulSoup(html, self.BeautifulSoupParser)

            lessons = []
            table_rows = soup.select("#asam_content div.table-responsive table tr")
            for table_row in table_rows:
                table_cells = table_row.select("td")

                if len(table_cells) == 6:
                    # Column 0
                    lines = table_cells[0].find_all(string=True)
                    number = lines[0] if len(lines) > 0 else ""
                    # time = lines[1] if len(lines) > 1 else ""

                    # Column 1-5: Monday to Friday
                    for weekday in range(1, 5):
                        span = table_cells[weekday].select_one("span span")
                        if span is not None:
                            lines = span.find_all(string=True)
                            subject = lines[0].strip() if len(lines) > 0 else ""
                            room = lines[1].strip() if len(lines) > 1 else ""

                            if subject != "":
                                lesson = Lesson(weekday, number, subject, room)
                                lessons.append(lesson)

            self.pupils[self.pupil_id]["lessons"] = lessons

    async def async_letter(self) -> None:
        """Elternportal letter."""

        letters = []
        url = "/aktuelles/elternbriefe"
        _LOGGER.debug(f"letter.url={url}")
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug(f"letter.status={response.status}")
            html = await response.text()
            soup = bs4.BeautifulSoup(html, self.BeautifulSoupParser)

            tags = soup.select(".link_nachrichten")
            for tag in tags:
                try:
                    match = re.search(r"\d+", tag.get("onclick"))
                    letter_id = match[0]
                except:
                    letter_id = "0"

                try:
                    attachment = tag.name == "a"
                except:
                    attachment = False

                try:
                    match = re.search(
                        r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}", tag.get_text()
                    )
                    sent = datetime.datetime.strptime(match[0], "%d.%m.%Y %H:%M:%S")
                    sent = self.timezone.localize(sent)
                except:
                    sent = None

                try:
                    cell = soup.find("td", {"id": "empf_" + letter_id})
                    new = cell.get_text() == "Empfang noch nicht bestätigt."
                    try:
                        cell2 = cell.find_previous_sibling()
                        number = cell2.get_text()
                    except:
                        number = "???"
                except:
                    new = True
                    number = "???"

                try:
                    cell = tag.find("h4")
                    subject = cell.get_text()
                except:
                    subject = None

                try:
                    cell = tag.parent

                    try:
                        span = cell.select_one("span[style='font-size: 8pt;']")
                        text = span.get_text()
                        liste = text.split("Klasse/n: ")
                        liste = [x for x in liste if x]
                        distribution = ", ".join(liste)
                    except:
                        distribution = None

                    try:
                        lines = cell.find_all(string=True)

                        description = ""
                        skip = True
                        for i in range(1, len(lines)):
                            line = lines[i].replace("\r", "").replace("\n", "")
                            if not skip:
                                description += line + "\n"
                            if line.startswith("Klasse/n: "):
                                skip = False
                    except:
                        description = None

                except:
                    distribution = None
                    description = None

                letter = Letter(
                    letter_id=letter_id,
                    number=number,
                    sent=sent,
                    new=new,
                    attachment=attachment,
                    subject=subject,
                    distribution=distribution,
                    description=description,
                )
                letters.append(letter)

        self.pupils[self.pupil_id]["letters"] = letters


    async def async_poll(self) -> None:
        """Elternportal poll."""

        polls = []
        url = "/aktuelles/umfragen"
        _LOGGER.debug(f"poll.url={url}")
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug(f"poll.status={response.status}")
            html = await response.text()
            soup = bs4.BeautifulSoup(html, self.BeautifulSoupParser)

            try:
                base_tag = soup.find("base")
                baseurl = base_tag["href"] if base_tag else url
            except:
                baseurl = ""

            rows = soup.select("#asam_content div.row.m_bot")
            for row in rows:
                try:
                    tag = row.select_one("div div:nth-child(1) a.umf_list")
                    title = tag.get_text()
                    href = urllib.parse.urljoin(baseurl, tag["href"])
                except:
                    title = None
                    href = None

                try:
                    tag = row.select_one("div div:nth-child(1) a[title='Anhang']")
                    attachment = tag is not None
                except:
                    attachment = False

                try:
                    tag = row.select_one("div div:nth-child(2)")
                    match = re.search(r"\d{2}\.\d{2}\.\d{4}", tag.get_text())
                    end = datetime.datetime.strptime(match[0], "%d.%m.%Y").date()
                except:
                    end = None

                try:
                    tag = row.select_one("div div:nth-child(3)")
                    match = re.search(r"\d{2}\.\d{2}\.\d{4}", tag.get_text())
                    vote = datetime.datetime.strptime(match[0], "%d.%m.%Y").date()
                except:
                    vote = None

                if href is None:
                    detail = None
                else:
                    async with self.session.get(href) as response2:
                        html2 = await response2.text()
                        soup2 = bs4.BeautifulSoup(html2, self.BeautifulSoupParser)

                        try:
                            div2 = soup2.select_one(
                                "#asam_content form.form-horizontal div.form-group:nth-child(3)"
                            )
                            detail = div2.get_text()
                        except:
                            detail = None

                poll = Poll(
                    title=title,
                    href=href,
                    attachment=attachment,
                    vote=vote,
                    end=end,
                    detail=detail,
                )
                polls.append(poll)

        self.pupils[self.pupil_id]["polls"] = polls

    async def async_register(self) -> None:
        """Elternportal register."""

        registers = []
        date_current = datetime.date.today() + datetime.timedelta(
            days=self.register_start_min
        )
        date_until = datetime.date.today() + datetime.timedelta(
            days=self.register_start_max
        )
        while date_current <= date_until:

            url = "/service/klassenbuch?cur_date=" + date_current.strftime("%d.%m.%Y")
            _LOGGER.debug(f"register.url={url}")
            async with self.session.get(url) as response:
                if response.status != 200:
                    _LOGGER.debug(f"register.status={response.status}")
                html = await response.text()
                soup = bs4.BeautifulSoup(html, self.BeautifulSoupParser)

                tags = soup.select("#asam_content table.table.table-bordered")
                for tag in tags:
                    table_cells = tag.select("th")
                    content = table_cells[1].get_text() if len(table_cells) > 1 else ""
                    subject = None
                    short = None
                    teacher = None
                    lesson = None
                    substitution = False
                    match = re.search(
                        r"(.*) - Lehrkraft: (.*) \((Einzel|Doppel)stunde(, Vertretung)?\)",
                        content,
                    )
                    if match is not None:
                        subject = match[1].replace("Fach: ", "")
                        teacher = match[2]
                        lesson = (
                            match[3]
                            .replace("Einzel", "single")
                            .replace("Doppel", "double")
                        )
                        substitution = match[4] is not None

                    for school_subject in SCHOOL_SUBJECTS:
                        if school_subject["Name"] == subject:
                            short = school_subject["Short"]

                    table_cells = tag.select("td")
                    rtype = table_cells[0].get_text() if len(table_cells) > 0 else ""
                    rtype = rtype.replace("Hausaufgabe", "homework")

                    lines = table_cells[1].find_all(string=True)
                    description = lines[0] if len(lines) > 0 else ""

                    if description != "Keine Hausaufgabe eingetragen.":
                        date_completion = date_current
                        if len(lines) > 2:
                            match = re.search(r"\d{2}\.\d{2}\.\d{4}", lines[2])
                            if match is not None:
                                date_completion = datetime.datetime.strptime(
                                    match[0], "%d.%m.%Y"
                                ).date()

                        register = Register(
                            subject=subject,
                            short=short,
                            teacher=teacher,
                            lesson=lesson,
                            substitution=substitution,
                            type=rtype,
                            start=date_current,
                            completion=date_completion,
                            description=description,
                        )
                        registers.append(register)

            date_current += datetime.timedelta(days=1)

        self.pupils[self.pupil_id]["registers"] = registers

    async def async_sicknote(self) -> None:
        """Elternportal sick note."""

        sicknotes = []
        url = "/meldungen/krankmeldung"
        _LOGGER.debug(f"sicknote.url={url}")
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug(f"sicknote.status={response.status}")
            html = await response.text()

            soup = bs4.BeautifulSoup(html, self.BeautifulSoupParser)

            rows = soup.select("#asam_content table.ui.table tr")
            for row in rows:
                cells = row.select("td")

                # link
                try:
                    tag = cells[0].find("a")
                    link = tag["href"]
                except TypeError:
                    link = None

                # query
                try:
                    result = urllib.parse.urlparse(link)
                    query = urllib.parse.parse_qs(result.query)
                except:
                    query = None

                # df -> start
                try:
                    df = int(query["df"][0])
                    start = datetime.datetime.fromtimestamp(
                        df, self.timezone
                    ).date()
                except KeyError:
                    try:
                        lines = cells[1].find_all(string=True)
                        match = re.search(r"\d{2}\.\d{2}\.\d{4}", lines[0])
                        start = datetime.datetime.strptime(
                            match[0], "%d.%m.%Y"
                        ).date()
                    except TypeError:
                        start = None

                # dt -> end
                try:
                    dt = int(query["dt"][0])
                    end = datetime.datetime.fromtimestamp(dt, self.timezone).date()
                except KeyError:
                    end = start

                # k -> comment
                try:
                    comment = str(query["k"][0])
                except KeyError:
                    try:
                        comment = cells[2].get_text()
                    except IndexError:
                        comment = None

                sicknote = SickNote(
                    start=start,
                    end=end,
                    comment=comment,
                )
                sicknotes.append(sicknote)

        self.pupils[self.pupil_id]["sicknotes"] = sicknotes

    async def async_logout(self) -> None:
        """Elternportal logout."""

        url = "/logout"
        _LOGGER.debug(f"logout.url={url}")
        async with self.session.get(url) as response:
            if response.status != 200:
                message = f"logout.status={response.status}"
                _LOGGER.exception(message)
                raise CannotConnectException(message)
