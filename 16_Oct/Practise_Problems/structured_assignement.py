import pandas as pd
import numpy as np
df=pd.read_csv("structured_data.csv")
print(df)
# 2
print(df[["Shipment_ID","Origin","Destination","Cost"]])

# 3
print(df[df['Mode'] == 'Road'])

# 4
print(df[df.Weight_Kg>150])

# 5
df["Cost_Per_Km"]= df["Cost"]/df["Distance_Km"]
print(df)

#6

print("Avg_Shipment_Cost",np.average(df["Cost"]))
print("Highest_Shipment_Cost",np.max(df["Cost"]))
print("Lowest_Shipment_Cost",np.min(df["Cost"]))

# 7

print(df.groupby("Mode")["Cost"].sum())
# 8
print(df.groupby("Mode")["Weight_Kg"].mean())
# 9
print(df.sort_values("Cost", ascending=False))
# 10.
print(df[df.Delivery_Days <= 1])
print(df[df.Cost  < 5000])