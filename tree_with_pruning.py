training_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]


max_Depth = 5;


def unique_vals(rows, col):
    return set([row[col] for row in rows])

def class_counts(rows):
    counts = {}
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def is_numeric(value):
    # in both conditions returns true
    return isinstance(value, int) or isinstance(value, float)


# A Question is used to partition a dataset
class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (header[self.column], condition, str(self.value))


def partition(rows, question):
    """Partitions a dataset.
    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """
    true_rows, false_rows = []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows




def gini(rows):
    #Calculate the Gini Impurity for a list of rows.
    counts = class_counts(rows) # Counts the number of each type of example in a dataset
    impurity = 1

    for label in counts:
        prob_of_label = counts[label] / float(len(rows))
        impurity -= prob_of_label**2
    return impurity



def info_gain(left, right, current_uncertainty):
    """Information Gain.
    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left) / len(left) + len(right))
    # whatever probabilty of left is, right is 1- p_left
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def find_best_split(rows):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""

    best_gain = 0 # keep track of best information gain
    best_question = None #  keep train of the feature / value that produced it
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1 # number of columns

    for col in range(n_features): # for each feature
        values = set([row[col] for row in rows]) # unique values in the column

        for val in values: # for each value:
            question = Question(col, val)

            # try splitting the dataset:
            true_rows, false_rows = partition(rows, question)
            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            gain = info_gain(true_rows, false_rows, current_uncertainty)

            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question

class leaf:
    """A Leaf node classifies data.
    This holds a dictionary of class (e.g., "Apple") -> number of times
    it appears in the rows from the training data that reach this leaf.
    """
    def __init__(self, rows):
        self.predictions = class_counts(rows)



class Decision_Node:
    """A Decision Node asks a question.
    This holds a reference to the question, and to the two child nodes.
    """
    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows, depth):
    gain, question = find_best_split(rows)

    # STOP POINT OF RECURSIVE TREE
    if gain == 0 or depth >= max_Depth:
        return Leaf(rows)

    # If we reach here, we have found a useful feature / value to partition on.
    true_rows, false_rows = partition(rows, question)

    # Recursively build the true branch.
    true_branch = build_tree(true_rows, depth+1)

    # Recursively build the false branch.
    false_branch = build_tree(false_rows, depth+1)

    # Return a Question node. This records the best feature / value to ask at this point, as well as the branches to follow dependingo on the answer. (branch with two more nodes to follow it)
    return Decision_Node(question, true_branch, false_branch)

# we use the calissify function to make classification for each row  of dataset via the decision_tree we made
def classify(row, node):
    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions
    # you will repeat this loop until you reach leaf
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def calculate_accuracy(data):
    sum = 0
    for row in training_data:
        if row[-1] == classify(row, data):
            sum += 1
    return float( sum / len(data) )


# treat depth as hyper-parameter for tree pruning:
error_set = []
for i in range(4, 10):
    max_Depth = i
    testSet = []
    data_temp = training_data.copy()
    for i in range(int(len(data_temp)/5)):
        x = data_temp[str(random.choice(len(data_temp)))]
        testSet.append(x)
        data_temp.remove(x)

    my_tree = build_tree(training_data, 1)
    accur = calculate_accuracy(testSet)
    error_set.append([max_Depth, accur])

max_Depth = min(error_set, key = lambda t: t[1])[0]
my_tree = build_tree(training_data, 1)


# Evaluate
testing_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 4, 'Apple'],
    ['Red', 2, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]

for row in testing_data:
    classify(row, my_tree)
