tile_layout = []

with open("test.txt", "r") as file:
    lines = file.readlines()

    for line in lines:
        tile_layout.insert(0, [])
        for tile in line:
            try:
                tile_layout[0].append(int(tile))
            except ValueError:
                pass

print(tile_layout)