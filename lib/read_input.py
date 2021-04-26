
def ReadInput(name: str):
    with open(name) as f:
        lines = f.readlines()

    dictionary = {}

    row = int(lines[0])

    column = int(lines[1])

    pedestrians = []
    p = int(lines[2])
    for i in range(3, 3+p):
        pedestrians.insert(i, eval(lines[i]))

    obstacles = []
    o = int(lines[3+p])
    for i in range(4+p, 4+p+o):
        obstacles.insert(i, eval(lines[i]))

    target = eval(lines[4+p+o])

    dictionary.update(
        [
            ('row', row),
            ('column', column),
            ('pedestrians', pedestrians),
            ('obstacles', obstacles),
            ('target', target)
        ],
    )
    return dictionary