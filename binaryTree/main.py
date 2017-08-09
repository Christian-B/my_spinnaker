from binary_tree import BinaryTree


def check_list(a_list):
    tree = BinaryTree()
    for i in range(len(a_list)):
        tree.insert(a_list[i])
    assert tree.balanced()
    assert len(tree) == i + 1
    tree.show(6)
    print "====================================="
    print list(tree)


check_list([1, 2, 3])
check_list([500, 918, 224, 85, 8])
check_list([500, 918, 224, 85, 8, 223])
check_list([659, 361, 204, 116, 684, 305, 930, 845, 150, 155, 870, 898, 642,
            338, 815, 346, 351, 785, 421, 468, 225,   6, 414, 981, 712, 203,
            55, 537, 937, 459, 159, 522, 293, 679,   6, 605])
check_list([283, 404,  23, 590, 546,  53, 570, 846, 543, 300, 728, 347, 846,
            492, 982, 982, 597, 991, 726, 492])
check_list([283, 404,  23, 590, 546,  53, 570, 846, 543, 300, 728, 347, 846,
            492, 982, 597, 991, 726, 492, 490, 928, 894, 652, 768, 871, 377,
            866, 216, 126, 673, 308, 671, 324, 202, 695, 747, 978, 620, 447,
            405, 968, 195, 727, 395, 893, 229,  64,  61, 620, 618, 512, 818,
            376, 106, 646, 226,   9, 900, 134, 227, 769, 331, 213, 302,  14,
            929, 511, 894, 347, 873, 908, 714, 783, 635, 949, 912, 730, 593,
            733, 894, 345, 870, 853, 561, 477, 999, 206, 314, 332, 497, 703,
            510, 274, 163, 550, 910, 429, 592, 664, 797])
"""

#a_list = nprnd.randint(100000, size=100000)
#print a_list
#b = sorted(a_list)
#check_list(a_list)
"""
print "done"
