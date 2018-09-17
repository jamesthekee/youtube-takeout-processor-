URL_TEXT = '<a href="https://www.youtube.com/watch?v='
CHANNEL_TEXT = '<a href="https://www.youtube.com/channel/'
URL_LENGTH = len("l6yOx6BbfA8")
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def data_parser(directory):
    try:
        html_file = open(file=directory, mode="r", encoding="utf-8")
    except FileNotFoundError:
        print(directory + " does not exist")
        return []

    # Find the distance in characters between the end of an entry in the history and the beginning of the next one
    # As it does not seem uniform for my various files
    with open(file=directory, mode="r", encoding="utf-8") as f:
        text = f.read()
        temp = text.find(URL_TEXT)
        text = text[temp + len(URL_TEXT):]
        text = text[text.find("</div><div"):]
        entry_gap = text.find(URL_TEXT)

    source = html_file.read()
    length = len(source)
    pointer = 0

    def find(string):
        cpointer = pointer
        while source[cpointer: cpointer + len(string)] != string:
            cpointer += 1
        return cpointer

    history = []
    pointer = source.find(URL_TEXT)

    while pointer < length:
        pointer = find(URL_TEXT) + len(URL_TEXT)

        temp = pointer + URL_LENGTH
        url = source[pointer: temp]
        pointer = find('</a>')
        title = source[temp + 2: pointer]

        # Put in special characters
        title = title.replace("&#39;", "'").replace("&quot;", '"').replace("&amp;", '&')

        # If channel deleted
        if 'https://www.youtube.com/watch?v=' + url == title:
            pointer += len("</a><br>")

            temp = find('</div><div')
            date = source[pointer: temp]
            pointer = temp + 780

            date = date.split(", ")
            dmy = date[0].split(" ")
            for (index, item) in enumerate(MONTHS):
                if item == dmy[1]:
                    dmy[1] = str(index + 1)
            dmy = '/'.join(dmy)
            hms = date[1]

            data = (url, "X" * 24, dmy, hms, title, "Deleted User")
        # If channel not deleted
        else:
            pointer += 49
            channel_id = source[pointer: pointer + 24]

            pointer += 24 + 2
            temp = find('</a><br>')
            author = source[pointer: temp]
            pointer = temp + len('</a><br>')

            # Put in special characters
            author = author.replace("&#39;", "'").replace("&quot;", '"').replace("&amp;", '&')

            temp = find('</div><div')
            date = source[pointer: temp]
            pointer = temp + entry_gap

            # Date formatting

            # dates do not come in uniform format, sometimes strings appear not as
            # 26 May 2018, 15:17:14
            # but as
            # Watched at 14:07
            # 26 May 2018, 13:31:25
            if len(date) > 21:
                date = date[date.find('<')+4:]

            date = date.split(", ")
            dmy = date[0].split(" ")
            for (index, item) in enumerate(MONTHS):
                if item == dmy[1]:
                    dmy[1] = str(index + 1)
            dmy = '/'.join(dmy)
            hms = date[1]

            data = (title, author, dmy, hms, url, channel_id)  # (url, channel_id, dmy, hms, title, author)
        history.append(data)
    return history
