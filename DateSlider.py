import datetime
import math
from dash import dcc
from datetime import date, datetime, timedelta


class DateSlider:
    __start_date = None
    __end_date = None
    __slice_size = None
    __slice_resolution = None
    __id = None
    __slider = None
    __marks = None
    __length = None

    def __init__(self, id: str, start_date: date, end_date: date, slice_size: int, slice_resolution: int):
        self.__id = id
        self.update_slider(start_date, end_date, slice_size, slice_resolution)

    def update_slider(self, start_date: date, end_date: date, slice_size: int, slice_resolution: int):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__slice_size = slice_size
        self.__slice_resolution = slice_resolution

        self.__do_stuff()

    def __do_stuff(self):
        if self.__slice_resolution == 1:
            num_of_years = self.__end_date.year - self.__start_date.year
            num_of_marks = math.floor(num_of_years / self.__slice_size)

            self.__length = num_of_marks + 1

            self.__marks = {}
            for i in range(num_of_marks + 1):
                current_year = self.__start_date.year + (i * self.__slice_size)
                date_mark = str(current_year)
                self.__marks.update({i: {'label': date_mark,
                                       'style': {'writing-mode': 'vertical-rl',
                                                 'text-orientation': 'sideways',
                                                 'height': '100px'
                                                 }
                                         }
                                     }
                                    )

            self.__slider = dcc.RangeSlider(id=self.__id,
                                            min=0,
                                            max=num_of_marks,
                                            step=1, allowCross=False,
                                            marks=self.__marks, value=[0, num_of_marks + 1])

        elif self.__slice_resolution == 2:
            num_of_years_between = self.__end_date.year - self.__start_date.year - 1
            num_of_months = 12 - self.__start_date.month + 1
            num_of_months += 12 * num_of_years_between
            num_of_months += self.__end_date.month

            whole_marks = math.floor(num_of_months / self.__slice_size)
            num_of_marks = whole_marks

            self.__length = num_of_marks

            self.__marks = {}
            current_month = self.__start_date.month
            current_year = self.__start_date.year
            for i in range(num_of_marks):
                date_mark = str(current_month) + " - " + str(current_year)
                self.__marks.update({i: {'label': date_mark,
                                       'style': {'writing-mode': 'vertical-rl',
                                                 'text-orientation': 'sideways',
                                                 'height': '100px'
                                                 }
                                         }
                                     }
                                    )
                current_month += 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1

            self.__slider = dcc.RangeSlider(id=self.__id,
                                            min=0,
                                            max=num_of_marks - 1,
                                            step=1, allowCross=False,
                                            marks=self.__marks)

        elif self.__slice_resolution == 3:
            num_of_days = (self.__end_date - self.__start_date).days
            whole_marks = math.floor(num_of_days / self.__slice_size)
            num_of_marks = whole_marks + 1

            self.__length = num_of_marks

            self.__marks = {}
            for i in range(num_of_marks):
                current_date = self.__start_date + timedelta(days=(self.__slice_size * i))
                date_mark = (str(current_date.day) + " - " + str(current_date.month) + " - " + str(current_date.year))
                self.__marks.update({i: {'label': date_mark,
                                       'style': {'writing-mode': 'vertical-rl',
                                                 'text-orientation': 'sideways',
                                                 'height': '100px'
                                                 }
                                         }
                                     }
                                    )

            self.__slider = dcc.RangeSlider(id=self.__id,
                                            min=0,
                                            max=num_of_marks - 1,
                                            step=1, allowCross=False,
                                            marks=self.__marks)
        else:
            print("ERROR: INVALID SLICE RESOLUTION - SHOULD BE \"1 - Year\", \"2 - Month\" OR \"3 - Day\"")

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date

    def get_slice_resolution(self):
        return self.__slice_resolution

    def get_slice_size(self):
        return self.__slice_size

    def get_marks(self):
        return self.__marks

    def get_length(self):
        return self.__length

    def get_slider(self):
        return self.__slider

    def get_date_at_pos(self, pos: int):
        date_string = str(self.__marks[pos]['label'])
        if self.__slice_resolution == 1:
            return datetime.strptime(date_string, '%Y').date()

        elif self.__slice_resolution == 2:
            return datetime.strptime(date_string, '%m - %Y').date()

        elif self.__slice_resolution == 3:
            return datetime.strptime(date_string, '%d - %m - %Y').date()

        return None
