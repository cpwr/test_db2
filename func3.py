# I might suppose the answer on the assigned task is
def handle_list_of_tuples(l):
    return sorted(l, key=lambda x: (x[0], x[1], x[2], x[3]))


# but the desired answer could be obtained if use this function
def handle_list_of_tuples2(l):
    return sorted(
        sorted(l, key=lambda x: (x[0], x[1])),
        key=lambda x: (x[1], x[2]),
        reverse=True,
    )
