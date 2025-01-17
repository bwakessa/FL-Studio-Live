import time
import pyautogui as pg
import pyflp

from changelog_entities.changelog import ChangeParser

# CONSTANT VALUES
WINDOW_TITLE = "FL Studio 20"

# CONSTANT OBJECTS
change_parser = ChangeParser()

if __name__ == "__main__":
    # take as input an fl studio file (chosen by the client through file explorer prompt)
    project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp"
    project = pyflp.parse(project_path)

    v1 = None
    v2 = project

    while True:
        v1 = v2 # -------------------------------------------------------------- shift the most recent version back to v1
        time.sleep(1) # -------------------------------------------------------- length of save period

        fl_window = pg.getWindowsWithTitle(WINDOW_TITLE)
        fl_window[0].activate()
        pg.hotkey('ctrl', 's') # ----------------------------------------------- focus to fl window and save

        time.sleep(1)
        v2 = pyflp.parse(project_path) # --------------------------------------- retrieve new version






