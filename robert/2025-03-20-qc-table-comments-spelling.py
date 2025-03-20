# coding: utf-8
import pandas
df = pandas.read_csv("openTECR recuration - table comments.csv")

for i, row in df.iterrows():
    error = False
    if "Kc'" in row.comment: error = True
    if "NH^{+}(aq)" in row.comment: error = True
    if "dm- " in row.comment: error=True
    if "dm " in row.comment: error=True

    if "  " in row.comment: error=True


    if re.search("dm-[^3]", row.comment): error=True
    if re.search("mol-[^1]", row.comment): error=True

    if re.search("[^\\\\]alpha", row.comment): error=True
    if re.search("[^\\\\]beta", row.comment): error=True

    if re.search("~[^=]", row.comment): error=True
    
    if " ±" in row.comment: error=True
    if "± " in row.comment: error=True
    if "- " in row.comment: 
        if not ("--" in row.comment or "D- and L-" in row.comment):
             error=True

    if error: print(row)

# get all backslash commands
collector = []
for i, row in df.iterrows():
    match = re.search("(\\\\[^\\s]*) ", row.comment)
    if match:
        collector.extend(match.groups())
print(set(collector))

# get all exponents
collector = []
for i, row in df.iterrows():
    match = re.search("\\^\\{(.*?)\\}", row.comment)
    if match:
        collector.extend(match.groups())
print(set(collector))

# get all occurences of = without space around it
collector = []
for i, row in df.iterrows():
    match = re.search("([^\\s]*?=[^\\s]*?)", row.comment)
    if match:
        print(match.groups())
        collector.extend(match.groups())
print(set(collector))
# {"=", "~=", "<=", ">="}



match
match.match
dir(match)
match.groups
match.group
match.pos
match.re
match.regs
match.span
match.string
