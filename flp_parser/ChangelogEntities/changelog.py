from pyflp.pattern import Note, Pattern

import enum
import ntplib # NTP Library
from datetime import datetime

@enum.unique
class ChangeType(enum.Enum):
    INSERT = 1
    DELETE = 2
    UPDATE = 3

class ChangeLogEntry():
    """An entry of a ChangeLog representing a single edit of a note

    Static Attributes:
        ntp_client: client to make NTP requests. Is static so we don't spend time making one for each class instance.
        
    Instance Attributes:
        change_type: The type of edit to the note in this entry
        note: The note being edited
        updates: the edits to <note>'s attributes; != None iff <change_type> != UPDATE
        timestamp: the NTP time that this entry was created at; used for sort-ordering entries
    """
    _ntp_client = ntplib.NTPClient()
    change_type: ChangeType
    pattern: Pattern
    note: Note
    updates: dict[any, dict[any, any]]
    timestamp: datetime

    def __init__(self, change_type: ChangeType, pattern: Pattern, note: Note, updates: dict[any, dict[any, any]] = None):
        self.change_type = change_type
        self.pattern = pattern
        self.note = note
        self.updates = updates
        try:
            response = self._ntp_client.request('north-america.pool.ntp.org', version=3)
            self.timestamp = datetime.utcfromtimestamp(response.tx_time)
        except Exception as e:
            raise ntplib.NTPException("NTP request failed. {}".format(e))

class ChangeLog():
    """An append-only log of ChangeLogEntries.

    Attributes:
        _entries: The list of entries in this ChangeLog
    """

    _entries: list[ChangeLogEntry]

    def __init__(self):
        self._entries = []

    def get_entries(self) -> list[ChangeLogEntry]:
        """Return this log's entries"""
        return self._entries
    
    def clear_entries(self) -> None:
        self._entries = []

    def log(self, entry: ChangeLogEntry | list[ChangeLogEntry]) -> None:
        """Append <entry> to this ChangeLog

        if <entry> is ChangeLogEntry, append to changelog.
        if <entry> is list<ChangeLogEntry>, extend to changelog
        """
        if isinstance(entry, ChangeLogEntry):
            self._entries.append(entry)
        elif isinstance(entry, list):
            self._entries.extend(entry)
        else:
            pass
