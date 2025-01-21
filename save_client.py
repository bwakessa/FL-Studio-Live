import time
import pyautogui as pg
import pyflp

from ChangelogEntities.changeparser import ChangeParser

# CONSTANT VALUES
WINDOW_TITLE = "FL Studio 20"

# CONSTANT OBJECTS
change_parser = ChangeParser()

if __name__ == "__main__":
    # take as input an fl studio file (chosen by the client through file explorer prompt)

    #desktop
    project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp"

    #laptop
    #project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\dark melody drill.flp"


    project = pyflp.parse(project_path)

    v1 = None
    v2 = project

    while True: # TODO: figure out what should trigger the end of this loop
        v1 = v2 # -------------------------------------------------------------- shift the most recent version back to v1
        time.sleep(1) # -------------------------------------------------------- length of save period

        fl_window = pg.getWindowsWithTitle(WINDOW_TITLE) # TODO: Why this isnt working?
        fl_window[0].activate()
        pg.hotkey('ctrl', 's') # ----------------------------------------------- focus to fl window and save

        time.sleep(1)
        v2 = pyflp.parse(project_path) # --------------------------------------- retrieve new version

        change_parser.parse_changes(v1, v2)
        # TODO: Determine how often to periodically serialize the changelog data to be retrieved in java and sent to the server

        # time.sleep(x)
        # change_log = change_parser.get_changelog()






