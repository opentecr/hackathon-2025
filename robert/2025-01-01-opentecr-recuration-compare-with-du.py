import pandas

if not "df_original" in globals():
    df_original = pandas.read_excel("openTECR recuration.ods", sheet_name="actual data")

df = df_original.copy()
df = df.replace({"col l/r": {"l":1,"r":2}})
df = df[~(df["entry nr"]=="error")]
df = df[~(df["entry nr"]=="duplicate")]
#df = df.dropna(subset=["part","page","col l/r","table from top", "entry nr"])
df[["part","page","col l/r","table from top", "entry nr"]] = df[["part","page","col l/r","table from top", "entry nr"]].astype(int)
df = df.drop(["EC","reference_code","reaction"], axis="columns")

if not "df2_original" in globals():
    df2_original = pandas.read_excel("openTECR recuration.ods", sheet_name="table metadata")

df2 = df2_original.copy()
df2[["part","page","col l/r","table from top"]] = df2[["part","page","col l/r","table from top"]].astype(int)
df2 = df2.drop(["method","buffer","pH","Cofactor","Evaluation","effort_needed","table_code","ECNumber","Enzyme"], axis="columns")

tecrdb = df.merge(df2, on=["part","page","col l/r","table from top"], validate="m:1")
tecrdb.loc[:, "matched"] = 0
tecrdb.head()

du = pandas.read_excel("doi 10.1016_j.bpj.2018.04.030 Supplementary mmc2.xlsx", sheet_name="Table S1. TECRDB Keqs")
du[["part","page","col l/r","table from top", "entry nr", "matching comment", "matches"]] = ""
du = du.rename({"Reaction":"Enzyme", "Reaction.1": "Reaction"}, axis="columns")

this = tecrdb[tecrdb.enthalpy.isna()]
perfect_match = 0
zero_matches = 0
others = 0
for i, row in du.iterrows():
    print(i)
    matches = []
    if not pandas.isna(row["pH"]) and type(row["pH"])!=str and type(row["K'"]) != str:
        matches = this.query(f'reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} & p_h == {row["pH"]} & K_prime == {row["K'"]} ')
    else:
        matches = []
    du.loc[i, "matches"] = len(matches)
    if len(matches) == 1:
        du.loc[i, "matching comment"] = "full match, based on reference_code+Temperature+pH+enthalpy"
        for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
            du.loc[i, x] = matches.iloc[0][x]
        tecrdb.loc[matches.index, "matched"] += tecrdb.loc[matches.index, "matched"] + 1
        perfect_match += 1
        continue
    elif len(matches) > 1:
        ## unlikely ;)
        du.loc[i, "matching comment"] = ">1 match for this reference_code+Temperature+pH+Kprime"
        for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
            if len(matches[x].unique()) == 1:
                du.loc[i, x] = matches.iloc[0][x]
        others += 1
        ## try to get more specific...
        matches = this.query(
            f'reaction == "{row["Reaction"]}" & reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} & p_h == {row["pH"]} & K_prime == {row["K'"]} ')
        if len(matches) <= du.loc[i, "matches"]:
            du.loc[i, "matches"] = len(matches)
            for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                if len(matches[x].unique()) == 1:
                    du.loc[i, x] = matches.iloc[0][x]
            if len(matches) == 1:
                du.loc[i, "matching comment"] = "full match for this reaction+reference_code+Temperature+pH+enthalpy"
                others -= 1
                perfect_match += 1
                continue
            else:
                du.loc[i, "matching comment"] = ">1 match for this reaction+reference_code+Temperature+pH+enthalpy"
                continue
        else:
            continue
    elif len(matches) == 0:
        ## try to get more unspecific...
        if not pandas.isna(row["pH"]) and type(row["pH"]) != str:
            matches = this.query(
                f'reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} & p_h == {row["pH"]} ')
        else:
            matches = []
        du.loc[i, "matches"] = len(matches)
        if len(matches) == 1:
            du.loc[i, "matching comment"] = "1 match for this reference_code+Temperature+pH"
            for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                du.loc[i, x] = matches.iloc[0][x]
            tecrdb.loc[matches.index, "matched"] += 1
            perfect_match += 1
            continue
        elif len(matches) > 1:
            du.loc[i, "matching comment"] = ">1 match for this reference_code+Temperature+pH"
            for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                if len(matches[x].unique()) == 1:
                    du.loc[i, x] = matches.iloc[0][x]
            others += 1
            ## try to get more specific...
            matches = this.query(
                f'reaction == "{row["Reaction"]}" & reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} & p_h == {row["pH"]} ')
            if len(matches) <= du.loc[i, "matches"]:
                du.loc[i, "matches"] = len(matches)
                for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                    if len(matches[x].unique()) == 1:
                        du.loc[i, x] = matches.iloc[0][x]
                if len(matches) == 1:
                    du.loc[i, "matching comment"] = "full match for this reaction+reference_code+Temperature+pH"
                    others -= 1
                    perfect_match += 1
                    continue
                else:
                    du.loc[i, "matching comment"] = ">1 match for this reaction+reference_code+Temperature+pH"
                    continue
            else:
                continue
        elif len(matches) == 0:
            ## try to get more unspecific...
            matches = this.query(
                f'reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} ')
            du.loc[i, "matches"] = len(matches)
            if len(matches) == 1:
                du.loc[i, "matching comment"] = "1 match for this reference_code+Temperature"
                for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                    du.loc[i, x] = matches.iloc[0][x]
                tecrdb.loc[matches.index, "matched"] += 1
                perfect_match += 1
                continue
            elif len(matches) > 1:
                du.loc[i, "matching comment"] = ">1 match for this reference_code+Temperature"
                for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                    if len(matches[x].unique()) == 1:
                        du.loc[i, x] = matches.iloc[0][x]
                others += 1
                ## try to get more specific...
                matches = this.query(
                    f'reaction == "{row["Reaction"]}" & reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} ')
                if len(matches) <= du.loc[i, "matches"]:
                    du.loc[i, "matches"] = len(matches)
                    for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                        if len(matches[x].unique()) == 1:
                            du.loc[i, x] = matches.iloc[0][x]
                    if len(matches) == 1:
                        du.loc[i, "matching comment"] = "full match for this reaction+reference_code+Temperature"
                        others -= 1
                        perfect_match += 1
                        continue
                    else:
                        du.loc[i, "matching comment"] = ">1 match for this reaction+reference_code+Temperature"
                        continue
                else:
                    continue
            elif len(matches) == 0:
                ## try to get more unspecific...
                matches = this.query(f'reference_code == "{row["Reference_id"]}" ')
                du.loc[i, "matches"] = len(matches)
                if len(matches) == 1:
                    du.loc[i, "matching comment"] = "1 match for this reference_code"
                    for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                        du.loc[i, x] = matches.iloc[0][x]
                    tecrdb.loc[matches.index, "matched"] += 1
                    perfect_match += 1
                    continue
                elif len(matches) > 1:
                    du.loc[i, "matching comment"] = ">1 match for this reference_code"
                    for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                        if len(matches[x].unique()) == 1:
                            du.loc[i, x] = matches.iloc[0][x]
                    others += 1
                    ## try to get more specific...
                    matches = this.query(
                        f'reaction == "{row["Reaction"]}" & reference_code == "{row["Reference_id"]}" ')
                    if len(matches) <= du.loc[i, "matches"]:
                        du.loc[i, "matches"] = len(matches)
                        for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                            if len(matches[x].unique()) == 1:
                                du.loc[i, x] = matches.iloc[0][x]
                        if len(matches) == 1:
                            du.loc[i, "matching comment"] = "full match for this reaction+reference_code"
                            others -= 1
                            perfect_match += 1
                            continue
                        else:
                            du.loc[i, "matching comment"] = ">1 match for this reaction+reference_code"
                            continue
                    else:
                        continue
                elif len(matches) == 0:
                    du.loc[i, "matching comment"] = "0 matches for this reference_code"
                    zero_matches += 1
                    continue


print("perfect matches:" , perfect_match)
print("zero matches:" , zero_matches)
print("other non-matches:" , others)
du.to_csv("2025-01-01-opentecr-recuration-compare-with-du.py.out-keqs-matched.csv", index=False)
tecrdb.to_csv("2025-01-01-opentecr-recuration-compare-with-du.py.out-tecrdb-matched.csv", index=False)

print(tecrdb["matched"].unique())
print(tecrdb["matched"].sum())

du_in_storage = du.copy()

## enthalpies:
du = pandas.read_excel("doi 10.1016_j.bpj.2018.04.030 Supplementary mmc2.xlsx", sheet_name="Table S2. TECRDB ΔrH data")
du[["part","page","col l/r","table from top", "entry nr", "matching comment", "matches"]] = ""

this = tecrdb[~tecrdb.enthalpy.isna()]
perfect_match = 0
zero_matches = 0
others = 0
for i, row in du.iterrows():
    print(i)
    matches = []
    if not pandas.isna(row["pH"]) and type(row["pH"])!=str:
        if not pandas.isna(row["drH(kJ/mol)"]) and not row["drH(kJ/mol)"]=="-":
            _enthalpy = row["drH(kJ/mol)"]
        elif not pandas.isna(row["drH°(kJ/mol)"]) and not row["drH°(kJ/mol)"]=="-":
            _enthalpy = row["drH°(kJ/mol)"]
        elif not pandas.isna(row["drH'°(kJ/mol)"]) and not row["drH'°(kJ/mol)"]=="-":
            _enthalpy = row["drH'°(kJ/mol)"]
        else:
            _enthalpy = 0
        matches = this.query(f'reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} & p_h == {row["pH"]} & enthalpy == {_enthalpy} ')
    else:
        matches = []
    du.loc[i, "matches"] = len(matches)
    if len(matches) == 1:
        du.loc[i, "matching comment"] = "full match, based on reference_code+Temperature+pH+enthalpy"
        for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
            du.loc[i, x] = matches.iloc[0][x]
        tecrdb.loc[matches.index, "matched"] += tecrdb.loc[matches.index, "matched"] + 1
        perfect_match += 1
        continue
    elif len(matches) > 1:
        ## unlikely ;)
        du.loc[i, "matching comment"] = ">1 match for this reference_code+Temperature+pH+enthalpy"
        for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
            if len(matches[x].unique()) == 1:
                du.loc[i, x] = matches.iloc[0][x]
        others+=1
        ## try to get more specific...
        matches = this.query(f'reaction == "{row["Reaction"]}" & reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} & p_h == {row["pH"]} & enthalpy == {_enthalpy} ')
        if len(matches) <= du.loc[i, "matches"]:
            du.loc[i, "matches"] = len(matches)
            for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                if len(matches[x].unique()) == 1:
                    du.loc[i, x] = matches.iloc[0][x]
            if len(matches) == 1:
                du.loc[i, "matching comment"] = "full match for this reaction+reference_code+Temperature+pH+enthalpy"
                others -= 1
                perfect_match += 1
                continue
            else:
                du.loc[i, "matching comment"] = ">1 match for this reaction+reference_code+Temperature+pH+enthalpy"
                continue
        else:
            continue
    elif len(matches)==0:
        ## try to get more unspecific...
        if not pandas.isna(row["pH"]) and type(row["pH"]) != str :
            matches = this.query(
                f'reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} & p_h == {row["pH"]} ')
        else:
            matches = []
        du.loc[i, "matches"] = len(matches)
        if len(matches) == 1:
            du.loc[i, "matching comment"] = "1 match for this reference_code+Temperature+pH"
            for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                du.loc[i, x] = matches.iloc[0][x]
            tecrdb.loc[matches.index, "matched"] += 1
            perfect_match += 1
            continue
        elif len(matches) > 1:
            du.loc[i, "matching comment"] = ">1 match for this reference_code+Temperature+pH"
            for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                if len(matches[x].unique()) == 1:
                    du.loc[i, x] = matches.iloc[0][x]
            others += 1
            ## try to get more specific...
            matches = this.query(
                f'reaction == "{row["Reaction"]}" & reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} & p_h == {row["pH"]} ')
            if len(matches) <= du.loc[i, "matches"]:
                du.loc[i, "matches"] = len(matches)
                for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                    if len(matches[x].unique()) == 1:
                        du.loc[i, x] = matches.iloc[0][x]
                if len(matches) == 1:
                    du.loc[i, "matching comment"] = "full match for this reaction+reference_code+Temperature+pH"
                    others -= 1
                    perfect_match += 1
                    continue
                else:
                    du.loc[i, "matching comment"] = ">1 match for this reaction+reference_code+Temperature+pH"
                    continue
            else:
                continue
        elif len(matches) == 0:
            ## try to get more unspecific...
            matches = this.query(
                    f'reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} ')
            du.loc[i, "matches"] = len(matches)
            if len(matches) == 1:
                du.loc[i, "matching comment"] = "1 match for this reference_code+Temperature"
                for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                    du.loc[i, x] = matches.iloc[0][x]
                tecrdb.loc[matches.index, "matched"] += 1
                perfect_match += 1
                continue
            elif len(matches) > 1:
                du.loc[i, "matching comment"] = ">1 match for this reference_code+Temperature"
                for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                    if len(matches[x].unique()) == 1:
                        du.loc[i, x] = matches.iloc[0][x]
                others += 1
                ## try to get more specific...
                matches = this.query(
                    f'reaction == "{row["Reaction"]}" & reference_code == "{row["Reference_id"]}" & temperature == {row["T(K)"]} ')
                if len(matches) <= du.loc[i, "matches"]:
                    du.loc[i, "matches"] = len(matches)
                    for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                        if len(matches[x].unique()) == 1:
                            du.loc[i, x] = matches.iloc[0][x]
                    if len(matches) == 1:
                        du.loc[i, "matching comment"] = "full match for this reaction+reference_code+Temperature"
                        others -= 1
                        perfect_match += 1
                        continue
                    else:
                        du.loc[i, "matching comment"] = ">1 match for this reaction+reference_code+Temperature"
                        continue
                else:
                    continue
            elif len(matches) == 0:
                ## try to get more unspecific...
                matches = this.query(f'reference_code == "{row["Reference_id"]}" ')
                du.loc[i, "matches"] = len(matches)
                if len(matches) == 1:
                    du.loc[i, "matching comment"] = "1 match for this reference_code"
                    for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                        du.loc[i, x] = matches.iloc[0][x]
                    tecrdb.loc[matches.index, "matched"] += 1
                    perfect_match += 1
                    continue
                elif len(matches) > 1:
                    du.loc[i, "matching comment"] = ">1 match for this reference_code"
                    for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                        if len(matches[x].unique()) == 1:
                            du.loc[i, x] = matches.iloc[0][x]
                    others += 1
                    ## try to get more specific...
                    matches = this.query(
                        f'reaction == "{row["Reaction"]}" & reference_code == "{row["Reference_id"]}" ')
                    if len(matches) <= du.loc[i, "matches"]:
                        du.loc[i, "matches"] = len(matches)
                        for x in ["part", "page", "col l/r", "table from top", "entry nr"]:
                            if len(matches[x].unique()) == 1:
                                du.loc[i, x] = matches.iloc[0][x]
                        if len(matches) == 1:
                            du.loc[i, "matching comment"] = "full match for this reaction+reference_code"
                            others -= 1
                            perfect_match += 1
                            continue
                        else:
                            du.loc[i, "matching comment"] = ">1 match for this reaction+reference_code"
                            continue
                    else:
                        continue
                elif len(matches) == 0:
                    du.loc[i, "matching comment"] = "0 matches for this reference_code"
                    zero_matches += 1
                    continue

print("perfect matches:" , perfect_match)
print("zero matches:" , zero_matches)
print("other non-matches:" , others)
du.to_csv("2025-01-01-opentecr-recuration-compare-with-du.py.out-enthalpies-matched.csv", index=False)
tecrdb.to_csv("2025-01-01-opentecr-recuration-compare-with-du.py.out-tecrdb-matched.csv", index=False)

pandas.concat([du, du_in_storage]).to_csv("2025-01-01-opentecr-recuration-compare-with-du.py.out-keq-and-enthalpies-matched.csv", index=False)