import pyflp

from flp_parser.ChangeLogEngine import *

project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp"
# ------------------------------ ChangeLogEngine ------------------------------ #
def test_change_engine():
    change_engine = ChangeLogEngine()

    v0 = pyflp.parse(project_path)
    # >>>>>>>>>>>>>>>> Here, make an edit in fl studio and save it <<<<<<<<<<<<<<<< #
    v1 = pyflp.parse(project_path)

    change_engine.parse_changes(v0, v1)
    # >>>>>>>>>>>>>>>> Here, make an edit in fl studio and save it <<<<<<<<<<<<<<<< #

    v1_log = change_engine.get_changelog()
    v2 = pyflp.parse(project_path)
    change_engine.parse_changes(v1, v2)
    v2_log = change_engine.get_changelog()

    assert v1_log != v2_log


if __name__ == "__main__":
    test_change_engine()
