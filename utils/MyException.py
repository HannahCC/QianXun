__author__ = 'Hannah'


class DataError(Exception):
    def __init__(self, data):
        Exception.__init__(self)
        self.data = data
