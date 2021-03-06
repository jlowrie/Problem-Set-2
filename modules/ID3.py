import math
from node import Node
import sys
from collections import Counter

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    
    root = Node()
    homogenous = check_homogenous(data_set)
    if homogenous!= None:
        root.label = homogenous
        return root
        
    if depth == 0  or len(data_set)==0 or len(attribute_metadata)<=1:
        root.label = mode(data_set)
        return root
        
    best_att, best_split = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
    if(numerical_splits_count[best_att]==0):
        root.label = mode(data_set)
        return root
        

    if best_att == False:
        root.label = mode(data_set)
        return root
        
    root.decision_attribute = best_att
    root.splitting_value = best_split
    root.name = attribute_metadata[best_att]['name']
    root.is_nominal = attribute_metadata[best_att]['is_nominal']
    if(root.is_nominal):
        examples = {}
        
        for k, val in split_on_nominal(data_set, best_att).items():
            if is_missing(val, best_att):
                val = replace_missing(val, best_att)
            examples[k] = ID3(val, attribute_metadata, numerical_splits_count, depth-1)
        root.children = examples
    else:
        root.children = []
        examples = [0,0]
        first_split, second_split = split_on_numerical(data_set, best_att, best_split)
        if is_missing(first_split, best_att):
            first_split= replace_missing(first_split, best_att)
        if is_missing(second_split, best_att):
            second_split = replace_missing(second_split, best_att)
        numerical_splits_count[best_att] -= 1
        examples[0] = ID3(first_split, attribute_metadata, numerical_splits_count, depth-1)
        examples[1] = ID3(second_split, attribute_metadata, numerical_splits_count, depth-1)
        root.children.append(examples[0])
        root.children.append(examples[1])
    return root
    
    
def is_missing(data_set, index):
    for i in range(len(data_set)):
        if len(data_set[i])> index:
            if data_set[i][index] == None:
                return True
    return False
    
def replace_missing(data_set, index):
    vals = []
    for i in range(len(data_set)):
        if len(data_set[i])> index:
            if data_set[i][index]!= None:
                vals.append([data_set[i][index]])
    most_common = mode(vals)
    
    for i in range(len(data_set)):
        if len(data_set[i])> index:
            if data_set[i][index] == None:
                data_set[i][index] = most_common
    return data_set

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    check_value = data_set[0][0]
    for element in data_set:
        if (element[0]!= check_value):
            return None
    return check_value
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    max_value = 0
    best_data = 0
    best_numeric_split = 0
    
    for val in range(1,len(data_set[0])):
        if  attribute_metadata[val]['is_nominal']:
            gain_ratio = gain_ratio_nominal(data_set, val)
            if gain_ratio> max_value:
                max_value = gain_ratio
                best_data = val
        else:
            (gain_ratio, split) = gain_ratio_numeric(data_set, val, 1)
            if gain_ratio> max_value:
                max_value = gain_ratio
                best_data = val
                best_numeric_split = split
    if max_value == 0:
        return False, False
    if attribute_metadata[best_data]['is_nominal']:
        return best_data, False
    else:
        return best_data, best_numeric_split
        
        
    

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    element_list = []
    if data_set!=[]:
        for element in data_set:
            element_list.append(element[0])
        counter = Counter(element_list)
        
        value, num = counter.most_common(1)[0]
        return value
    return False
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    count_vals = {}
    entropy = 0
    for val in data_set:
        index = val[0]
        if val[0] in count_vals.keys():
            count_vals[index]= count_vals[index]+1
        else:
            count_vals[index] = 1
    
    for key, val in count_vals.items():

        if val == len(data_set):
            return 0
        weight = (float)(val)/ (float) (len(data_set))
        entropy =entropy+ weight * math.log(weight,2)
    
    return -entropy
        
        

# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    count_vals = {}
    all_values = []
    for val in data_set:
        all_values.append([val[0]])
        if val[attribute] in count_vals.keys():
            count_vals[val[attribute]].append([val[0]])
        else:
            count_vals[val[attribute]] = [[val[0]]]
    
    total = 0
    iv = 0
    for val in count_vals:
        weight = (float)(len(count_vals[val]))/ (len(data_set))
        total += weight * entropy(count_vals[val])
        iv -= weight *math.log(weight, 2)
    if iv == 0:
       return False
    return (entropy(all_values) - total)/iv


# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    
    ent = entropy(data_set)
    threshold_val = 0
    max_gain_ratio = 0
    iv = 0
    val = 0
    while val < len(data_set):
        split = split_on_numerical(data_set, attribute, data_set[val][attribute])
        if(split != None):
            first_ent = entropy(split[0])
            sec_ent = entropy(split[1])
            first_weight = (float)(len(split[0]))/(len(data_set))
            sec_weight = (float)(len(split[1]))/(len(data_set))
            gain_ratio = ent - first_ent*first_weight - sec_ent*sec_weight
            if gain_ratio> max_gain_ratio:
                max_gain_ratio = gain_ratio
                threshold_val = data_set[val][attribute] 
                iv = -first_weight*math.log(first_weight,2) - sec_weight*math.log(sec_weight,2)
        val+= steps
        
    if iv == 0:
        return None, None
    
    return (float)(max_gain_ratio)/iv, threshold_val
        

    
    
# ======== Test case =============================
# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [1,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    result = {}
    for val in data_set:
        if val[attribute] in result.keys():
            result[val[attribute]].append([val[0], val[attribute]])
        else:
            result[val[attribute]] =  [[val[0], val[attribute]]]
    
    return result
    
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
    attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
        
    first_half = []
    
    second_half = []
    
    
    for val in range(len(data_set)):
        if data_set[val][attribute]< splitting_value:
            first_half.append(data_set[val])
        else:
            second_half.append(data_set[val])
        
    
    return (first_half, second_half)

# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])