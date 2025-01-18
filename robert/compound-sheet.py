# coding: utf-8
import pandas

if not "df" in locals():
    print("reading file 1")
    # get this file from https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/edit?gid=652907302#gid=652907302
    df = pandas.read_excel("2024-01-00_openTECR_recuration/openTECR recuration.ods", sheet_name="table metadata")

if not "actual_data" in locals():
    print("reading second sheet in file 1")
    actual_data = pandas.read_excel("2024-01-00_openTECR_recuration/openTECR recuration.ods", sheet_name="actual data")
    actual_data = actual_data[actual_data["entry nr"] != "error"]
    actual_data = actual_data[actual_data["entry nr"] != "duplicate"]
    actual_data = actual_data[~actual_data.duplicated(['part', 'page', 'col l/r', 'table from top'])]

if not "noor" in locals():
    print("reading file 2")
    # get this file from https://zenodo.org/records/5495826
    noor = pandas.read_csv("TECRDB.csv")

merged = actual_data.drop(["reference_code", "reaction"], axis="columns").merge(df, on=['part', 'page', 'col l/r', 'table from top'], validate="1:1").merge(noor, on="id", how="left")
merged.reaction_y = merged.reaction_y.fillna("")
print("start...")

KNOWN_EXCEPTIONS = [
    ## start of block...
    # in some reactions, beta enantiomer is specifically mentioned and shall not be misannotated:
    ('C00092', 'D-glucose 6-phosphate', '{\\beta}-D-glucose 6-phosphate'),
    # C00103 is the alpha isomer, not beta:
    ('C00103', '{\\alpha}-D-glucose 1-phosphate', '{\\beta}-D-glucose 1-phosphate'),
    # C00877 is the trans isomer:
    ('C00877', 'cis-but-2-enoyl-CoA', 'trans-but-2-enoyl-CoA'),
    ('C00877', 'cis-but-2-enoyl-CoA', 'trans-but-2-enoyl-coenzyme A'),
    # specific enantiomer not the same as racemic mixture:
    ('C01144', '(S)-3-hydroxybutanoyl-CoA', 'DL-3-hydroxybutanoyl-CoA'),
    # C00252 is without stereo:
    ('C00252', 'isomaltose', '{\\alpha}-isomaltose'),
    ('C00252', 'isomaltose', '{\\beta}-isomaltose'),
    # C02557 is without stereo; C00683 would be the (S) enantiomer:
    ('C02557', 'methylmalonyl-CoA', '(S)-methylmalonyl-CoA'),
    # C03912 is the (S) stereoisomer (same as L)!
    ('C03912', '{\\Delta}-1-pyrroline-5-carboxylate', 'DL-{\\Delta}-1-pyrroline-5-carboxylate'),
    # C05402 is the alpha isomer, but naming is strange anyway:
    ('C05402', '{\\alpha}-D-melibiose', '{\\beta}-D-melibiose'),
    ## ...end of block

    ## equivalence / correctness would need to be checked in detail
    # C03652 is the specific stereoisomer, but the name "2,3-dimethylmalate" is not stereospecific
    ('C03652', '2,3-dimethylmalate', '(2R,3S)-2,3-dimethylmalate'),
    # C05984 is the specific stereoisomer, but the name "2-hydroxybutanoate" is not stereospecific
    ('C05984', '2-hydroxybutanoate', 'D-2-hydroxy-n-butanoate'),


    ## okay if annotated uniformly / consistently like this:
    ('C00031', '{\\beta}-D-glucose', 'D-glucose'),
    ('C00092', 'D-glucose 6-phosphate', '{\\alpha}-D-glucose 6-phosphate'),
    ('C00103', '{\\alpha}-D-glucose 1-phosphate', 'D-glucose 1-phosphate'),
    ('C00620', '{\\alpha}-D-ribose 1-phosphate', 'D-ribose 1-phosphate'),
    ('C00636', '{\\alpha}-D-mannose 1-phosphate', 'D-mannose 1-phosphate'),
    ('C04256', 'N-acetyl-{\\alpha}-D-glucosamine 1-phosphate', 'N-acetyl-D-glucosamine 1-phosphate'),

    ## here come confirmed synonyms:
    ('C00003', 'NAD', 'NAD(ox)'),
    ('C00004', 'NADH', 'NAD(red)'),
    ('C00005', 'NADPH', 'NADP(red)'),
    ('C00006', 'NADP', 'NADP(ox)'),
    ('C00009', 'orthophosphate', 'HPO4'),
    ('C00009', 'orthophosphate', 'phosphate'),
    ('C00013', 'pyrophosphate', 'diphosphate'),
    ('C00051', 'reduced glutathione', 'glutathione (reduced)'),
    ('C00051', 'reduced glutathione', 'glutathione(red)'),
    ('C00081', "inosine 5'-triphosphate", 'ITP'),
    ('C00100', 'propanoyl-CoA', 'propionyl-CoA'),
    ('C00101', '5,6,7,8-tetrahydrofolate', 'tetrahydrofolate'),
    ('C00104', "inosine 5'-diphosphate", 'IDP'),
    ('C00111', 'dihydroxyacetone phosphate', 'glycerone phosphate'),
    ('C00118', 'D-glyceraldehyde 3-phosphate', 'D-glyceraldehyde-3-phosphate'),
    ('C00127', 'oxidized glutathione', 'glutathione(ox)'),
    ('C00144', 'GMP', "guanosine 5'-phosphate"),
    ('C00164', '3-oxobutanoate', 'acetoacetate'),
    ('C00166', 'keto-phenylpyruvate', 'phenylpyruvate'),
    ('C00224', "adenosine 5'-phosphosulfate", 'adenylyl sulfate'),
    ('C00224', "adenosine 5'-phosphosulfate", 'adenylylsulfate'),
    ('C00332', '3-oxobutanoyl-CoA', 'acetoacetyl-CoA'),
    ('C00360', 'dAMP', "2'-deoxyadenosine 5'-monophosphate"),
    ('C00376', 'vitamin A aldehyde', 'all-trans-retinal'),
    ('C00415', '7,8-dihydrofolate', 'dihydrofolate'),
    ('C00424', 'L-lactaldehyde', '(S)-lactaldehyde'),
    ('C00441', 'L-aspartate 4-semialdehyde', 'L-aspartate-4-semialdehyde'),
    ('C00473', 'vitamin A alcohol', 'retinol'),
    ('C00522', 'pantoic acid', '(R)-pantoate'),
    ('C00577', '(R)-glyceraldehyde', 'D-glyceraldehyde'),
    ('C00644', 'D-mannitol 1-phosphate', 'D-mannitol-1-phosphate'),
    ('C00794', 'D-sorbitol', 'D-glucitol'),
    ('C00942', "guanosine 3':5'-(cyclic)phosphate", "guanosine 3':5'-cyclic phosphate"),
    ('C00944', '5-dehydroquinate', '3-dehydroquinate'),
    ('C01005', 'O-phospho-L-serine', 'L-O-phosphoserine'),
    ('C01144', '(S)-3-hydroxybutanoyl-CoA', '(3S)-3-hydroxybutanoyl-CoA'),
    ('C01144', '(S)-3-hydroxybutanoyl-CoA', '(3S)-hydroxybutanoyl-coenzyme A'),
    ('C01182', 'D-ribulose 1,5-biphosphate', 'D-ribulose 1,5-bisphosphate'),
    ('C01996', 'O-acetylcholine', 'acetylcholine'),
    ('C02637', '5-dehydroshikimate', '3-dehydroshikimate'),
    ('C03082', 'L-4-aspartyl phosphate', '4-phospho-L-aspartate'),
    ('C03149', 'N{\\omega}-phosphotaurocyamine', 'phosphotaurocyamine'),
    ('C03232', '3-phosphohydroxypyruvate', '3-phosphonooxypyruvate'),
    ('C03232', '3-phosphohydroxypyruvate', '3-phosphono-oxypyruvate'),
    ('C03406', 'N-(L-argino)succinate', 'L-arginosuccinate'),
    ('C03459', '2-oxo-3-hydroxysuccinate', '2-oxo-3-hydroxybutanedioic acid'),
    ('C03943', '2,4-diaminopentanoate', 'D-threo-2,4-diaminopentanoate'),
    ('C05268', '(S)-3-hydroxyhexanoyl-CoA', '(3S)-3-hydroxyhexanoyl-CoA'),
]

KNOWN_REACTIONS_TO_SKIP_FOR_NOW = [
    # Noor transcribed the entry as cellotriose (the trimer) whereas the Goldberg review says it is cellobiose (the dimer):
    "cellobiose(aq) + orthophosphate(aq) = D-glucose(aq) + {\\alpha}-D-glucose 1-phosphate(aq)",
    # start of block ...
    # the following reactions are to be skipped because they included a water molecule in the Noor dataset:
    "6-phospho-D-gluconate(aq) + NADP(aq) = D-ribulose 5-phosphate(aq) + NADPH(aq) + carbon dioxide(aq)",
    "formate(aq) + NAD(aq) = carbon dioxide(aq) + NADH(aq)",
    "formate(aq) + NADP(aq) = carbon dioxide(aq) + NADPH(aq)",
    "ATP^{4-}(aq) + H2O(l) = ADP^{3-}(aq) + HPO4^{2-}(aq) + H^{+}(aq)",
    "ADP^{3-}(aq) + H2O(l) = AMP^{2-}(aq) + HPO4^{2-}(aq) + H^{+}(aq)",
    "phosphocreatine(aq) = creatine(aq) + orthophosphate(aq)",
    "2 O2·(aq) + 2 H^{+}(aq) = O2(aq) + H2O2(aq)",
    # ... end of block.
]

compound_dict = {}
reverse_check = {}

## first run: extracts annotated compounds and checks them 
annotated_reactions_counter = 0
new_reaction_counter = 0
for i, row in merged.iterrows():
    print(i)
    if row.reaction_x in KNOWN_REACTIONS_TO_SKIP_FOR_NOW:
        print("this is an manual exception, skipping...")
        continue
    kegg_ids   = [foo.strip().replace("0.5 ", "")
                  .replace("2 ", "")
                  .replace("3 ", "")
                  .replace("4 ", "")
                  .replace("5 ", "")
                  .replace("6 ", "")
                  .replace("7 ", "")
                  .replace("8 ", "") for foo in list(row.reaction_y
                  .replace("=","+")
                  .replace("kegg:","")
                  .split(" + "))]
    free_texts = [foo.strip().replace("0.5 ", "")
                  .replace("2 ", "")
                  .replace("3 ", "")
                  .replace("4 ", "")
                  .replace("5 ", "")
                  .replace("6 ", "")
                  .replace("7 ", "")
                  .replace("8 ", "") for foo in list(row.reaction_x
                  .replace("(1)","(l)")
                  .replace("(aq)","")
                  .replace("(l)","")
                  .replace("(sln)","")
                  .replace("^{+}","")
                  .replace("^{-}", "")
                  .replace("^{2-}", "")
                  .replace("^{3-}", "")
                  .replace("^{4-}", "")
                  .replace("=","+")
                  .split(" + "))]
    part = row.part

    if kegg_ids == [""]:
        ### only consider annotated compounds in the first run
        print("not annotated yet, skipping...")
        new_reaction_counter += 1
        continue 
    if len(free_texts) != len(kegg_ids):
        print("differing amount of elements in free text (recurated) and KEGG ids (Noor)")
        print((free_texts, kegg_ids))
        if row.reaction_x != row.description:
            print("...reaction free text was changed, too")
            print(row.reaction_x)
            print(row.reaction_y)
            print(row.description)


    annotated_reactions_counter += 1

    for cpd, kegg in zip(free_texts, kegg_ids):
        #print(cpd,kegg)
        if cpd in compound_dict:
            if compound_dict[cpd]["kegg"]!=kegg:
                print(("compound exists already with different kegg!", compound_dict[cpd], cpd, kegg, row.reaction_x, row.description))
        else:
            compound_dict[cpd] = {"kegg": kegg, "number of involved reactions": 0}
        compound_dict[cpd].update({f"appears in part {str(int(part))}": 1})
        compound_dict[cpd]["number of involved reactions"] += 1

        if kegg in reverse_check:
            if (kegg, reverse_check[kegg], cpd) in KNOWN_EXCEPTIONS:
                continue
            #assert reverse_check[kegg] == cpd, (reverse_check[kegg], kegg, cpd)
            if reverse_check[kegg] != cpd:
                print(("reverse check failed!", row.reaction_x, row.description))
                print((kegg, reverse_check[kegg], cpd))
                continue
        reverse_check[kegg] = cpd

print("annotated_reactions_counter", annotated_reactions_counter)
print("new_reaction_counter: ", new_reaction_counter)



## second run: checks "new" reactions and tries to find existent annotations for its compounds 
new_reaction_counter = 0
for i, row in merged.iterrows():
    print(i)
    if row.reaction_x in KNOWN_REACTIONS_TO_SKIP_FOR_NOW:
        print("skipping.")
        continue
    kegg_ids   = [foo.strip().replace("0.5 ", "")
                  .replace("2 ", "")
                  .replace("3 ", "")
                  .replace("4 ", "")
                  .replace("5 ", "")
                  .replace("6 ", "")
                  .replace("7 ", "")
                  .replace("8 ", "") for foo in list(row.reaction_y
                  .replace("=","+")
                  .replace("kegg:","")
                  .split(" + "))]
    free_texts = [foo.strip().replace("0.5 ", "")
                  .replace("2 ", "")
                  .replace("3 ", "")
                  .replace("4 ", "")
                  .replace("5 ", "")
                  .replace("6 ", "")
                  .replace("7 ", "")
                  .replace("8 ", "") for foo in list(row.reaction_x
                  .replace("(1)","(l)")
                  .replace("(aq)","")
                  .replace("(l)","")
                  .replace("(sln)","")
                  .replace("^{+}","")
                  .replace("^{-}", "")
                  .replace("^{2-}", "")
                  .replace("^{3-}", "")
                  .replace("^{4-}", "")
                  .replace("=","+")
                  .split(" + "))]
    part = row.part

    if kegg_ids != [""]:
        ### only consider unannotated reactions in the second run
        continue 

    new_reaction_counter += 1

    print(len(free_texts))
    for cpd in free_texts:
        if cpd in compound_dict:
            if compound_dict[cpd]["kegg"] != "":
                print("could annotate a free-text from previously annotated compounds")
            else:
                print("could not annotate this free-text name: ", cpd)
        else:
            print("could not annotate this free-text name: ", cpd)
            compound_dict[cpd] = {"kegg": "", "number of involved reactions": 0}
        compound_dict[cpd].update({f"appears in part {str(int(part))}": 1})
        compound_dict[cpd]["number of involved reactions"] += 1

print("new_reaction_counter: ", new_reaction_counter)

output = pandas.DataFrame.from_dict(compound_dict).T
output["compound_name"] = output.index
output = output[["compound_name", "kegg", "number of involved reactions", "appears in part 1", "appears in part 2", "appears in part 3", "appears in part 4", "appears in part 5", "appears in part 6", "appears in part 7"]]
output.to_csv("out.csv", index=False)

output2 = output.copy()
output2.loc[:,"i"] = range(1,len(output2)+1)
output2 = output2[["i","compound_name", "number of involved reactions", "appears in part 1", "appears in part 2", "appears in part 3", "appears in part 4", "appears in part 5", "appears in part 6", "appears in part 7"]]
output2.to_csv("out2.csv", index=False)