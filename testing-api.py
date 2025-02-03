# import flapi

# import general


# import arrangement
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

#desktop
#proj = pyflp.parse("C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp")

#laptop
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
                print(note)

                # create function to determine integer value of a key; ie: C0 = 0, C1 = 12, ...
                note.key = 'C5'
                note.length = note.length * 2
                #desktop
                #pyflp.save(proj, "C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp")

                #laptop
                pyflp.save(proj, "C:\\Users\\wbirm\\OneDrive\\Desktop\\dark melody drill.flp")

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

            pyflp.save(proj, "C:\\Users\\wbirm\\OneDrive\\Desktop\\Folders\\beats\\fls\\dark melody drill.flp")
            eventids = t.events.ids
            for pp in eventids:
                event1 = t.events.first(pp)
                # figuring out what an event is in a track... how to manipulate a track using events and event ids
            t.events.append(event1)







