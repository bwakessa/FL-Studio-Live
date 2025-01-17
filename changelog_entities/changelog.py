from pyflp import Project
import enum
from itertools import zip_longest

@enum.unique
class ChangeType(enum.Enum):
    INSERT = 1
    DELETE = 2
    POSITION = 3
    KEY = 4

class ChangeLogEntry():

    def __init__(self, change_type: ChangeType):
        pass

class ChangeLog():

    def __init__(self):
        pass

class ChangeParser:

    def __init__(self):
        pass

    def merge_changelogs(self, log1: ChangeLog, log2: ChangeLog) -> ChangeLog:
        pass

    def parse_changes(self, v1: Project, v2: Project) -> ChangeLog:
        changelog = ChangeLog()

        for pattern1, pattern2 in zip(v1.patterns, v2.patterns):
            # Must exhuast the generators into a data structure to determine insertions/deletions, etc.
            # Possible data structures:
            # - indexed adjacent arrays (2x space of data)
            # - a hash table (1x-2x space of data, but cant accomodate for different note counts)
            # Choice: indexed adjacent arrays (avoids possible overhead of hash tables)

            unmatched_indices = [] # indices of notes in <v1_notes>, <v2_notes> where changes between notes occurred

            v1_notes = []
            v2_notes = []
            for v1_note, v2_note in zip_longest(pattern1.notes, pattern2.notes, fillvalue=None):
                if v1_note != v2_note:
                    unmatched_indices.append(max(len(v1_notes), len(v2_notes)))

                v1_notes.append(v1_note)
                v2_notes.append(v2_note)

            if len(v1_notes) > len(v2_notes):
                # deletion(s) occurred: m = len(v1_notes) - len(unmatched_indices) (REFER TO DOCUMENTATION FOR DEFINITION OF <m>)
                pass
                # step 1: log  DELETE ChangeEntry
            elif len(v1_notes) < len(v2_notes):
                # insertion(s) occurred: m = len(v2_notes) - len(unmatched_indices)
                pass
            else:
                # len(v1) == len(v2)
                pass






        return changelog




