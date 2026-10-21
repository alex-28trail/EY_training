import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
data = {
    "Employee": ["Aisha", "Rahul", "Neha", "Omar", "Priya", "Karan", "Fatima", "Vikram"],
    "Department": ["HR", "IT", "Finance", "IT", "HR", "Finance", "IT", "HR"],
    "Training_Hours": [12, 18, 10, 22, 15, 8, 20, 14],
    "Assessment_Score": [78, 88, 72, 91, 84, 69, 95, 80],
    "Completed": ["Yes", "Yes", "No", "Yes", "Yes", "No", "Yes", "Yes"]
}

df = pd.DataFrame(data)

#1
print(df)

#2
print(df.head(4))

#3
print(df[["Employee","Assessment_Score"]])

#4
print(df[df.Department == "IT"])

#5
print(df[df.Assessment_Score > 80])

#6
print(df[df.Completed == "Yes"])

#7
print(df[(df["Department"] == "IT") & (df["Assessment_Score"] > 85)])

#8
df["Passed"]=np.where(df["Assessment_Score"]>=75, "Pass", "Fail")
print(df)

#9
print("Average score:", np.mean(df["Assessment_Score"]))

#10
print("Max score:", np.max(df["Assessment_Score"]))
print("Min score:", np.min(df["Assessment_Score"]))

#11
print("Average training hours:", np.mean(df["Training_Hours"]))

#12
print(df.sort_values( "Assessment_Score", ascending=False))

#13
print(df.groupby("Department")["Assessment_Score"].mean())

#14
print(df.groupby("Department")["Training_Hours"].sum())

#15
print(df.groupby("Department")["Employee"].count())

#16
print(df.groupby("Completed")["Employee"].count())

#17
scores=df["Assessment_Score"].to_numpy()
print("Mean score:", np.mean(scores))
print("Max score:", np.max(scores))
print("Min score:", np.min(scores))
print("Standard deviation:", np.std(scores))

#18
import matplotlib.pyplot as plt
sales=df.groupby("Department")["Assessment_Score"].mean()
sales.plot(kind="bar")
plt.title("Department by Score")
plt.xlabel("Department")
plt.ylabel("Assessment Score")
plt.show()


#19
