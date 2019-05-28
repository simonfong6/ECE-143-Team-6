#!/usr/bin/env python3
"""
Functions that help with loading and filtering the data.
"""
import json
import pandas as pd

DATA_FILE_NAME = 'data_fetching/sadscore_data.json'

def dumps(dict_):
    """
    Converts dictionaries to indented JSON for readability.

    Args:
        dict_ (dict): The dictionary to be JSON encoded.

    Returns:
        str: JSON encoded dictionary.
    """
    string = json.dumps(dict_, indent=4, sort_keys=True)
    return string

def print_dict(dict_):
    """
    Prints a dictionary in readable format.

    Args:
        dict_ (dict): The dictionary to be JSON encoded.
    """
    print(dumps(dict_))

class QuizResponse:
    """
    Wraps each individual response dictionary so that it is easier to access.

    Attributes:
        data (dict): The raw quiz response data.
        timestamp (float): The timestamp of when the data was recorded.
        total_score (int): The total score of this response.
        responses (dict): Just the quiz question and value recorded.
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

        Args:
            responses (dict(dict)): Responses for each question.

        Returns:
            dict(question->value): A dictionary that maps from question to
                response value.

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

    Returns:
        list(dict): The data a dictionary.
    """
    with open(DATA_FILE_NAME) as input_file:
        data = json.load(input_file)
    
    return data

def filter(data):
    """
    Runs through all the data, creates QuizResponse objects, and puts them in a
    list.

    Args:
        data (list(dict)): The nested dictionaries to be converted.
    
    Returns:
        list(QuizResponse): Each response as a QuizResponse object.
    """
    filtered = []
    for response in data:
        # There is one dictionary that just stores the count of responses.
        if 'responses' not in response:
            continue
        qr = QuizResponse(response)
        filtered.append(qr)
    return filtered

def create_dataframe(data):
    """
    Create a DataFrame from our data for easier manipulation.

    Args:
        data (list(dict): The quiz responses.

    Returns:
        pandas.DataFrame: The quiz responses as a DataFrame.
    """
    df = pd.DataFrame(data)
    return df

def load_data_dataframe():
    """
    Loads data as dataframe.

    Returns:
        pandas.DataFrame: The data loaded as dataframe.
    """
    data = load_data()
    data = filter(data)

    # Just use the list of responses for each QuizReponse object.
    responses = []
    for response in data:
        response_dict = response.responses
        response_dict['timestamp'] = response.timestamp
        response_dict['total_score'] = response.total_score

        responses.append(response)
    just_list = [ r.responses for r in data]

    df = create_dataframe(just_list)

    # Columns to convert to numeric types.
    numeric_columns = [
        'foreign_langauges_fluent',
        'foreign_langauges_nonfluent',
        'height_cm',
        'instruments',
        'iq_score',
        'attractiveness'
    ]

    # Fix strings to numeric values.
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column])

    # Convert tattoos column to numeric and fill NaN with 0's.
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

    Args:
        df (pandas.DataFrame): The data to filter.
        column_name (str): The column name to filter on.
        min_val (int): The minimum value allowed in this category.
        max_val (int): The maximum value allowed in this category.

    Returns:
        pandas.DataFrame: The same dataframe, but with outliers removed.
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

    Args:
        df (pandas.DataFrame): The data to filter out outliers from.
    
    Returns:
        pandas.DataFrame: The same data without outliers.
    """

    # Keep heights between 4ft and 8ft.
    df, outliers_height = drop_outliers(df, 'height_cm', 121, 250)

    # Drop Instruments outliers.
    df, outliers_instruments = drop_outliers(df, 'instruments', 0, 20)
    
    # Drop IQ Score outliers.
    df, outliers_iq_score = drop_outliers(df, 'iq_score', 0, 200)

    # Drop fluent languages outliers.
    df, outliers_foreign_langauges_fluent = drop_outliers(
                                            df, 
                                            'foreign_langauges_fluent',
                                            0,
                                            20)
    
    # Drop non-fluent languages outliers.
    df, outliers_foreign_langauges_nonfluent = drop_outliers(
                                                df,
                                                'foreign_langauges_nonfluent',
                                                0,
                                                20)

    # Drop non-fluent languages outliers.
    df, outliers_tattoos = drop_outliers(
                                                df,
                                                'tattoos',
                                                0,
                                                20)

    # Combine outliers
    outliers = pd.concat(
                [
                    outliers_height,
                    outliers_instruments,
                    outliers_iq_score,
                    outliers_foreign_langauges_fluent,
                    outliers_foreign_langauges_nonfluent,
                    outliers_tattoos
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