import re

# Parameter field (\d+$)?
# flags Field [-\+ 0#]?
# Width field \d*  or with dynamic fields ([\d+(*d))?
# Percision field (\.\d+)?
# Type field [acdefignopsuxAFEGX]
# REGEXP = re.compile("%(\d+$)?[-\+ 0#]?\d+?[acdefignopsuxAFEGX]")

REGEXP = re.compile(r"%\d*(?:\.\d+)?[diksuxR]")

STRING_REGEXP = re.compile(r'"([^"]|\\"|(""))*"')

message_id = 0


def find(text):
    print(text)
    match = REGEXP.search(text)
    if match is None:
        print("NOT FOUND")
    else:
        print("{} start: {} end {}".format(
            match.group(0), match.start(), match.end()))
        for group in match.groups():
            print(group)


def shorten(text):
    global message_id
    message_id += 1
    count = text.count("%")
    if count == 0:
        return '"%u", {}'.format(message_id)
    else:
        result = '"%u'
        matches = REGEXP.findall(text)
        if len(matches) != count:
            raise Exception("Unexpected formatString in {}".format(text))
        for match in matches:
            result += " "
            result += match
        return result + '", {}'.format(message_id)


with open("/home/brenninc/spinnaker/sPyNNaker/neural_modelling/messages.txt") \
        as src:
    for line in src:
        print(line)
        text = STRING_REGEXP.search(line).group(0)
        print(shorten(text))
