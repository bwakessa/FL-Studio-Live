from pyflp import Project
from pyflp.pattern import PatternID
from .changelog import *

from itertools import zip_longest
import pickle
import copy

class ChangeLogEngine:
    """Parses between versions of an FL Studio File to find changes

    Attributes:
        _change_log: The changelog this changeparser is currently logging to.
    """
    _change_log: ChangeLog

    def __init__(self):
        self._change_log = ChangeLog()

    def _is_equal(self, note1, note2) -> bool:
        """Helper Function: Return note1 == note2
        TODO: figure out how to loop through attributes instead of doing explicit comparisons
        """
        key_letter = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}

        if note1 and note2:
            keys_are_equal = False
            if isinstance(note1.key, str) and isinstance(note2.key, str):
                keys_are_equal = True if note1.key == note2.key else False
            elif isinstance(note1.key, str):
                keys_are_equal = True if (12*int(note1.key[-1]) + key_letter[note1.key[:-1]]) == note2.key else False
            elif isinstance(note2.key, str):
                keys_are_equal = True if note1.key == (12*int(note2.key[-1]) + key_letter[note2.key[:-1]]) else False
            else:
                keys_are_equal = True if note1.key == note2.key else False

        return False if not note1 or not note2 \
                    or note1.fine_pitch != note2.fine_pitch \
                    or note1.group != note2.group \
                    or not keys_are_equal \
                    or note1.length != note2.length \
                    or note1.midi_channel != note2.midi_channel \
                    or note1.mod_x != note2.mod_x \
                    or note1.mod_y != note2.mod_y \
                    or note1.pan != note2.pan \
                    or note1.position != note2.position \
                    or note1.rack_channel != note2.rack_channel \
                    or note1.release != note2.release \
                    or note1.velocity != note2.velocity \
        else True

    def _find_differences(self, note1: Note, note2: Note) -> dict[str, dict[Note, any]]:
        """Helper Function: Return a dictionary of the unequal attributes between <note1> and <note2>
        <note1> must be from the file version before the save
        <note2> must be from the file version after the save

        return: {a: {note1: note1.a, note2: note2.a}}
        """
        differences = {}
        if note1.fine_pitch != note2.fine_pitch:
            differences["fine_pitch"] = {note1: note1.fine_pitch, note2: note2.fine_pitch}
        if note1.group != note2.group:
            differences["group"] = {note1: note1.group, note2: note2.group}
        if note1.key != note2.key:
            differences["key"] = {note1: note1.key, note2: note2.key}
        if note1.length != note2.length:
            differences["length"] = {note1: note1.length, note2: note2.length}
        if note1.midi_channel != note2.midi_channel:
            differences["midi_channel"] = {note1: note1.midi_channel, note2: note2.midi_channel}
        if note1.mod_x != note2.mod_x:
            differences["mod_x"] = {note1: note1.mod_x, note2: note2.mod_x}
        if note1.mod_y != note2.mod_y:
            differences["mod_y"] = {note1: note1.mod_y, note2: note2.mod_y}
        if note1.pan != note2.pan:
            differences["pan"] = {note1: note1.pan, note2: note2.pan}
        if note1.position != note2.position:
            differences["position"] = {note1: note1.position, note2: note2.position}
        if note1.rack_channel != note2.rack_channel:
            differences["rack_channel"] = {note1: note1.rack_channel, note2: note2.rack_channel}
        if note1.release != note2.release:
            differences["release"] = {note1: note1.release, note2: note2.release}
        if note1.slide != note2.slide:
            differences["slide"] = {note1: note1.slide, note2: note2.slide}
        if note1.velocity != note2.velocity:
            differences["velocity"] = {note1: note1.velocity, note2: note2.velocity}

        return differences
    
    
    def get_changelog(self) -> ChangeLog:
        """Return this engine's change log"""
        return self._change_log
    
    def set_changelog(self, new_log: ChangeLog) -> None:
        """Set this engine's change log to <new_log>"""
        self.clear_changelog()
        self.append_changelog(new_log)

    def clear_changelog(self) -> None:
        """Clear this engine's change log"""
        self._change_log.clear_entries()

    def append_changelog(self, log: ChangeLog) -> None:
        """Append <log> to this engine's changelog

        <log>: ChangeLog to be appended to <self._change_log>
        """
        entries = log.get_entries()
        for entry in entries:
            self._change_log.log(entry)

    def merge_changelog(self, log: ChangeLog) -> None:
        """Merge <log> with this engine's changelog, using the <ChangeLogEntry.timestamp> as the sort order

        <log>: ChangeLog to be sort-merged with <self._change_log>
        """
        new_change_log = ChangeLog()
        left_entries = self._change_log.get_entries()
        right_entries = log.get_entries()

        left_pointer = 0
        right_pointer = 0
        # basic sort-merge (not merge sort) algorithm
        while left_pointer < len(left_entries) and right_pointer < len(right_entries):
            if left_entries[left_pointer].timestamp < right_entries[right_pointer].timestamp: # left entry was logged earlier than right entry
                new_change_log.log(left_entries[left_pointer])
                left_pointer += 1
            elif left_entries[left_pointer].timestamp > right_entries[right_pointer].timestamp: # right entry was logged earlier than left entry
                new_change_log.log(right_entries[right_pointer])
                right_pointer += 1
            else: # left and right entry were logged at the exact same time
                new_change_log.log([left_entries[left_pointer], right_entries[right_pointer]])
                left_pointer += 1
                right_pointer += 1
        
        if left_pointer < len(left_entries): # there remains some un-merged entries in self._change_log, but none from <log>
            while left_pointer < len(left_entries):
                new_change_log.log(left_entries[left_pointer])
                left_pointer += 1
        elif right_pointer < len(right_entries): # there remains some un-merged entries in <log>, but none from this log
            while right_pointer < len(right_entries):
                new_change_log.log(right_entries[right_pointer])
                right_pointer += 1

        self._change_log = new_change_log

    def parse_changes(self, v1: Project, v2: Project) -> None:
        """Given 2 version of an FL Studio file, determine the pattern changes and log them into <self._change_log>

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
                    delete_entry = ChangeLogEntry(ChangeType.DELETE, pattern1, v1_notes[unmatched_indices[i]])
                    new_change_log.log(delete_entry)

                # step 2: log an UPDATE ChangeEntry for the remaining len(v2) - m = len(v2) - len(v1) + len(unmatched) unmatched notes
                for i in range(0, len(unmatched_indices) - len(v1_notes) + len(v2_notes)):
                    updates = self._find_differences(v1_notes[unmatched_indices[i]], v2_notes[unmatched_indices[i]])
                    update_entry = ChangeLogEntry(ChangeType.UPDATE, pattern1, v1_notes[unmatched_indices[i]], updates)
                    new_change_log.log(update_entry)

            elif len(v1_notes) < len(v2_notes): # insertions occured: m = len(v2) - len(unmatched_indices)
                # step 1: log len(v2) - len(v1) INSERT ChangeEntries from <unmatched_indices>, traversing backwards from its tail
                for i in range(len(unmatched_indices) - 1, len(unmatched_indices) - 1 - (len(v2_notes) - len(v1_notes)), -1):
                    insert_entry = ChangeLogEntry(ChangeType.INSERT, pattern1, v2_notes[unmatched_indices[i]])
                    new_change_log.log(insert_entry)

                # step 2: log an UPDATE ChangeEntry for the remaining len(v1) - m = len(v1) - len(v2) + len(unmatched) notes
                for i in range(0, len(unmatched_indices) - len(v2_notes) + len(v1_notes)):
                    updates = self._find_differences(v1_notes[unmatched_indices[i]], v2_notes[unmatched_indices[i]])
                    update_entry = ChangeLogEntry(ChangeType.UPDATE, pattern1, v1_notes[unmatched_indices[i]], updates)
                    new_change_log.log(update_entry)

            else: # (practically) no insertions or deletions occured, only updates; len(v1) == len(v2)
                for i in unmatched_indices:
                    updates = self._find_differences(v1_notes[i], v2_notes[i])
                    update_entry = ChangeLogEntry(ChangeType.UPDATE, pattern1, v1_notes[i], updates)
                    new_change_log.log(update_entry)

        self.append_changelog(new_change_log)

    def _update_note(self, note: Note, updates: dict[any, dict[any, any]]) -> None: 
        key_letter = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}

        if "fine_pitch" in updates:
            note.fine_pitch = list(updates["fine_pitch"].values())[1]
        if "group" in updates:
            note.group = list(updates["group"].values())[1]
        if "key" in updates:
            if isinstance(note.key, str):
                note.key = list(updates["key"].values())[1]
            else:
                k = list(updates["key"].values())[1]
                note.key = 12*int(k[-1]) + key_letter[k[:-1]]
        if "length" in updates:
            note.length = list(updates["length"].values())[1]
        if "midi_channel" in updates:
            note.midi_channel = list(updates["midi_channel"].values())[1]
        if "mod_x" in updates:
            note.mod_x = list(updates["mod_x"].values())[1]
        if "mod_y" in updates:
            note.mod_y = list(updates["mod_y"].values())[1]
        if "pan" in updates:
            note.pan = list(updates["pan"].values())[1]
        if "position" in updates:
            note.position = list(updates["position"].values())[1]
        if "rack_channel" in updates:
            note.rack_channel = list(updates["rack_channel"].values())[1]
        if "release" in updates:
            note.release = list(updates["release"].values())[1]
        if "slide" in updates:
            note.slide = list(updates["slide"].values())[1]
        if "velocity" in updates:
            note.velocity = list(updates["velocity"].values())[1]
    
    def apply_changes(self, project_snapshot: Project) -> Project:
        for edit in self._change_log.get_entries():            
            # Retrieve the Notes Event of <edit.pattern>
            pattern_to_update = None
            for pattern in project_snapshot.patterns:
                if pattern.name == edit.pattern.name:
                    pattern_to_update = pattern
                    break
            notes_event = pattern_to_update.events.first(PatternID.Notes)          
            if notes_event:
                if edit.change_type == ChangeType.INSERT:
                    notes_event.append(edit.note)
                elif edit.change_type == ChangeType.DELETE:
                    self._remove_note(notes_event, edit.note)
                else: # UPDATE
                    for note in notes_event.data:
                        if self._is_equal(note, edit.note): # TODO: debug whether memory address of <note> and <edit.note> are equal
                            self._update_note(note, edit.updates)
                            break        
        return project_snapshot
    
    def _remove_note(self, event, note: Note) -> None:
        for e in event.data:
            if self._is_equal(e, note):
                event.remove(e)
                break
        


                    

    
    
        

if __name__ == "__main__":
    """The main in this file will only be called when the java server code executes this file.
       In this method is where we retrieve all the changelogs from the designated folder to be merged by ChangeLogEngine.merge_changelog()     
    """
    logs_to_merge_folder = "C:\\Users\\wbirm\\OneDrive\\Desktop\\premerge"
    
    try:
        temp_changelog_engine = ChangeLogEngine()
        merge_number = 0
        while (True): # This loop will break when it encounters an error when trying to open a file that doesnt exist
            with open(logs_to_merge_folder + "\\log{}.pkl".format(merge_number), "rb") as f:
                new_log = pickle.load(f)
                temp_changelog_engine.merge_changelog(new_log)
            merge_number += 1
    except FileExistsError as e:
        print("Log {} not found. Saving merged log to Desktop...".format(merge_number))
    finally:
        with open("C:\\Users\\wbirm\\OneDrive\\Desktop\\merged_log.pkl", "wb") as f:
            pickle.dump(temp_changelog_engine.get_changelog(), f)
