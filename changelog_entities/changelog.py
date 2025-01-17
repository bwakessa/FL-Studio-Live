from pyflp import Project
import enum

@enum.unique
class ChangeType(enum):
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
        pass


