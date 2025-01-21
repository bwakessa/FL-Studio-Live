from pyflp import Project
from pyflp.pattern import Note
from .changelog import *

from itertools import zip_longest

class ChangeParser:
    """Parses between versions of an FL Studio File to find changes

    Attributes:
        change_log: The changelog this changeparser is currently logging to.
    """
    change_log: ChangeLog

    def __init__(self):
        self.change_log = ChangeLog()

    def get_changelog(self) -> ChangeLog:
        return self.change_log

    def _is_equal(self, note1: Note, note2: Note) -> bool:
        """Return note1 == note2
        TODO: figure out how to loop through attributes instead of doing explicit comparisons
        """
        return False if note1.fine_pitch != note2.fine_pitch \
                    or note1.group != note2.group \
                    or note1.key != note2.key \
                    or note1.length != note2.length \
                    or note1.midi_channel != note2.midi_channel \
                    or note1.mod_x != note2.mod_x \
                    or note1.mod_y != note2.mod_y \
                    or note1.pan != note2.pan \
                    or note1.position != note2.position \
                    or note1.rack_channel != note2.rack_channel \
                    or note1.release != note2.release \
                    or note1.slide != note2.slide \
                    or note1.velocity != note2.velocity \
        else True

    def _find_differences(self, note1: Note, note2: Note) -> dict[str, dict[Note, any]]:
        """Return a dictionary of the unequal attributes between <note1> and <note2>
        <note1> must be from the file version before the save
        <note2> must be from the file version after the save
        """
        differences = {}
        if note1.fine_pitch != note2.fine_pitch:
            differences["fine_pitch"] = {note1: note1.fine_pitch, note2: note2.fine_pitch}
        if note1.group != note2.group:
            differences["group"] = {note1: note1.group, note2: note2.group}
        if note1.group != note2.group:
            differences["key"] = {note1: note1.key, note2: note2.key}
        if note1.group != note2.group:
            differences["length"] = {note1: note1.length, note2: note2.length}
        if note1.group != note2.group:
            differences["midi_channel"] = {note1: note1.midi_channel, note2: note2.midi_channel}
        if note1.group != note2.group:
            differences["mod_x"] = {note1: note1.mod_x, note2: note2.mod_x}
        if note1.group != note2.group:
            differences["mod_y"] = {note1: note1.mod_y, note2: note2.mod_y}
        if note1.group != note2.group:
            differences["pan"] = {note1: note1.pan, note2: note2.pan}
        if note1.group != note2.group:
            differences["position"] = {note1: note1.position, note2: note2.position}
        if note1.group != note2.group:
            differences["rack_channel"] = {note1: note1.rack_channel, note2: note2.rack_channel}
        if note1.group != note2.group:
            differences["release"] = {note1: note1.release, note2: note2.release}
        if note1.group != note2.group:
            differences["slide"] = {note1: note1.slide, note2: note2.slide}
        if note1.group != note2.group:
            differences["velocity"] = {note1: note1.velocity, note2: note2.velocity}

        return differences

    def append_changelog(self, log: ChangeLog) -> None:
        """Append <log> to <self.change_log>

        <log>: ChangeLog to be appended to <self.change_log>
        """
        entries = log.get_entries() # TODO: implement this in ChangeLog
        for entry in entries:
            self.change_log.log(entry)

    def parse_changes(self, v1: Project, v2: Project) -> None:
        """Given 2 version of an FL Studio file, determine the changes in the patterns and log them into <change_log>

        <v1>: FL Studio file object before the save
        <v2>: FL Studio file object after the save
        """
        new_change_log = ChangeLog()

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

            if len(v1_notes) > len(v2_notes): # deletions occurred: m = len(v1) - len(unmatched_indices) (REFER TO DOCUMENTATION FOR DEFINITION OF <m>)
                # step 1: log len(v1) - len(v2) DELETE ChangeEntries from <unmatched_indices>, traversing backwards from its tail
                for i in range(len(unmatched_indices) - 1, len(unmatched_indices) - 1 - (len(v1_notes) - len(v2_notes)), -1):
                    delete_entry = ChangeLogEntry(ChangeType.DELETE, v1_notes[unmatched_indices[i]])
                    new_change_log.log(delete_entry) # TODO: implement in ChangeLog

                # step 2: log an UPDATE ChangeEntry for the remaining len(v2) - m = len(v2) - len(v1) + len(unmatched) unmatched notes
                for i in range(0, len(unmatched_indices) - len(v1_notes) + len(v2_notes)):
                    updates = self._find_differences(v1_notes[unmatched_indices[i]], v2_notes[unmatched_indices[i]])
                    update_entry = ChangeLogEntry(ChangeType.UPDATE, v1_notes[unmatched_indices[i]], updates)
                    new_change_log.log(update_entry)

            elif len(v1_notes) < len(v2_notes): # insertions occured: m = len(v2) - len(unmatched_indices)
                # step 1: log len(v2) - len(v1) INSERT ChangeEntries from <unmatched_indices>, traversing backwards from its tail
                for i in range(len(unmatched_indices) - 1, len(unmatched_indices) - 1 - (len(v2_notes) - len(v1_notes)), -1):
                    insert_entry = ChangeLogEntry(ChangeType.INSERT, v2_notes[unmatched_indices[i]])
                    new_change_log.log(insert_entry)

                # step 2: log an UPDATE ChangeEntry for the remaining len(v1) - m = len(v1) - len(v2) + len(unmatched) notes
                for i in range(0, len(unmatched_indices) - len(v2_notes) + len(v1_notes)):
                    updates = self._find_differences(v1_notes[unmatched_indices[i]], v2_notes[unmatched_indices[i]])
                    update_entry = ChangeLogEntry(ChangeType.UPDATE, v1_notes[unmatched_indices[i]], updates)
                    new_change_log.log(update_entry)

            else: # (practically) no insertions or deletions occured, only updates
                # len(v1) == len(v2)
                for i in unmatched_indices:
                    updates = self._find_differences(v1_notes[i], v2_notes[i])
                    update_entry = ChangeLogEntry(ChangeType.UPDATE, v1_notes[i], updates)
                    new_change_log.log(update_entry)

        self.append_changelog(new_change_log)
