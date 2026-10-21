with open("airport_operations_report.txt") as f:
    test = f.read()

print(test)

# 2
words=test.split()
print("Total words:",len(words))
with open("airport_operations_report.txt") as f:
    lines=f.readlines()
print("Total lines:",len(lines))
print("Total CHArs:",len(test))


if "maintenance" in test.lower():
    print("maintenance was mentioned")\

# 3
print("flight repeats")
print(test.lower().count("flight"))
print("runway repeats")
print(test.lower().count("runway"))
print("operations repeats")
print(test.lower().count("operations"))
print("reported repeats")
print(test.lower().count("reported"))

# 4
for i in lines:
    if "runway" in i.lower():
        print(i.strip())
# 5
for i in lines:
    if "delay" or "delayed" or"delays" in i.lower():
        print(i.strip())

#6

for i in lines:
    if "reported" in i.lower():
        print(i)
#7
keywords = [
    "emergency",
    "inspection",
    "weather",
    "passengers",
    "maintenance",
]

for i in keywords:
    if i.lower() in test:
        print(f"{i} : Found")
    else:
        print(f"{i} : Not Found")


