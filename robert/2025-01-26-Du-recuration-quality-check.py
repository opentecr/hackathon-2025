import pandas

READ_CSV = False

if READ_CSV:
    online = pandas.read_csv("openTECR recuration - compare Du with this.csv")
else:
    if not "online" in globals():
        online = pandas.read_excel("openTECR recuration.ods", sheet_name="compare Du with this")

## containing NaNs
print("containing NaNs:")
online_isna = online.isna()
subset=["part","page","col l/r","table from top", "entry nr"]
counter = 0
for row in online_isna.index:
    print_this = False
    for col in subset:
        if online_isna.loc[row,col]==True:
            print_this = True
    if print_this:
        #print(online.loc[row])
        counter += 1
print(f"A total of {counter} rows contained NaNs.")

## drop NaNs -- these entries just haven't been worked on
#online = online.dropna(subset=["part","page","col l/r","table from top", "entry nr"])

## convert to ints
#online[["part","page","col l/r","table from top", "entry nr"]] = online[["part","page","col l/r","table from top", "entry nr"]].astype(int)



## consistency check between online spreadsheet and original Du data
du1 = pandas.read_excel("doi 10.1016_j.bpj.2018.04.030 Supplementary mmc2.xlsx", sheet_name="Table S1. TECRDB Keqs")
du1 = du1.rename({"Reaction":"Enzyme", "Reaction.1": "Reaction"}, axis="columns")
du2 = pandas.read_excel("doi 10.1016_j.bpj.2018.04.030 Supplementary mmc2.xlsx", sheet_name="Table S2. TECRDB ΔrH data")

du = pandas.concat([du1, du2])

## check that all ids are still there
assert set(du["order id"]) - set(online["order id"]) == set(), f"The following IDs were deleted online: {set(du["order id"])-set(online["order id"])}"
## non-curated values should not have been changed by anyone!
leftjoined = pandas.merge(du, online, on="order id", how="left", validate="1:1")
SHOULD_BE_THE_SAME = [
    "Enzyme",
    "EC value",
    "Method",
    "Evaluation",
    "Reaction",
    "Reaction formula in CID format",
    "order",
    "Reaction formula in python dictionary",
    "T(K)",
    "pH",
    "Ionic strength",
    "pMg",
    "drH(kJ/mol)",
    "drH°(kJ/mol)",
    "drH'°(kJ/mol)",
    "Buffer/reagents/solute added",
    "Reference_id",
    "media conditions",
    "exclude",
]
for s in SHOULD_BE_THE_SAME:
    entries_where_both_are_nans = leftjoined[ leftjoined[f"{s}_x"].isna() & leftjoined[f"{s}_y"].isna() ]
    if len(entries_where_both_are_nans) == 0:
        #assert (leftjoined[f"{s}_x"] == leftjoined[f"{s}_y"]).all(), (s, print(leftjoined[~(leftjoined[f"{s}_x"] == leftjoined[f"{s}_y"])][["order id",f"{s}_x",f"{s}_y"]].to_string()))
        if not (leftjoined[f"{s}_x"] == leftjoined[f"{s}_y"]).all():
            print(leftjoined[~(leftjoined[f"{s}_x"] == leftjoined[f"{s}_y"])][["order id", f"{s}_x", f"{s}_y"]].to_string())
    else:
        tmp = leftjoined[ ~ (leftjoined[f"{s}_x"].isna() & leftjoined[f"{s}_y"].isna()) ]
        #assert (tmp[f"{s}_x"] == tmp[f"{s}_y"]).all(), (s, print(tmp[~(tmp[f"{s}_x"] == tmp[f"{s}_y"])][["order id",f"{s}_x",f"{s}_y"]].to_string()))
        if not (tmp[f"{s}_x"] == tmp[f"{s}_y"]).all():
            print(tmp[~(tmp[f"{s}_x"] == tmp[f"{s}_y"])][["order id",f"{s}_x",f"{s}_y"]].to_string())

print("The online spreadsheet data and its original data source are still in sync.")

