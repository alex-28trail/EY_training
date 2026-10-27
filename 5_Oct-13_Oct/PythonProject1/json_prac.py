import pandas as pd
import json
#with open("support_tickets.json") as file:
#    tickets = json.load(file)

#print(tickets)

#print(tickets[0])
#print(tickets[0]["issue"])
#print(tickets[0]["customer"]["name"])

#for ticket in tickets:
 #   print(ticket["ticket_id"], ticket["issue"])

    #optional fieks

#print(tickets[0]["priority"])

#print(tickets[1].get("priority","not assigned"))

#df=pd.json_normalize(tickets)
#print(df)



#text files
with open("trail.txt") as f:
    trail = f.read()

print(trail)

words=trail.split()
print("Total words:",len(words))

#search
if "vibration" in trail.lower():
    print("vibration was mentioned")


#count occurance
print(trail.lower().count("vibration"))