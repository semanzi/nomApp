import datetime
import math
import dash
from dash import dcc
from datetime import date


class DateSlider:
    start_date = None
    end_date = None
    slice_size = None
    slice_resolution = None

    slider = None



    def __init__(self, start_date: date, end_date: date, slice_size: int, slice_resolution: str):
        self.start_date = start_date
        self.end_date = end_date
        self.slice_size = slice_size
        self.slice_resolution = slice_resolution

        self.update_slider(start_date, end_date, slice_size, slice_resolution)



    def update_slider(self, start_date: date, end_date: date, slice_size: int, slice_resolution: str):
        self.start_date = start_date
        self.end_date = end_date
        self.slice_size = slice_size
        self.slice_resolution = slice_resolution

        self.do_stuff()


    def do_stuff(self):
        if self.slice_resolution == "Year":
            num_of_years = self.end_date.year - self.start_date.year + 1


        elif self.slice_resolution == "Month":
            num_of_years_between = self.end_date.year - self.start_date.year - 1
            num_of_months = 12 - self.start_date.month + 1
            num_of_months += 12 * num_of_years_between
            num_of_months += self.end_date.month

            whole_marks = math.floor(num_of_months / self.slice_size)
            remainder = num_of_months % self.slice_size
            num_of_marks = whole_marks

            marks = {}
            current_month = self.start_date.month
            current_year = self.start_date.year
            for i in range(num_of_marks):
                current_month += i
                if current_month > 12:
                    current_month = 1
                    current_year += 1
                date_mark = str(current_month) + " - " + str(current_year)
                marks.update({i: {'label': date_mark,
                                  'style': {'writing-mode': 'vertical-rl',
                                            'text-orientation': 'sideways',
                                            'height': '100px'
                                            }
                                  }
                              }
                             )
            self.slider = dcc.RangeSlider(id='date_slider',
                                          min=0,
                                          max=num_of_marks,
                                          step=1, allowCross=False,
                                          marks=marks)


        elif self.slice_resolution == "Day":
            num_of_days = (self.end_date - self.start_date).days
            whole_marks = math.floor(num_of_days / self.slice_size)
            remainder = num_of_days % self.slice_size
            num_of_marks = whole_marks + 1
            marks = {}
            for i in range(num_of_marks):
                current_date = self.start_date + datetime.timedelta(days=self.slice_size*i)
                date_mark = (str(current_date.day) + " - " + str(current_date.month) + " - " + str(current_date.year))
                marks.update({i: {'label': date_mark,
                                  'style': {'writing-mode': 'vertical-rl',
                                            'text-orientation': 'sideways',
                                            'height': '100px'
                                            }
                                  }
                              }
                             )




            self.slider = dcc.RangeSlider(id='date_slider',
                                          min=0,
                                          max=num_of_marks,
                                          step=1, allowCross=False,
                                          marks=marks)



        else:
            print("ERROR: INVALID SLICE RESOLUTION - SHOULD BE \"Year\", \"Month\" OR \"Day\"")


    def get_slider(self):
        return self.slider
