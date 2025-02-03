
# Elements of the state of a file you want collaboration on.
# Note: Main -> must be implemented in the MVP
# - Playlist (Main) - "patterns"
# - Piano Roll (Main)
# - Channel Rack (Main) - "channels"
# - Mixer
#
# - Tempo (Main)
#
#
# *#


# import playlist # functions for interacting with the playlist
import pyflp
import copy
from pyflp.pattern import PatternID
from pyflp import EventTree

#proj = pyflp.parse("C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp")
proj = pyflp.parse("C:\\Users\\wbirm\\OneDrive\\Desktop\\dark melody drill.flp")

if __name__ == "__main__":
    print("How many tugs did i have this year and how many times did my bed get sticky?\nHad a uncle whos name was ricky, took me to his van and he touched my dicky.\nI didnt want to tell aunt vicky so I went police station real quickly.\nHow many years did he get? Top of my head, i think about 50!")
    print(proj.ppq)

    for ch in proj.channels:
       print(ch)

    print(type(proj.channels))

    for pt in proj.patterns:
       print(pt)

    for marker in proj.patterns:
       print(marker.timemarkers)

    for arr in proj.arrangements:
        for t in arr.tracks:
            for note in t[0].pattern.notes:
                # ----------------------------------- EXPERIMENTALS -------------------------------------
                # b = t[0]
                # c = b.pattern
                # d = c.events
                # a = d.first(PatternID.Notes)
                # NotesEventID = PatternID.Notes
                #
                # for indexed_event in d.lst:
                #     if (a == indexed_event.e):
                #         print("found it: {}".format(indexed_event.r))
                #
                # sample_note = a.data[0].copy() # making base for new note
                #
                # # edits to base of new note
                # sample_note.length = 384 # 4*ppq
                # sample_note.key = 48 # C4
                #
                # a.append(sample_note) # append new note to our NoteEvent
                #
                # # NOW WE WANT TO INSERT THIS NOTEEVENT BACK INTO THE EVENT TREE,
                # # AND REMOVE THE OLD VERSION OF THIS NOTEEVENT FROM THE EVENT TREE.
                # # TO DO THIS, WE NEED TO DETERMINE THE POSITION OF THE ORIGINAL NOTE EVENT,
                # # AND INSERT THIS NEW EVENT INTO THAT POSITION
                #
                # meoldy = t[0].pattern.notes
                # ----------------------------------- EXPERIMENTALS -------------------------------------




                # ---------- change LENGTH of a note ------------
                note.length = note.length * 2

                # ---------- change POSITION of a note ----------
                note.position += 384 # position

                # ---------- change KEY of a note ---------------
                note.key = 0 # 0 = C0; 131 = B10

                # ---------- INSERT note ------------------------

                # 1. retrieve note event
                note_event = t[0].pattern.events.first(PatternID.Notes)

                # 2. create a copy of the Note datastructure to edit (ds is "Container")
                new_note_base = note_event.data[0].copy()

                # 3. make some edits to the note base
                new_note_base.length = 384 # 4*ppq
                new_note_base.key = 48 # key = C4

                # 4. add new note to a COPY of the note event
                note_event.append(new_note_base) # this already edits the event tree; don't need to proceed to step 5


                delete_copy = copy.deepcopy(new_note_base)
                # ---------- DELETE note ------------------------
                note_event.remove(delete_copy)

                #     # 5. insert note event back into the event tree
                #
                #         # 5a. Determine id of NotesEvent in the root event tree
                # rootidx = None
                # for indexed_event in t[0].pattern.events.lst:
                #     if (indexed_event.e == note_event):
                #         rootidx = indexed_event.r
                #         break
                #
                #         # 5b. Remove original NotesEvent by root.remove(PatternID.Notes, id)
                #
                # if rootidx:
                #     t[0].pattern.events.root.remove(PatternID.Notes, rootidx)
                #         # 5c. Use the id to insert into the root event tree by root.insert(id, new_note_event)
                # if rootidx:
                #     t[0].pattern.events.root.insert(rootidx, note_event)


                pyflp.save(proj, "C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp")

            print(t[0].length) # length = ppq. In fl studio, a block of length 1 is 4 quarter notes, so a block of length 1 in fl studio is of length 4*ppq in the code.
            print(t[1].length)

            ## FIGURED OUT HOW TO MOVE TRACK ITEMS WITH t[i].position = k*ppq
            ## FIGURE OUT HOW TO ALTER THE LENGTH OF A TRACK ITEM; STUDY HOW OFFSET WORKS WITH THE PATTERN CLASS
            print(t[0].offsets)
            print(t[1].position)

            t[0].position = 384*2
            t[0].length = 384*2

            print(t[0].length)
            print(t[0].offsets)

            #pyflp.save(proj, "C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp")
            eventids = t.events.ids
            for pp in eventids:
                event1 = t.events.first(pp)
                # figuring out what an event is in a track... how to manipulate a track using events and event ids
            t.events.append(event1)







