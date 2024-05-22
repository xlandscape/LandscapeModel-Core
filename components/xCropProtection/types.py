import datetime
import typing
import random

class Time:

    def __init__(self, hour: int, minute: int) -> None:
        self._hour = hour
        self._minute = minute

    @property
    def Hour(self) -> int:
        return self._hour

    @Hour.setter
    def Hour(self, value: int) -> None:
        self._hour = value    

    @property
    def Minute(self) -> int:
        return self._minute

    @Minute.setter
    def Minute(self, value: int) -> None:
        self._minute = value    

    def __le__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            hour = int((other - int(other)) * 24)
            minute = int((other - int(other) - hour / 24) * 60)
            return hour > self._hour or (hour == self._hour and minute > self._minute)
        return False

    def __ge__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            hour = int((other - int(other)) * 24)
            minute = int((other - int(other) - hour / 24) * 60)
            return hour < self._hour or (hour == self._hour and minute < self._minute)
        return False

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            hour = int((other - int(other)) * 24)
            minute = int((other - int(other) - hour / 24) * 60)
            return hour == self._hour and minute == self._minute
        return False

    def toordinal(self) -> float:
        return self._hour / 24 + self._minute / (24 * 60)

class TimeSpan:

    def __init__(self, start: Time, end: Time) -> None:
        self._start = start
        self._end = end

    @property
    def Start(self) -> Time:
        return self._start

    @Start.setter
    def Start(self, value: Time) -> None:
        self._start = value    

    @property
    def End(self) -> Time:
        return self._end

    @End.setter
    def End(self, value: Time) -> None:
        self._end = value

    def is_within(self, day: typing.Union[float, int]) -> bool:
        return day >= self._start and day <= self._end

    def sample(self) -> Time:
        random_time = random.uniform(self._start.toordinal(), self._end.toordinal())
        hour = int(random_time * 24)
        minute = int((random_time - hour / 24) * 60)
        return Time(hour, minute)

class MonthDay:

    def __init__(self, month: int, day: int) -> None:
        self._month = month
        self._day = day

    @property
    def Month(self) -> int:
        return self._month

    @Month.setter
    def Month(self, value: int) -> None:
        self._month = value    

    @property
    def Day(self) -> int:
        return self._day

    @Day.setter
    def Day(self, value: int) -> None:
        self._day = value    

    def __le__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            date = datetime.datetime.fromordinal(int(other))
            return date.month > self._month or (date.month == self._month and date.day > self._day)
        return False

    def __ge__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            date = datetime.datetime.fromordinal(int(other))
            return date.month < self._month or (date.month == self._month and date.day < self._day)
        return False

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            date = datetime.datetime.fromordinal(int(other))
            return date.month == self._month and date.day == self._day
        return False

    def toordinal(self, year: int) -> int:
        return datetime.datetime(year, self._month, self._day).toordinal()

class MonthDaySpan:

    def __init__(self, start: MonthDay, end: MonthDay) -> None:
        self._start = start
        self._end = end

    @property
    def Start(self) -> MonthDay:
        return self._start

    @Start.setter
    def Start(self, value: MonthDay) -> None:
        self._start = value    

    @property
    def End(self) -> MonthDay:
        return self._end

    @End.setter
    def End(self, value: MonthDay) -> None:
        self._end = value

    def is_within(self, day: typing.Union[float, int]) -> bool:
        return day >= self._start and day <= self._end

    def sample(self) -> MonthDay:
        random_month_day = random.randint(self._start.toordinal(1), self._end.toordinal(1))
        date = datetime.date.fromordinal(random_month_day)
        return MonthDay(date.month, date.day)

class MonthDayTime:

    def __init__(self, month: int, day: int, hour: int, minute: int) -> None:
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute

    @property
    def Month(self) -> int:
        return self._month

    @Month.setter
    def Month(self, value: int) -> None:
        self._month = value    

    @property
    def Day(self) -> int:
        return self._day

    @Day.setter
    def Day(self, value: int) -> None:
        self._day = value    

    @property
    def Hour(self) -> int:
        return self._hour

    @Hour.setter
    def Hour(self, value: int) -> None:
        self._hour = value    

    @property
    def Minute(self) -> int:
        return self._minute

    @Minute.setter
    def Minute(self, value: int) -> None:
        self._minute = value    

    def __le__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            date = datetime.datetime.fromordinal(int(other))
            hour = int((other - int(other)) * 24)
            minute = int((other - int(other) - hour / 24) * 60)
            return date.month > self._month or (date.month == self._month and date.day > self._day) or \
                (date.month == self._month and date.day == self._day and hour > self._hour) or \
                    (date.month == self._month and date.day == self._day and hour == self._hour and minute > self._minute)
        return False

    def __ge__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            date = datetime.datetime.fromordinal(int(other))
            hour = int((other - int(other)) * 24)
            minute = int((other - int(other) - hour / 24) * 60)
            return date.month < self._month or (date.month == self._month and date.day < self._day) or \
                (date.month == self._month and date.day == self._day and hour < self._hour) or \
                    (date.month == self._month and date.day == self._day and hour == self._hour and minute < self._minute)
        return False

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            date = datetime.datetime.fromordinal(int(other))
            hour = int((other - int(other)) * 24)
            minute = int((other - int(other) - hour / 24) * 60)
            return date.month == self._month and date.day == self._day and hour == self._hour and minute == self._minute
        return False

    def toordinal(self, year: int) -> float:
        return datetime.datetime(year, self._month, self._day, self._hour, self._minute).toordinal() + self._hour / 24 + self._minute / (24 * 60)

class MonthDayTimeSpan:

    def __init__(self, start: MonthDayTime, end: MonthDayTime) -> None:
        self._start = start
        self._end = end

    @property
    def Start(self) -> MonthDayTime:
        return self._start

    @Start.setter
    def Start(self, value: MonthDayTime) -> None:
        self._start = value    

    @property
    def End(self) -> MonthDayTime:
        return self._end

    @End.setter
    def End(self, value: MonthDayTime) -> None:
        self._end = value

    def is_within(self, day: typing.Union[float, int]) -> bool:
        return day >= self._start and day <= self._end

    def sample(self) -> MonthDayTime:
        random_month_day_time = random.uniform(self._start.toordinal(), self._end.toordinal())
        date = datetime.date.fromordinal(int(random_month_day_time))
        time = (random_month_day_time - int(random_month_day_time))
        hour = int(time * 24)
        minute =  int((time - hour / 24) * 60)
        return MonthDayTime(date.month, date.day, hour, minute)

class Date:

    def __init__(self, year: int, month: int, day: int) -> None:
        self._year = year
        self._month = month
        self._day = day

    @property
    def Year(self) -> int:
        return self._year

    @Year.setter
    def Year(self, value: int) -> None:
        self._year = value    

    @property
    def Month(self) -> int:
        return self._month

    @Month.setter
    def Month(self, value: int) -> None:
        self._month = value    

    @property
    def Day(self) -> int:
        return self._day

    @Day.setter
    def Day(self, value: int) -> None:
        self._day = value    

    def __le__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            date = datetime.datetime.fromordinal(int(other))
            return date.year > self._year or (date.year == self._year and date.month > self._month) or \
                (date.year == self._year and date.month == self._month and date.day > self._day)
        return False

    def __ge__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            date = datetime.datetime.fromordinal(int(other))
            return date.year < self._year or (date.year == self._year and date.month < self._month) or \
                (date.year == self._year and date.month == self._month and date.day < self._day)
        return False

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            date = datetime.datetime.fromordinal(int(other))
            return date.year == self._year and date.month == self._month and date.day == self._day
        return False

    def toordinal(self) -> int:
        return datetime.date(self._year, self._month, self._day).toordinal()

class DateSpan:

    def __init__(self, start: Date, end: Date) -> None:
        self._start = start
        self._end = end

    @property
    def Start(self) -> Date:
        return self._start

    @Start.setter
    def Start(self, value: Date) -> None:
        self._start = value    

    @property
    def End(self) -> Date:
        return self._end

    @End.setter
    def End(self, value: Date) -> None:
        self._end = value

    def is_within(self, day: typing.Union[float, int]) -> bool:
        return day >= self._start and day <= self._end

    def sample(self) -> Date:
        random_date = random.randint(datetime.date(self._start.Year, self._Y))
        date = datetime.date.fromordinal(random_date)
        return Date(date.year, date.month, date.day)
