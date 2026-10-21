import numpy as np
import pandas as pd

df=pd.read_csv("library_loans.csv")
print(df)

print(df[["Member_Name", "Book_Category", "Fine"]])
print(df[df.Fine > 80])

df["Status"]=np.where(df["Fine"]==0, "No Fine", "Due")
print(df)

# print("Avg Days Borrowed",np.mean(df["Days_Borrowed"]))
# print(df.groupby("Book_Category")["Fine"].sum())