import pickle
import os

from ChangeLogEngine import ChangeLogEngine

if __name__ == "__main__":
    temp_changelog_engine = ChangeLogEngine()

    logs_to_merge_folder = "C:\\Users\\wbirm\\OneDrive\\Desktop\\premerge"
    num_files = 0
    for path in os.listdir(logs_to_merge_folder):
        if os.path.isfile(os.path.join(logs_to_merge_folder, path)):
            num_files += 1
    
    merge_number = 0
    try:
        while merge_number < num_files:
            with open(logs_to_merge_folder + "\\log{}.pkl".format(merge_number), "rb") as f:
                new_log = pickle.load(f) 
                temp_changelog_engine.merge_changelog(new_log)
                merge_number += 1
        
        with open("C:\\Users\\wbirm\\OneDrive\\Desktop\\merged_log.pkl", "wb") as f:              
                pickle.dump(temp_changelog_engine.get_changelog(), f)
    except FileExistsError as e:
        print("bruh wtf")
    