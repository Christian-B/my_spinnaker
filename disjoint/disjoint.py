all_sets = []

def add_set(new_set):
    for a_set in all_sets:
        intersection =  new_set & a_set
        if intersection:
            all_sets.remove(a_set)
            union = a_set | new_set
            add_set(union)
            return
    all_sets.append(new_set)
    return

if __name__ == '__main__':
