from pyflp import Project
from pyflp.pattern import Note
from changelog import ChangeLog, ChangeLogEntry, ChangeType

from itertools import zip_longest

class ChangeParser:

    def __init__(self):
        pass

    def merge_changelogs(self, log1: ChangeLog, log2: ChangeLog) -> ChangeLog:
        pass

    def _is_equal(self, note1: Note, note2: Note) -> bool:
        """Return note1 == note2"""


    def parse_changes(self, v1: Project, v2: Project) -> ChangeLog:
        change_log = ChangeLog()

        for pattern1, pattern2 in zip(v1.patterns, v2.patterns):
            # Must exhuast the generators into a data structure to determine insertions/deletions, etc.
            # Possible data structures:
            # - indexed adjacent arrays (2x space of data)
            # - a hash table (1x-2x space of data, but cant accomodate for different note counts)
            # Choice: indexed adjacent arrays (avoids possible overhead of hash tables)

            unmatched_indices = [] # indices of notes in <v1_notes>, <v2_notes> where unmatches occur

            v1_notes = []
            v2_notes = []
            for v1_note, v2_note in zip_longest(pattern1.notes, pattern2.notes, fillvalue=None):
                if not self._is_equal(v1_note, v2_note):
                    unmatched_indices.append(max(len(v1_notes), len(v2_notes)))

                if v1_note:
                    v1_notes.append(v1_note)
                if v2_note:
                    v2_notes.append(v2_note)

            if len(v1_notes) > len(v2_notes):
                # deletion(s) occurred: m = len(v1) - len(unmatched_indices) (REFER TO DOCUMENTATION FOR DEFINITION OF <m>)
                # step 1: log len(v1) - len(v2) DELETE ChangeEntries from <unmatched_indices>, traversing backwards from its tail
                pass
                # for i in range(len(unmatched_indices) - 1, len(unmatched_indices) - 1 - (len(v1_notes) - len(v2_notes)), -1):
                #     delete_entry = ChangeLogEntry(ChangeType.DELETE, v1_notes[unmatched_indices[i]])
                #     change_log.log(delete_entry) # TODO: implement in changelog.py


                # step 2: for the remaining len(v2) - m unmatched indices, log an UPDATE ChangeEntry 7by comparing the notes at the indices in v1 and v2 to find differences
                # TODO: implement method algorithm which determines differences between notes, and returns a dictionary of the changed attributes
            elif len(v1_notes) < len(v2_notes):
                # insertion(s) occurred: m = len(v2_notes) - len(unmatched_indices)
                pass
            else:
                # len(v1) == len(v2)
                pass






        return change_log
