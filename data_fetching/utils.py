#!/usr/bin/env python3
"""
"""
import json

DATA_FILE_NAME = 'sadscore_data.json'


def load_data():
    with open(DATA_FILE_NAME) as input_file:
        data = json.load(input_file)
    
    return data

def main():
    data = load_data()
    print(data[1])

if __name__ == '__main__':
    main()