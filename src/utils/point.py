class Point:

    __slots__ = ('histogram', 'frame')

    def __init__(self, histogram, frame):
        self.histogram = histogram
        self.frame = frame

    def __repr__(self):
        return f'{self.histogram}'