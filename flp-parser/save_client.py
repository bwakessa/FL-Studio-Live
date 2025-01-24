import time
import pyautogui as pg
import pyflp
import pickle

from ChangelogEntities.ChangeLogEngine import ChangeLogEngine

# CONSTANT VALUES
WINDOW_TITLE = "FL Studio 20"

# CONSTANT OBJECTS
changelog_engine = ChangeLogEngine()

if __name__ == "__main__":
    # take as input an fl studio file (chosen by the client through file explorer prompt)

    #desktop
    project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp"

    #laptop
    # project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\dark melody drill.flp"
    project = pyflp.parse(project_path)

    v1 = None
    v2 = project

    serialization_trigger = 0
    while True: # TODO: figure out what should trigger the end of this loop
                # ^ This loop should be active only when a something (like a button) is triggered by the user.

        v1 = v2 # -------------------------------------------------------------- shift the most recent version back to v1
        time.sleep(0.1) # -------------------------------------------------------- length of save period

        fl_window = pg.getWindowsWithTitle(WINDOW_TITLE) # TODO: Why this isnt working?
        fl_window[0].activate()
        pg.hotkey('ctrl', 's') # ----------------------------------------------- focus to fl window and save

        time.sleep(0.5)
        v2 = pyflp.parse(project_path) # --------------------------------------- retrieve new version

        changelog_engine.parse_changes(v1, v2)
        # TODO: Determine how often to periodically serialize the changelog data to be retrieved in java and sent to the server

        if serialization_trigger == 10:
            serialization_trigger = 0
            with open("changelog.pkl", "wb") as f:
                pickle.dump(changelog_engine, f)

            # run java client program through subprocess
                # java program retrieves the pkl file and sends it to the java server program
                # the server uses subprocess to call the merge algorithm which will be in ChangeLogEngine.py
                    # problem: have to keep a "snapshot" of the file before each serialization trigger
                # new merged log will be retrieved by server, and sent to client to be saved to "mergedchangelog.pkl"
            # retrieve mergedchangelog.pkl here


        # time.sleep(x)
        # change_log = change_parser.get_changelog()






