"""
Test whether changelog engine properly keeps tracks of changes, and applies changes to project snapshots
"""
import pyflp
import copy
from ChangelogEntities.ChangeLogEngine import *
from ChangelogEntities.changelog import *

project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\dark melody drill.flp"

def test_track_changes():
    """Test whether a changelog engine properly keeps track of changes 
            
                *** TEST USING DEBUGGER INSTEAD OF INSERTIONS ***     """
    
    """ SUCCESSFULLY PASSED 3 TESTS """
    changelog_engine = ChangeLogEngine()

    v0 = pyflp.parse(project_path)
    # >>>>>>>>>>>>>>>> Here, make an edit in fl studio and save it <<<<<<<<<<<<<<<< #
    v1 = pyflp.parse(project_path)
    changelog_engine.parse_changes(v0, v1)
    v1_log = changelog_engine.get_changelog()

    # >>>>>>>>>>>>>>>> Here, make an edit in fl studio and save it <<<<<<<<<<<<<<<< #
    v2 = pyflp.parse(project_path)
    changelog_engine.parse_changes(v1, v2)
    v2_log = changelog_engine.get_changelog()
    
def test_apply_changes():
    """Test the automatic application of a changelog to a project snapshot"""
    changelog_engine = ChangeLogEngine()

    v0 = pyflp.parse(project_path)
    project_snapshot = pyflp.parse(project_path) # deepcopy doesnt work for some reason, so just hope this will be the same as v0
    # >>>>>>>>>>>>>>>> Here, make an edit in fl studio and save it <<<<<<<<<<<<<<<< #
    v1 = pyflp.parse(project_path)
    changelog_engine.parse_changes(v0, v1)
    v1_log = changelog_engine.get_changelog()

    # >>>>>>>>>>>>>>>> Here, make an edit in fl studio and save it <<<<<<<<<<<<<<<< #
    # v2 = pyflp.parse(project_path)
    # changelog_engine.parse_changes(v1, v2)
    # v2_log = changelog_engine.get_changelog()

    # apply changes
    updated_project = changelog_engine.apply_changes(project_snapshot)
    pyflp.save(updated_project, project_path)





    
if __name__ == "__main__":
    #test_track_changes()
    test_apply_changes()

