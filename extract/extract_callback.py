import csv


class ScrapeCallback(object):
    """docstring for ScrapeCallback"""
    def __init__(self):
        self.writer = csv.writer(open('call.csv', 'a'))
