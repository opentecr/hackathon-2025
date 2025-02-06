

#!wget -O "openTECR recuration - compare Du with this.csv" "https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/export?format=csv&gid=1051830387"
#!wget -O "openTECR recuration - actual data.csv" "https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/export?format=csv&gid=2123069643"
#!wget -O "openTECR recuration - table codes.csv" "https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/export?format=csv&gid=831893235"

# !wget -O "openTECR recuration - table metadata.csv" "https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/export?format=csv&gid=1475422539"
# !wget -O "openTECR recuration.ods" "https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/export?format=ods"
# !wget -O "TECRDB.csv" "https://w3id.org/related-to/doi.org/10.5281/zenodo.3978439/files/TECRDB.csv"

#!pip install odfpy
## Installing library for processing .ods file

import pandas

df = pandas.read_csv("openTECR recuration - actual data.csv")
df = df.replace({"col l/r": {"l":1,"r":2}}) ##replaced l and r in col l/r with 1 and 2
df = df.dropna(subset=["part","page","col l/r","table from top", "entry nr"])
df = df[~((df["entry nr"]=="duplicate") | (df["entry nr"]=="error"))]
df[["part","page","col l/r","table from top", "entry nr"]] = df[["part","page","col l/r","table from top", "entry nr"]].astype(int)

## unify K and Kprime
for i, row in df.iterrows():
    _K = ""
    if not pandas.isna(row["K"]):
        _K = row["K"]
    elif not pandas.isna(row["K_prime"]):
        _K = row["K_prime"]
    df.loc[i, "Keq"] = _K



du = pandas.read_csv("openTECR recuration - compare Du with this.csv")
du = du[~((du["entry nr"]=="new") | (du["entry nr"]=="duplicate") | (du["entry nr"]=="virtual"))]
du[["part","page","col l/r","table from top", "entry nr"]] = du[["part","page","col l/r","table from top", "entry nr"]].astype(int)

## unify enthalpies
for i, row in du.iterrows():
    _enthalpy = ""
    if not pandas.isna(row["drH(kJ/mol)"]) and not row["drH(kJ/mol)"] == "-":
        _enthalpy = row["drH(kJ/mol)"]
    elif not pandas.isna(row["drH°(kJ/mol)"]) and not row["drH°(kJ/mol)"] == "-":
        _enthalpy = row["drH°(kJ/mol)"]
    elif not pandas.isna(row["drH'°(kJ/mol)"]) and not row["drH'°(kJ/mol)"] == "-":
        _enthalpy = row["drH'°(kJ/mol)"]
    du.loc[i, "enthalpy"] = _enthalpy


merged_du_df = du.merge(df, on=["part","page","col l/r","table from top", "entry nr"], how="left", validate="1:1")
leftjoined = merged_du_df

## Columns that should be the same
SHOULD_BE_THE_SAME = [
    # this     Du      Noor
    ("temp",   "T(K)", "temperature"),
    ("ph",     "pH", "p_h"),
    ("ionst",  "Ionic strength", "ionic_strength"),
    ("pmg",    "pMg", "p_mg"),
    ("eq",     "K'", "Keq"),
    ("enth",   "enthalpy_x", "enthalpy_y"),
]
for s, x, y in SHOULD_BE_THE_SAME:
    # entries_where_both_are_nans = leftjoined[ leftjoined[f"{x}"].isna() & leftjoined[f"{y}"].isna() ]
    # if len(entries_where_both_are_nans) == 0:
    #     if not (leftjoined[f"{x}"] == leftjoined[f"{y}"]).all():
    #         print(x, leftjoined[~(leftjoined[f"{x}"] == leftjoined[f"{y}"])][["id",f"{x}",f"{y}"]].to_string())
    # else:
    #     tmp = leftjoined[ ~ (leftjoined[f"{x}"].isna() & leftjoined[f"{y}"].isna()) ]
    #     if not (tmp[f"{x}"] == tmp[f"{y}"]).all():
    #         print(x, tmp[~(tmp[f"{x}"] == tmp[f"{y}"])][["id",f"{x}",f"{y}"]].to_string())
    #

    leftjoined[x] = pandas.to_numeric(leftjoined[x], errors="coerce")
    leftjoined[y] = pandas.to_numeric(leftjoined[y], errors="coerce")

    selector = ( leftjoined[x].isna() & leftjoined[y].isna() )
    subset = leftjoined[ selector ]
    leftjoined.loc[ subset.index, f"deviation_relative_{s}"] = ""
    leftjoined.loc[ subset.index, f"deviation_absolute_{s}"] = ""

    selector = (leftjoined[x].isna() ^ leftjoined[y].isna())
    subset = leftjoined[selector]
    leftjoined.loc[subset.index, f"deviation_relative_{s}"] = "only_one_nan"
    leftjoined.loc[subset.index, f"deviation_absolute_{s}"] = "only_one_nan"

    selector = ~( leftjoined[x].isna() | leftjoined[y].isna() )
    subset = leftjoined[ selector ]
    leftjoined.loc[ subset.index, f"deviation_relative_{s}"] = subset[x] / subset[y] - 1.
    leftjoined.loc[ subset.index, f"deviation_absolute_{s}"] = subset[x] - subset[y]

which_columns_to_keep = []
which_columns_to_keep.extend(["order id", "reference_code", "part","page","col l/r","table from top", "entry nr"])
for s, x, y in SHOULD_BE_THE_SAME:
    which_columns_to_keep.extend([x,y])
    which_columns_to_keep.append(f"deviation_relative_{s}")
    which_columns_to_keep.append(f"deviation_absolute_{s}")

leftjoined[which_columns_to_keep].to_csv("du-noor.out.csv", index=False)