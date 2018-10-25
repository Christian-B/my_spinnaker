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
        return "overlap"
    return "distinct"


def not_covered(first, second):
    uncovered = []
    for i in range(len(first)):
        if second[i] == "X":
            if first[i] == "0":
                uncovered.append(second[:i] + "1" + second[i+1:])
            elif first[i] == "1":
                uncovered.append(second[:i] + "0" + second[i+1:])
    return uncovered


for pattern1 in patterns("", 2):
    for pattern2 in patterns("", 2):
        if compare(pattern1, pattern2) in ["overlap", "wider"]:
            print(pattern1, pattern2, compare(pattern1, pattern2),
                  not_covered(pattern1, pattern2))
