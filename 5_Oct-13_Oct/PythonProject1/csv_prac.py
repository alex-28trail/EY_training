import pandas as pd

df=pd.read_csv("ev_session.csv")
print(df)

print(df.columns)
print(df.shape)
print(df.dtypes)
print(df[["Station", "kWh","Amount"]])