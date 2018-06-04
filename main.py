import os
import datetime

try:
    import bs4
except ImportError:
    bs4 = None
    print("This script requires the package \"Beautiful Soup 4\" to be installed.")
    exit()


class Message(object):
    def __init__(self, contents, sender, timestamp: datetime):
        self.contents = contents
        self.sender = sender
        self.timestamp = timestamp


def parse(data, contents):
    for element in contents:
        if element.find("img"):
            contents = os.path.abspath(element.find("img")["src"])

    if type(contents) is list:
        contents = contents[0].text

    return Message(
        contents,
        data.find("span", class_="user").text,
        datetime.datetime.strptime(
            data.find("span", class_="meta").text,
            "%A, %B %d, %Y at %I:%M%p %Z"
        )
    )


# Download a copy of your Facebook data.
# Find the HTML file for the chat you would like to parse in the "messages" directory.
print("Enter the name of the chat file. It must be in the same directory as this script. ")
filename = input("$ ").strip().strip(".")

if ".html" not in filename:
    filename = filename + ".html"

try:
    f = open(filename)
except FileNotFoundError:
    f = None
    print("File not found.")
    exit()

soup = bs4.BeautifulSoup(f, "html.parser")
f.close()

# Removes the first two children from div.thread.
# These are the name of the chat and its participants.
thread = list(soup.find("div", class_="thread").children)[2:]

# Removes all newline elements from div.thread.
thread = [a for a in thread if a != "\n"]

i = 0
while i < len(thread):
    raw = {
        "data": thread[i],
        "contents": []
    }
    j = 1
    while i + j < len(thread):
        if "class" in thread[i + j].attrs:
            if thread[i + j]["class"][0] == "message":
                break
        raw["contents"].append(thread[i + j])
        j = j + 1
    i = i + j

    message = parse(raw["data"], raw["contents"])

    # YOUR CODE HERE
    #
    # The Message class has attributes contents, sender, and timestamp.
    # The "message" variable above is an instance of this class.
    #
    # message.contents
    #   EITHER the text of the message
    #   OR, if the message was an image, its complete path.
    # message.sender
    #   The user who sent the message. Chat nicknames are not reflected.
    # message.timestamp
    #   The timestamp as a string. Any conversion to a datetime object must be performed by you.
    #   E.G. Tuesday, April 21, 2015 at 2:10pm EDT
