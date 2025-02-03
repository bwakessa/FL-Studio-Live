"""
Test whether the java client file will be compiled and executed correctly from save_client.py
"""

import subprocess

if __name__ == "__main__":
    # ---------- COMPILE ---------- #
    compile_command = ["javac", "C:\\Users\\wbirm\\FL-Studio-Live\\flp_network\\client\\Client.java"]
    compile_process = subprocess.run(compile_command, capture_output=True, text=True)

    assert compile_process.returncode == 0

    # ------------ RUN ------------ #
    run_client_command = ["java", "-cp", "C:\\Users\\wbirm\\FL-Studio-Live\\flp_network", "client.Client"]
    client_process = subprocess.Popen(run_client_command, 
                                            stdin=subprocess.PIPE, 
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            text=True)
    
    assert client_process.returncode == None 