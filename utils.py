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

def drop_outliers(df, column_name, min_val, max_val):
    """
    Drops outliers based on range, inclusive.
    """

    # Find the outliers.
    max_outliers = df[df[column_name] > max_val]
    min_outliers = df[df[column_name] < min_val]
    outliers = pd.concat([max_outliers,min_outliers])
    
    # Drop the outliers.
    df = df[df[column_name] <= max_val]
    df = df[df[column_name] >= min_val]

    return df, outliers

def drop_all_outliers(df):
    """
    Drops all outliers.
    """

    # Keep heights between 4ft and 8ft.
    df, outliers_height = drop_outliers(df, 'height_cm', 121, 250)

    # Drop Instruments outliers.
    df, outliers_instruments = drop_outliers(df, 'instruments', 0, 20)
    
    # Drop IQ Score outliers.
    df, outliers_iq_score = drop_outliers(df, 'iq_score', 0, 200)

    # Combine outliers
    outliers = pd.concat(
                [
                    outliers_height,
                    outliers_instruments,
                    outliers_iq_score
                ])

    return df, outliers

def main():
    df = load_data_dataframe()
    turn_off_scientific_notation()
    df, outliers = drop_all_outliers(df)
    sums = df.sum()
    count = df.shape[0]
    averages = sums / count

if __name__ == '__main__':
    main()