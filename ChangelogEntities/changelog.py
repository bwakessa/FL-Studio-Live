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
    """An entry of a ChangeLog representing a single edit of a note

    Attributes:
        change_type: The type of edit to the note in this entry
        note: The note being edited
        updates: the edits to <note>'s attributes; != None iff <change_type> = UPDATE
    """

    change_type: ChangeType
    note: Note
    updates: dict[any, dict[any, any]]

    def __init__(self, change_type: ChangeType, note: Note, updates: dict[any, dict[any, any]] = None):
        self.change_type = change_type
        self.note = note
        self.updates = updates

class ChangeLog():

    def __init__(self):
        pass





