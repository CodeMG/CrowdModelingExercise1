
def ReadInput(name: str):
    with open(name) as f:
        lines = f.readlines()

    dictionary = {}

    row = int(lines[0])

    column = int(lines[1])

    pedestrians = []
    p = int(lines[2])
    for i in range(3, 3+p):
        x = lines[i].split(", ")
        pedestrians.append(((int(x[0].strip()), int(x[1].strip())), float(x[2].strip())))

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
