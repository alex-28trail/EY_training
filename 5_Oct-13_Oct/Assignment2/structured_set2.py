import pandas as pd
import numpy as np
df=pd.read_csv("renewable_energy.csv")
print(df)
# 2

print(df[df["Energy_Type"].isin(["Solar", "Wind"])])
# 3

df["Efficiency_Percent"]= (df["Actual_Output_MW"]/df["Capacity_MW"])*100

# 4
print(df[df.Efficiency_Percent>85])

# 5
print(df.groupby("Energy_Type")["Efficiency_Percent"].mean())

#6
print(df.groupby("Energy_Type")["Maintenance_Cost"].sum())
# 7
print(df.groupby("Plant_Name")["Actual_Output_MW"].max())
# 8
df["Cost_Per_MW"]= df["Maintenance_Cost"]/df["Actual_Output_MW"]
#9
print(df.sort_values("Cost_Per_MW"))

# 10
print(df[df.Efficiency_Percent < 80])
print(df[df.Maintenance_Cost < 70000])



