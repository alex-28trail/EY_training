import pandas as pd
import json
import numpy as np
with open("festival_events.json") as file:
    fest = json.load(file)

print(fest)
df=pd.read_json("festival_events.json")
print(df)

print(df[["name"]])
print(df[["name","location"]])

#print(tickets[0])
#print(tickets[0]["issue"])
#print(tickets[0]["customer"]["name"])

#for ticket in tickets:
 #   print(ticket["ticket_id"], ticket["issue"])