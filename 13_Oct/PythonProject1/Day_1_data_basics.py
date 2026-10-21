import pandas as pd
import matplotlib.pyplot as plt
data = {
    "Product": ["Laptop", "Mouse", "Keyboard", "Laptop", "Mouse"],
    "City": ["Hyderabad", "Mumbai", "Delhi", "Hyderabad", "Delhi"],
    "Quantity": [2, 5, 3, 1, 4],
    "Price": [60000, 800, 1500, 60000, 800]
}
#pandas
df = pd.DataFrame(data)
#print(df)

#print(df.shape)
#print(df.columns)
#print(df.dtypes)

#print(df[df.City == "hyderabad"])
#print(df[df.City == "Delhi"])


#numpy
df["Total"]=df["Quantity"]*df["Price"]
print(df)

print(df.groupby("Product")["Total"].sum())

print(df.sort_values("Total", ascending=False))


sales=df.groupby("Product")["Total"].sum()
sales.plot(kind="bar")

#matplot
#plt.title("Sales by Product")
#plt.xlabel("Product")
#plt.ylabel("Sales")
#plt.show()

#seaborn
import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(data=df, x="Product", y="Total")

plt.title("Sales by Product")
plt.show()