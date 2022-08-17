import dash
from dash import dcc
from datetime import date


class DateSlider:
    slider = None
    min_marks = 2
    max_marks = 20

    def __init__(self, start_date: date, end_date: date, slice_size: int):
        self.update_slider(start_date, end_date, slice_size)


    def update_slider(self, start_date: date, end_date: date, slice_size: int):
        pass


    def get_slider(self):
        return self.slider


