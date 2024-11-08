parts = 8

for i in range(parts):
    output = open(f"output_{i}.txt","r",encoding='utf-8')
    lines = output.readlines()
    print(f"output_{i}.txt")
    print(lines)
    for line in lines:
        if line.startswith("exclude"):
            print(line.rstrip('\n'))