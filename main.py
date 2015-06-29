import re
import itertools

# DEBUG INPUT
input = "var I : [1,2,3,4]" + "\n"
input += "var J : [3,10]" + "\n"
input += "begin" + "\n"
input += "exp1,exp2,prob1" + "\n"
input += "exp3,exp4,prob2" + "\n"
input += "end"

# Parse Body
def parse_body(line):
    triple = []
    # include triple expression in array
    splitted = line.split(',')
    triple = [(splitted[0], splitted[1], splitted[2])]
    return triple

# Run algorithm
def run(variables, triples):
    list_of_names = ""
    # iterate over variables
    for (name, value_range) in variables:
        # create all variables
        exec("var_evalued_" + name + " = " + value_range)
        list_of_names += ", var_evalued_" + name
    # remove first comma and space
    list_of_names = list_of_names[2:]

    # generate the combination
    exec("combined = list(itertools.product(" + list_of_names + "))")

    return None

# BEGIN THE PARSER
input_lines = input.split("\n")
vars = []
triples = []
has_begin = False

for line in input_lines:
    #  variable definition
    if line[:3] == "var":
        # remove "var"
        line = re.sub(r"var\s*", "", line)
        # remove everything else var name
        var_name = re.sub(r"\h*:\s*.*", "", line).strip()
        # remove var name
        var_range = re.sub(r"\w+\s*:\s*", "", line).strip()
        # include tuple in array
        vars.append((var_name, var_range))

        continue

    if line[:5] == "begin":
        has_begin = True

        continue

    if line[:5] == "end":
        has_begin = False

        break

    if has_begin:
        triples += parse_body(line)

        continue

print(vars)
print(triples)
run(vars, triples)
