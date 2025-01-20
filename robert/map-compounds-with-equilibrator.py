import equilibrator_api
if not "cc" in globals():
    cc = equilibrator_api.ComponentContribution


import pandas
## get file from: https://docs.google.com/spreadsheets/d/1YTiEAf4EVZaGsISSjGfCcEc-UOl1sQ8Z5WeXrIQa6nE/edit?gid=80878444#gid=80878444&fvid=2039963870
df = pandas.read_csv("~/online.csv")
df = df[df.kegg.isna()]

progress = 1
for i, row in df.iterrows():
    print(progress, "of", len(df))
    progress += 1
    print(i)
    print("searching...")
    cpd = cc.search_compound(row.compound_name)
    print("...done.")
    #cc.search_compound_by_inchi_key("YBAZINRZQSAIAY-UHFFFAOYSA-N")
    df.loc[i,"common_name"] = cpd.get_common_name()
    df.loc[i,"all_identifiers"] = str(cpd.identifiers)
    kegg_ids = []
    for id in cpd.identifiers:
        if id.registry.namespace == "kegg":
            kegg_ids.append(f"https://www.kegg.jp/entry/{id.accession}")
    df.loc[i,"kegg_links"] = str(kegg_ids)

    df.to_csv("annotated-equilibrator.csv", index=False)
