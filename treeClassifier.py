import numpy as np
import pandas as pd
from collections import Counter
import math

'''
Задача классификации людей с сайта Kaggle. Дана обучающая выборка - информация о людях  и ответ - зарабатывают ли они
<50k$ в год, или больше . Задача - классифицировать тестовую выборку. Я сделал это с помощью алгоритма решающего дерева.
Данная задача - стандартная задача машинного обучения
'''

def get_values(data, attribute):
    """
    Returns array of unique attribute values in data

    Input:
        data (we search values in this array of records)
        attribute, which unique values we want to get
    """

    vals = [record[attribute] for record in data]

    return set(vals)

def majority_value(data, attribute):
    """
    Returns the most popular attribute value in data

    Input:
        data (we search values in this array of records)
        attribute, which the most popular value we want to get

    If the most popular value is '?', we return the next value
    """

    vals = [record[attribute] for record in data]
    if len(vals) == 0:
        return '<=50K'
    else:
        if Counter(vals).most_common(1)[0][0] == '?':
            return Counter(vals).most_common(1)[1][0]
        else:
            return Counter(vals).most_common(1)[0][0]

def get_examples(data, best, value):
    """
    Returns records in data, where the value of best attribute is current value

    Input:
        data (we search values in this array of records)
        best is a attrubute, which values we search
        value (we want to get records, where record[best] = value)
    """

    examples = []
    for record in data:
        if record[best] == value:
            examples.append(record)

    return examples

def skip_replacement(data, majority_values):
    """
    Return data with most popular values instead '?'

    Input:
        data (we search values in this array of records)
        majority_values is an array of most popular values of attributes
    """

    for i in range(0, len(data)):
        for attribute in range(0, len(data[0])):
            if data[i][attribute] == '?':
                data[i][attribute] = majority_values[attribute]

    return data

def get_new_cont(data):
    """
    Returns array of new values of continuous attributes (transform into discrete values)

    Input:
        data (we search values in this array of records)
    """

    cont_attr_min_max = {}
    cont_attr_shifts = {}
    new_cont_attr = {}
    cont_attr = [0, 2, 4, 10, 11, 12]
    shifts = [8.0, 400000.0, 4.0, 100.0, 100.0, 12.0]

    for i in range(0, len(cont_attr)):
        cont_attr_shifts[cont_attr[i]] = shifts[i]

    for attribute in cont_attr:
        cont_attr_min_max[attribute] = [100000000.0, 0.0]

    for record in data:
        for attribute in cont_attr:
            if record[attribute] < cont_attr_min_max[attribute][0]:
                cont_attr_min_max[attribute][0] = record[attribute]
            else:
                if record[attribute] > cont_attr_min_max[attribute][1]:
                    cont_attr_min_max[attribute][1] = record[attribute]

    for attribute in cont_attr:
        new_cont_attr[attribute] = []
        min = cont_attr_min_max[attribute][0]
        shift = cont_attr_shifts[attribute]
        max = min + shift

        while max <= cont_attr_min_max[attribute][1]:
            new_str = (min, max)
            new_cont_attr[attribute].append(new_str)
            min += shift
            max += shift

        if max > cont_attr_min_max[attribute][1]:
            new_str = (min, cont_attr_min_max[attribute][1])
            new_cont_attr[attribute].append(new_str)

    return new_cont_attr

def process_input_with_cont(data, new_cont_attr):
    """
    Returns the data with changed values of continuous attributes (transform into discrete values)

    Input:
        data (we search values in this array of records)
        new_cont_attr (array of discrete values of continuous attributes)
    """

    new_data = []
    cont_attr = [0, 2, 4, 10, 11, 12]

    for record in data:
        new_data.append(record)

    for record in new_data:
        new_record = record

        for attribute in cont_attr:
            value = record[attribute]
            new_record[attribute] = -1

            for minmax in new_cont_attr[attribute]:
                if minmax[0] < value <= minmax[1]:
                    new_record[attribute] = minmax

            if new_record[attribute] == -1:
                if value <= new_cont_attr[attribute][0][0]:
                    new_record[attribute] = new_cont_attr[attribute][0]
                else:
                    new_record[attribute] = new_cont_attr[attribute][len(new_cont_attr[attribute]) - 1]

    return new_data

def entropy(data, target_attr):
    """
    Counts the Shannon entropy of subset

    Input:
        data (subset, which entropy we want to count)
        target_attr (this value we want to predict)
    """

    val_freq = {}
    data_entropy = 0.0

    for record in data:
        if val_freq.has_key(record[target_attr]):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]] = 1.0

    for freq in val_freq.values():
        data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2)

    return data_entropy

def gain(data, attr, target_attr):
    """
    Counts Information Gain of attribute

    Input:
        data (we will count gain if attribute in this array of records)
        attr (we want to count information gain of this attribute)
        target_attr (this value we want to predict)
    """

    val_freq = {}
    subset_entropy = 0.0

    for record in data:
        if val_freq.has_key(record[attr]):
            val_freq[record[attr]] += 1.0
        else:
            val_freq[record[attr]] = 1.0

    for val in val_freq.keys():
        val_prob = val_freq[val] / sum(val_freq.values())
        data_subset = [record for record in data if record[attr] == val]
        subset_entropy += val_prob * entropy(data_subset, target_attr)

    return entropy(data, target_attr) - subset_entropy

def choose_attribute(data, attributes, target_attr):
    """
    Returns the best (with highest gain) attribute and its gain

    Input:
        data (we want to find best attribute in this array of records)
        attributes (array of attributes)
        target_attr (this value we want to predict)
    """

    gains = {}
    attributes = attributes[:len(attributes) - 1]

    for attribute in attributes:
        gains[attribute] = gain(data, attribute, target_attr)

    vals = list(gains.values())
    keys = list(gains.keys())
    best = keys[vals.index(max(vals))]
    val = gains[best]

    return (best, val)

def create_decision_tree(data, attributes, target_attr, values):
    """
    Recursive function which returns subtree (root with new branches which are unique values of best attribute)

    Input:
        data (we build subtree according this array of records)
        attributes (array of available attributes)
        target_attr (this value we want to predict)
        values (array of unique values of attributes)

    We escape from recursion in the case of empty data or attributes or in the case of equal values of target attribute
    If gain of attribute is less than 0.05, we escape from recursion and make leaf with most popular target attribute
        value in data
    """

    data = data[:]
    vals = [record[target_attr] for record in data]
    default = majority_value(data, target_attr)

    if not data or (len(attributes) - 1) <= 0:
        return default

    if vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        best, gain = choose_attribute(data, attributes, target_attr)
        if gain <= 0.05:
            return default

        tree = {best:{}}
        for val in values[best]:
            subtree = create_decision_tree(get_examples(data, best, val),
                                           [attr for attr in attributes if attr != best],
                                           target_attr, values)
            tree[best][val] = subtree

    return tree

def predict(record, tree, majority_values):
    """
    The process of descending a tree and this returns prediction of current record

    Input:
        record (we want to predict target attribute value of this record)
        tree (decision tree)
        majority_values is an array of most popular values of attributes

    We escape from recursion in the case of string (answer)
    """

    if isinstance(tree, basestring):
        return tree
    else:
        for key in tree.keys():
            values = tree.get(key)
            cur_val = record[key]

            if cur_val == '?':
                cur_val = majority_values[key]

            for value in values:
                if cur_val == value:
                    return predict(record, tree[key][value], majority_values)

def make_prediction(test, tree, majority_values):
    """
    Returns the array of predictions

    Input:
        test (we want to predict target attribute values of this array of records)
        tree (decision tree)
        majority_values is an array of most popular values of attributes
    """

    prediction = []

    for i in range(0, len(test)):
        pred = predict(test[i], tree, majority_values)
        prediction.append(pred)

    return prediction

def make_submission(prediction, filename_or_buffer, id_col='Id', prediction_col='Solution'):
    """
    Transforms array of predictions into corresponding form and save it

    Input:
        prediction (array of predictions)
        filename_or_buffer (name of .csv file)
        id_col, prediction_col are names of columns
    """

    df = pd.DataFrame({id_col : range(1, len(prediction) + 1), prediction_col : prediction})
    df.to_csv(filename_or_buffer, cols=[id_col, prediction_col], index=False)


#Read the data
train = pd.read_csv('train.csv')
data = pd.read_csv('test.csv', header=None)
train = np.asarray(train)
data = np.asarray(data)

#Process continuous attributes of data into discrete form
new_cont_attr = get_new_cont(train)
train = process_input_with_cont(train, new_cont_attr)
data = process_input_with_cont(data, new_cont_attr)

majority_values = []
values = []

#Create array of majority values
for attribute in range(0, len(train[0]) - 1):
    majority_values.append(majority_value(train, attribute))

#Replace '?' in train
train = skip_replacement(train, majority_values)

#Get array of unique values of attributes
for attribute in range(0, len(train[0])):
    values.append(get_values(train, attribute))

#Create decision tree
tree = create_decision_tree(train, range(0, len(train[0])), len(train[0]) - 1, values)

#Make and save prediction
submission = make_prediction(data, tree, majority_values)
make_submission(submission, '5.csv')
