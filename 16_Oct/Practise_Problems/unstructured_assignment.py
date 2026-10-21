with open("unstructured_data.txt") as f:
    test = f.read()

print(test)

# 2
words=test.split()
print("Total words:",len(words))

# 4
if "maintenance" in test.lower():
    print("maintenance was mentioned")\

# 3
with open("unstructured_data.txt") as f:
    lines=f.readlines()
print("Total lines:",len(lines))
# 5
print("conveyor repeats")
print(test.lower().count("conveyor"))

#6
for i in lines:
    if "team" in i.lower():
        print(i.strip())

#7
for i in lines:
    if "incident" in i.lower():
        print(i.strip())


# 8

for i in lines:
    if "damaged" in i.lower():
        print(i.strip())

# # 9
# lower_text = test.lower()
#
# with open("lowercase_report.txt", "w") as file:
#     file.write(lower_text)
#
# print("\nSaved lowercase_report.txt")

# 10
keywords = [
    "maintenance",
    "injuries",
    "inspection",
    "replacement",
    "operations"
]

for i in keywords:
    if i.lower() in test:
        print(f"{i} : Found")
    else:
        print(f"{i} : Not Found")