#!/usr/bin/env python3
"""
"""
import json

DATA_FILE_NAME = 'data_fetching/sadscore_data.json'

def dumps(dict_):
    string = json.dumps(dict_, indent=4, sort_keys=True)
    return string

def print_dict(dict_):
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
        new_questions = {}
        for key, question in responses.items():
            new_questions[key] = question['value']
        return new_questions


def load_data():
    with open(DATA_FILE_NAME) as input_file:
        data = json.load(input_file)
    
    return data

def filter(data):
    filtered = []
    for response in data:
        if 'responses' not in response:
            continue
        qr = QuizResponse(response)
        filtered.append(qr)
    return filtered

def is_numeric(value):
    return not isinstance(value, bool)

def run_statistics(data):
    count = len(data)
    accumulated = {}
    for point in data:
        resp = point.responses
        for question, value in resp.items():
            # Add the question if not already in.
            if question not in accumulated:
                accumulated[question] = 0
            
            # For numeric types, sum the values.
            if is_numeric(value):
                try:
                    accumulated[question] += float(value)
                except ValueError as e:
                    msg = f"Converting '{value}' to 0.'"
                    # print(msg)
                    accumulated[question] += 0
            # For true/false, just count the number of true.
            else:
                if value is True:
                    accumulated[question] += 1
    print_dict(accumulated)
    print(f"Count: {count}")

    return accumulated, count


def main():
    data = load_data()
    
    data = filter(data)

    run_statistics(data)

if __name__ == '__main__':
    main()