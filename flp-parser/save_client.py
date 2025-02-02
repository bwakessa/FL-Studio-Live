import time
import copy
import pyautogui as pg
import pyflp
import pickle
import subprocess

# CODON AND CYTHON

from ChangelogEntities.ChangeLogEngine import ChangeLogEngine

# CONSTANT VALUES
WINDOW_TITLE = "FL Studio 20"

# CONSTANT OBJECTS
changelog_engine = ChangeLogEngine()

if __name__ == "__main__":
    # ---------- COMPILE JAVA CLIENT ---------- #
    compilation_successful = False
    try: 
        compile_command = ["javac", "C:\\Users\\wbirm\\FL-Studio-Live\\flp-network\\client\\Client.java"]
        compile_process = subprocess.run(compile_command, capture_output=True, text=True)

        if compile_process.returncode == 0:
            compilation_successful = True
        else:
            print("Failed to compile client program: {}".format(compile_process.stderr))
    except Exception as e:
        print(e)

    # ---------- RUN JAVA CLIENT ---------- #
    running_successful = False
    if compilation_successful:
        try:
            run_client_command = ["java", "-cp", "C:\\Users\\wbirm\\FL-Studio-Live\\flp-network", "client.Client"] 
            client_process = subprocess.Popen(run_client_command, 
                                            stdin=subprocess.PIPE, 
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            text=True)
            if client_process.returncode == 0:
                running_successful = True
            else:
                print("Failed to run client program: {}".format(client_process.stderr))
        except Exception as e:
            print(e)

    time.sleep(1)
    
    # ---------- START PYTHON SNAPSHOT LOOP IF CLIENT PROGRAM IS RUNNING ---------- #
    if running_successful:
        # Desktop:
        # project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp"
        # Laptop:
        project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\dark melody drill.flp"

        project = pyflp.parse(project_path)
        project_snapshot = copy.deepcopy(project) # this is the snapshot we will implement the changes in the changelog to

        v1 = None
        v2 = project

        serialization_trigger = 0
        while True: # TODO: figure out what should trigger the end of this loop
                    # ^ This loop should be active only when something (like a button) is triggered by the user.

            v1 = v2 # -------------------------------------------------------------- shift the most recent version back to v1
            time.sleep(0.1) # -------------------------------------------------------- length of save period

            fl_window = pg.getWindowsWithTitle(WINDOW_TITLE) # TODO: Why this isnt working?
            if not fl_window[0].isActive:
                pg.press('altleft')
            fl_window[0].activate()
            pg.hotkey('ctrl', 's') # ----------------------------------------------- focus to fl window and save

            time.sleep(0.5)
            v2 = pyflp.parse(project_path) # --------------------------------------- retrieve new version

            changelog_engine.parse_changes(v1, v2)

            serialization_trigger += 1
            if serialization_trigger == 10:
                serialization_trigger = 0

                # Laptop
                with open("C:\\Users\\wbirm\\OneDrive\\Desktop\\changelog.pkl", "wb") as f:
                    pickle.dump(changelog_engine.get_changelog(), f)
                # Desktop
                # ---

                client_process.stdin.write("go\n") # Send trigger to the client to send changelog to server
                retrieve_trigger = client_process.stdout.readline() #

                if retrieve_trigger == "get":  
                    with open("C:\\Users\\wbirm\\OneDrive\\Desktop\\merged_changelog.pkl", "rb") as f:
                        merged_log = pickle.load(f) # retrieve the merged log

                        changelog_engine.set_changelog(merged_log) 
                        project = changelog_engine.apply_changes(project_snapshot) # apply changes in the mergelog to the project
                        project_snapshot = copy.deepcopy(project) # create a new snapshot

                        # ---------- SAVE PROJECT AND RESTART THE USER'S FL STUDIO ---------- #
                        pyflp.save(project, "C:\\Users\\wbirm\\OneDrive\\Desktop\\dark melody drill.flp") # save project
                else:
                    print("merge log failed...")
                    break

                        




                # - send input to java program to let it know to retrieve pkl file
                # - java program retrieves the pkl file and sends it to the java server program
                # - the server uses subprocess to call the merge algorithm which will be in ChangeLogEngine.py
                        # problem: have to keep a "snapshot" of the file before each serialization trigger
                    # new merged log will be created by server, and sent to client to be saved to "merged_log.pkl"
                # retrieve mergedchangelog.pkl here


            # time.sleep(x)
            # change_log = change_parser.get_changelog()






