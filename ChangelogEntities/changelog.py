from pyflp import Project
from pyflp.pattern import Note

import enum
from itertools import zip_longest

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
        updates: the edits to <note>'s attributes; != None iff <change_type> = UPDATE
        timestamp: the NTP time that this entry was created at; used for sort-ordering entries
    """
    ntp_client = ntplib.NTPClient()
    change_type: ChangeType
    note: Note
    updates: dict[any, dict[any, any]]
    timestamp: datetime

    def __init__(self, change_type: ChangeType, note: Note, updates: dict[any, dict[any, any]] = None):
        self.change_type = change_type
        self.note = note
        self.updates = updates
        try:
            response = ntp_client.request('north-america.pool.ntp.org', version=3)
            self.timestamp = datetime.utcfromtimestamp(response.tx_time)
        except Exception as e:
            raise ntplib.NTPException("NTP request failed. {}".format(e))


class ChangeLog():
    """

    """
    def __init__(self):
        pass


if __name__ == "__main__":
    ntp_client = ntplib.NTPClient()
    try:
        r = ntp_client.request('north-america.pool.ntp.org', version=3)
        ntp_time1 = datetime.utcfromtimestamp(r.tx_time)
        print(ntp_time1)

        r2 = ntp_client.request('north-america.pool.ntp.org', version=3)
        ntp_time2 = datetime.utcfromtimestamp(r2.tx_time)
        print(ntp_time2)

        print(ntp_time1 > ntp_time2) # if time_a < time_b, then time_a is earlier than time_b
    except Exception as e:
        print("Failed: {}".format(e))







