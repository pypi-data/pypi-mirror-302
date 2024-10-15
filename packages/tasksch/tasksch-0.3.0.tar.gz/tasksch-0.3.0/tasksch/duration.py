import re
from .errors import TaskSchdError


duration_rx = re.compile(
    r"""
    ^P
    ((?P<years>\d+)Y)?
    ((?P<months>\d+)M)?
    ((?P<days>\d+)D)?
    T
    ((?P<hours>\d+)H)?
    ((?P<minutes>\d+)M)?
    ((?P<seconds>\d+)S)?
    $
    """,
    re.VERBOSE,
)


class Duration:
    """
    Taskschd time duration format:

        PnYnMnDTnHnMnS

    P = period
    T = time
    Y, M, D, H, M, S = year, month, day, hour, minute, second

    Examples:
        P3DT = 3 days
        PT5M = 5 minutes
        P3DT3H15M = 3 days, 3 hours and 15 minutes
        pT0S = run indefinitely

    """

    years: int | None
    months: int | None
    days: int | None
    hours: int | None
    minutes: int | None
    seconds: int | None

    def __init__(
        self,
        years: int = None,
        months: int = None,
        days: int = None,
        hours: int = None,
        minutes: int = None,
        seconds: int = None,
    ):
        self.years = years
        self.months = months
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __eq__(self, other: "Duration") -> bool:
        return (
            self.years == other.years
            and self.months == other.months
            and self.days == other.days
            and self.hours == other.hours
            and self.minutes == other.minutes
            and self.seconds == other.seconds
        )

    def __str__(self) -> str:
        if self == INDEFINITE_DURATION:
            return "indefinitely"

        content = []

        def format(dval: int | None, name: str):
            if dval and dval == 1:
                return f"{dval} {name}"
            elif dval and dval > 1:
                return f"{dval} {name}s"

        if years := format(self.years, "year"):
            content.append(years)

        if months := format(self.months, "month"):
            content.append(months)

        if days := format(self.days, "day"):
            content.append(days)

        if hours := format(self.hours, "hour"):
            content.append(hours)

        if minutes := format(self.minutes, "minute"):
            content.append(minutes)

        if seconds := format(self.seconds, "second"):
            content.append(seconds)

        if len(content) == 0 and self.seconds == 0:
            content.append("indefinitely")

        return " ".join(content)

    @staticmethod
    def from_notation(src_txt: str) -> "Duration":
        if not src_txt:
            return Duration()
        if m := duration_rx.match(src_txt):
            kw = {}
            for key, value in m.groupdict().items():
                if value is None:
                    continue
                i = int(value)
                if i > 0 or key == "seconds" and i >= 0:
                    kw[key] = i
            return Duration(**kw)
        raise TaskSchdError(f"'{src_txt}' is an invalid Duration format.")

    def _period_notation(self) -> str:
        content = ["P"]
        if self.years and self.years > 0:
            content.append(f"{self.years}Y")
        if self.months and self.months > 0:
            content.append(f"{self.months}M")
        if self.days and self.days > 0:
            content.append(f"{self.days}D")
        return "".join(content)

    def _time_notation(self) -> str:
        content = ["T"]
        if self.hours and self.hours > 0:
            content.append(f"{self.hours}H")
        if self.minutes and self.minutes > 0:
            content.append(f"{self.minutes}M")
        if self.seconds and self.seconds > 0:
            content.append(f"{self.seconds}S")
        if len(content) > 1:
            return "".join(content)
        return ""

    def to_notation(self) -> str:
        if self == INDEFINITE_DURATION:
            return "PT0S"

        if self == EMPTY_DURATION:
            return ""

        content = []
        content.append(self._period_notation())
        content.append(self._time_notation())
        return "".join(content)


INDEFINITE_DURATION = Duration(seconds=0)
EMPTY_DURATION = Duration()
