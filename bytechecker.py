javaf = open("java.csv", "r")
javadata = list()
for line in javaf:
    javadata.append(line.split(","))

pythonf = open("python.csv", "r")
pythondata = list()
for line in pythonf:
    pythondata.append(line.split(","))

print(len(javadata) == len(pythondata))
for row in range(len(javadata)):
    for col in range(len(javadata[row])):
        if (javadata[row][col] != pythondata[row][col]):
            print(row, col, javadata[row][col], pythondata[row][col])
