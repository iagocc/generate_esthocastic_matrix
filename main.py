import re
import itertools
import numpy

# DEBUG INPUT
input = "var i : [1]" + "\n"
input += "var j : [3,4]" + "\n"
input += "begin" + "\n"
input += "i == 1 and j == 3, i == 1 and j == 3, 0.5" + "\n"
input += "i == 1 and j == 3, i == 1 and j == 4, 0.5" + "\n"
input += "i == 1 and j == 4, i == 1 and j == 3, 0.667" + "\n"
input += "i == 1 and j == 4, i == 1 and j == 4, 0.333" + "\n"
input += "end"

# Parse Body
def parse_body(line):
    triple = []
    # include triple expression in array
    splitted = line.split(',')
    triple = [(splitted[0].strip(), splitted[1].strip(), splitted[2].strip())]
    return triple

def evaluate_predicate(predicate, standard_variables, values):
    var_dict = {}
    index = 0
    for var in standard_variables:
        var_dict[var[0]] = values[index]
        index += 1

    for (key, value) in var_dict.items():
        predicate = predicate.replace(str(key), str(value))

    return eval(predicate)

# Run algorithm
def run(variables, triples):
    list_of_names = ""
    # iterate over variables
    for (name, value_range) in variables:
        # create all variables
        exec("var_list_evaluated_" + name + " = " + value_range)
        list_of_names += ", var_list_evaluated_" + name
    # remove first comma and space
    list_of_names = list_of_names[2:]

    # generate the combinations
    exec("combined = list(itertools.product(" + list_of_names + "))")

    # initialize the matrix of probabilities
    size = len(combined)
    matrix = numpy.zeros((size, size))

    # iterate all elements
    for leave in combined:
        # transform leave tuple in array
        ordered_vars = list(leave)

        # iterate over all predicates
        for (p, q, prob) in triples:
            # check the leave predicate
            if evaluate_predicate(p, variables, ordered_vars):
                # get all arrive states
                for arrive in combined:
                    ordered_arrive_vars = list(arrive)
                    # check the arrive predicate
                    if evaluate_predicate(q, variables, ordered_arrive_vars):
                        # calculate row and column of the matrix
                        row = 0
                        index = 0
                        for o in leave:
                            row += eval("var_list_evaluated_" + variables[index][0]).index(o)
                            index += 1
                        column = 0
                        index = 0
                        for o in arrive:
                            column += eval("var_list_evaluated_" + variables[index][0]).index(o)
                            index += 1
                        matrix[row][column] = eval(prob)

    return matrix

# Begin the parser
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

matrix = run(vars, triples)
print matrix
