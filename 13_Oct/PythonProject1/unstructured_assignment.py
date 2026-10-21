with open("wildlife_report.txt") as f:
    trail = f.read()

print(trail)

words=trail.split()
print("Total words:",len(words))

#search
if "elephant" in trail.lower():
    print("elephant was mentioned")


print(trail.lower().count("elephant"))