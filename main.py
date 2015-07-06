import re
import itertools
import numpy
import math
from fractions import Fraction

# DEBUG INPUT
input = """
// Declaracao de variavel
var i:[1,2,3,4,5] // estados

i==1 or i==5,(i==1 or i==5) and i==~i, 1/2
i==1,i==2, 1/2
i==5,i==4, 1/2
i>=2 and i<=4,i==~i+1, 1/2
i>=2 and i<=4,i==~i-1, 0.5
"""

# Remove comments
def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

# Parse Body
def parse_body(line):
    triple = []
    # include triple expression in array
    splitted = line.split(',')
    # parser the fraction
    prob = str(float(Fraction(splitted[2].strip())))

    triple = [(splitted[0].strip(), splitted[1].strip(), prob)]
    return triple

def evaluate_predicate(predicate, standard_variables, values, leave_values = None):
    var_dict = {}
    var_dict_leave = {}
    index = 0
    for var in standard_variables:
        if leave_values != None:
            var_dict_leave["~"+var[0]] = leave_values[index]
        var_dict[var[0]] = values[index]
        index += 1

    for (key, value) in var_dict_leave.items():
        predicate = predicate.replace(str(key), str(value))

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
                    if evaluate_predicate(q, variables, ordered_arrive_vars, ordered_vars):
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
initialized = False
has_begin_body = False
done = False

line_number = 0
for line in input_lines:
    line_number+= 1

    # remove comments
    line = remove_comments(line)

    #  variable definition
    if line[:3] == "var":
        initialized = True
        # remove "var"
        line = re.sub(r"var\s*", "", line)
        # remove everything else var name
        var_name = re.sub(r"\h*:\s*.*", "", line).strip()
        # remove var name
        var_range = re.sub(r"\w+\s*:\s*", "", line).strip()
        # include tuple in array
        vars.append((var_name, var_range))
        continue

    if line == "" and initialized and not has_begin_body and not done:
        has_begin_body = True
        continue

    if line == "" and initialized and has_begin_body and not done:
        done = True
        continue

    if line == "" and done:
        print "Erro de sintaxe na linha: " + str(line_number)
        break

    if has_begin_body:
        triples += parse_body(line)
        continue

# Run the algorithm
matrix = run(vars, triples)

# check warnings
# check if not stochastic matrix
sums = map(sum, matrix)
warns = map(lambda (i,x): "Matrix nao estocastica: linha " + str(i) if x > 1 or x < 1 else None, list(enumerate(sums)))
warns = filter(None, warns)
if len(warns) > 0: print '\nWarnings:'
if len(warns) > 0: print '\n'.join(warns)

print "\nResultado:"
# Print in octave stardard
print '\n'.join(' '.join(str(cell) for cell in row) for row in matrix)
