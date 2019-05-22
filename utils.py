#!/usr/bin/env python3
"""
"""
import json
import pandas as pd

DATA_FILE_NAME = 'data_fetching/sadscore_data.json'

def dumps(dict_):
    """
    Helps print dictionaries as indented JSON for readability.
    """
    string = json.dumps(dict_, indent=4, sort_keys=True)
    return string

def print_dict(dict_):
    """
    Prints a dictionary in readable format.
    """
    print(dumps(dict_))

class QuizResponse:
    """
    Wraps each individual response dictionary so that it is easier to access.
    """

    def __init__(self, resp_data):
        self.data = resp_data
        self.timestamp = resp_data['timestamp_secs']
        self.total_score = resp_data['total_score']
        self.responses = QuizResponse.filter_questions(resp_data['responses'])

    def __repr__(self):
        return 'QuizResponse(\n' + dumps(self.responses) + '\n)'

    @staticmethod
    def filter_questions(responses):
        """
        Extract only the value of each response disregarding other details.

        Example:
        data = {
                "above_platinum": {
                    "name": "above_platinum",
                    "score": 0,
                    "value": false
                }
        }
        -> {
            "above_platinum": false
        }
        """
        new_questions = {}
        for key, question in responses.items():
            new_questions[key] = question['value']
        return new_questions


def load_data():
    """
    Loads the JSON data as a dictionary.
    """
    with open(DATA_FILE_NAME) as input_file:
        data = json.load(input_file)
    
    return data

def filter(data):
    """
    Runs through all the data, creates QuizResponse objects, and puts them in a
    list.
    """
    filtered = []
    for response in data:
        if 'responses' not in response:
            continue
        qr = QuizResponse(response)
        filtered.append(qr)
    return filtered

def is_numeric(value):
    """
    Checks if a given value is numeric. Usefull for diffrentiating true or
    false questions vs ones that require a free response number.
    """
    return not isinstance(value, bool)

def create_dataframe(data):
    df = pd.DataFrame(data)
    return df

def load_data_dataframe():
    """
    Loads data as dataframe.
    """
    data = load_data()
    data = filter(data)
    just_list = [ r.responses for r in data]
    df = create_dataframe(just_list)

    numeric_columns = [
        'foreign_langauges_fluent',
        'foreign_langauges_nonfluent',
        'height_cm',
        'instruments',
        'iq_score'
    ]

    # Fix strings to numeric values.
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column])

            
    column = 'tattoos'
    df[column] = pd.to_numeric(df[column])
    df[column].fillna(0)


    return df

def turn_off_scientific_notation():
    """
    Turns off scienctific notation in Pandas when displaying dataframes.
    """
    pd.set_option('display.float_format', lambda x: '%.3f' % x)

def drop_height_outliers(df):
    """
    Attempts to remove very large height outliers from data.
    """
    max_height = 250    # 8 ft
    min_height = 121    # 4 ft
    df = df[df['height_cm'] <= max_height]
    df = df[df['height_cm'] >= min_height]
    return df

def main():
    df = load_data_dataframe()
    turn_off_scientific_notation()
    df = drop_height_outliers(df)
    print(df)
    sums = df.sum()
    count = df.shape[0]
    averages = sums / count
    print(averages)

if __name__ == '__main__':
    main()