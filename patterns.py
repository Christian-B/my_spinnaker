def patterns(str, remaining):
    if remaining == 0:
        yield str
    else:
        for pattern in patterns(str + "1", remaining-1):
            yield pattern
        for pattern in patterns(str + "0", remaining-1):
            yield pattern
        for pattern in patterns(str + "X", remaining-1):
            yield pattern

def compare(pattern1, pattern2):
    if pattern1 == pattern2:
        return "equals"
    if pattern1[0] == pattern2[0]:
        return compare(pattern1[1:], pattern2[1:])
    if pattern2[0] == "X":
        remainder = compare(pattern1[1:], pattern2[1:])
        if remainder in ["wider", "equals"]:
            return "wider"
        if remainder == "distinct":
            return "distinct"
        return "todo"
    if pattern1[0] == "X":
        remainder = compare(pattern1[1:], pattern2[1:])
        if remainder in ["narrower", "equals"]:
            return "narrower"
        if remainder == "distinct":
            return "distinct"
        return "todo"
    return "distinct"


for pattern1 in patterns("", 2):
    for pattern2 in patterns("", 2):
        if compare(pattern1, pattern2) == "todo":
            print pattern1, pattern2, compare(pattern1, pattern2)