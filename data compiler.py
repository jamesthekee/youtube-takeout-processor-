from os import walk
import dataparser
import datetime
import sqlite3

# Find youtube takeout folders
a = walk('Takeouts')
directories = a.__next__()[1]
# Folders should be automatically in chronological order


def strings_to_datetime(strings):
    dmy = strings[0].split('/')
    hms = strings[1].split(':')
    return datetime.datetime(int(dmy[2]), int(dmy[1]), int(dmy[0]), int(hms[0]), int(hms[1]), int(hms[2]))


# If folders exist
if directories:

    # Do first takeout file
    history = dataparser.data_parser('Takeouts/{}/Takeout/YouTube/history/watch-history.html'.format(directories[0]))
    start_date = history[0][2:4]
    start = strings_to_datetime(start_date)

    # Do the rest
    for i in directories[1:]:
        current_history = dataparser.data_parser('Takeouts/{}/Takeout/YouTube/history/watch-history.html'.format(i))
        # If empty - in case of FileNotFoundError
        if current_history:

            # Remove overlap of records from the multiple takeouts
            end = strings_to_datetime(current_history[-1][2:4])
            if start < end:
                history = current_history + history
            else:
                pointer = 0
                while current_history[pointer][2:4] != start_date and pointer < len(current_history):
                    pointer += 1
                history = current_history[:pointer] + history
            start_date = history[0][2:4]
    print("All data compiled")
    print("Writing to file")

    conn = sqlite3.connect("youtube-history.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history"
                   "(title TEXT, author TEXT, date TEXT, time TEXT, videoid TEXT, channelid TEXT)")

    cursor.executemany("INSERT INTO history VALUES (?, ?, ?, ?, ?, ?)", history)
    conn.commit()

    cursor.close()
    conn.close()






