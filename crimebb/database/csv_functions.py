import pandas as pd

def convert_to_gb(row):
    if row["str_size"].lower()=="kb":
        return row["num_size"]
    elif row["str_size"].lower()=="mb":
        return row["num_size"]*1000
    elif row["str_size"].lower()=="gb":
        return row["num_size"]*1000000


def plot_db_sizes(db_dict, year_studied="2021"):
    db_df = pd.DataFrame(data=db_dict)
    db_df["num_size"] = db_df["size"].apply(lambda x: int(x.split(" ")[0]))
    db_df["str_size"] = db_df["size"].apply(lambda x: x.split(" ")[1])
    
    db_df["val_size"] = db_df.apply(lambda row: convert_to_gb(row), axis=1)
    
    if year_studied == "2019":
      db_df["db_name"] = db_df["db_name"].apply(lambda x: f'{x.split("_")[-1]}-{x.split("_")[1]}')
    
    db_df.set_index("db_name", inplace=True)
    db_df.sort_values(by="val_size", ascending=False, inplace=True)
    
    mean_val = db_df["val_size"].mean()

    ax = db_df["val_size"].plot(kind="bar", figsize=(16,8), title=f"DB sizes (in kB): {round(mean_val, 2)} kB", xlabel="DB name", ylabel="Size (Kb)", rot=45)
    
    return db_df
