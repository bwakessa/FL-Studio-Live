from pyflp import Project
from pyflp.pattern import Note

import enum
from itertools import zip_longest

@enum.unique
class ChangeType(enum.Enum):
    INSERT = 1
    DELETE = 2
    UPDATE = 3

class ChangeLogEntry():

    def __init__(self, change_type: ChangeType, note: Note):
        pass

class ChangeLog():

    def __init__(self):
        pass





