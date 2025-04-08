import time
import pyautogui as pg
import pyflp
import pickle
import subprocess

from ChangeLogEngine import ChangeLogEngine

# CONSTANT VALUES
WINDOW_TITLE = "FL Studio 20"

# CONSTANT OBJECTS
changelog_engine = ChangeLogEngine()

if __name__ == "__main__":
    # ---------- COMPILE JAVA CLIENT ---------- #
    compilation_successful = False
    try: 
        compile_command = ["javac", "C:\\Users\\wbirm\\FL-Studio-Live\\flp_network\\client\\Client.java"]
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
            run_client_command = ["java", "-cp", "C:\\Users\\wbirm\\FL-Studio-Live\\flp_network", "client.Client"] 
            client_process = subprocess.Popen(run_client_command, 
                                            stdin=subprocess.PIPE, 
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            text=True)
            if not client_process.returncode: # returncode for Popen is initially None, instead of 0, on success
                running_successful = True
            else:
                print("Failed to run client program: {}".format(client_process.stderr))
        except Exception as e:
            print(e)

    time.sleep(1)
    
    # ---------- START PROJECT SNAPSHOT LOOP IF CLIENT PROGRAM IS RUNNING ---------- #
    if running_successful:
        project_path = "C:\\Users\\wbirm\\OneDrive\\Desktop\\dark melody drill.flp" # TODO

        project = pyflp.parse(project_path)
        project_snapshot = pyflp.parse(project_path) # this is the snapshot we will implement the changes in the changelog to

        v1 = None
        v2 = project

        serialization_trigger = 0
        while True: # TODO: This loop should be active only when something (like a button) is triggered by the user.
            v1 = v2 # -------------------------------------------------------------- shift the most recent version back to v1            
            time.sleep(0.5) # -------------------------------------------------------- length of save period

            fl_window = pg.getWindowsWithTitle(WINDOW_TITLE) # TODO: Why this isnt working?
            if not fl_window[0].isActive:
               pg.press('altleft')
            fl_window[0].activate()
            pg.hotkey('ctrl', 's') # ----------------------------------------------- focus to fl window and save

            time.sleep(0.5)
            v2 = pyflp.parse(project_path) # --------------------------------------- retrieve new version

            changelog_engine.parse_changes(v1, v2)
            serialization_trigger += 1
            if serialization_trigger == 1:
                serialization_trigger = 0

                # Laptop
                with open("C:\\Users\\wbirm\\OneDrive\\Desktop\\changelog.pkl", "wb") as f:
                    pickle.dump(changelog_engine.get_changelog(), f)

                output, error = client_process.communicate("go\n", timeout=60)

                if output == "get\n":  
                    with open("C:\\Users\\wbirm\\OneDrive\\Desktop\\merged_changelog.pkl", "rb") as f:
                        merged_log = pickle.load(f) # retrieve the merged log

                        changelog_engine.set_changelog(merged_log) 
                        project = changelog_engine.apply_changes(project_snapshot) # apply changes in the mergelog to the project
                    
                        # ---------- SAVE PROJECT AND RESTART THE USER'S FL STUDIO ---------- #
                        pyflp.save(project, project_path) # save project
                        project_snapshot = pyflp.parse(project_path) # create a new snapshot

                        ex_path = "C:\\Program Files\\Image-Line\\FL Studio 20\\FL64"
                        subprocess.Popen([ex_path, project_path])
                else:
                    print("merge log failed...")
                    break

