from .session import Session

class Stack(object):

    def __init__(self, **kwargs):
        self.__session = Session(**kwargs)
