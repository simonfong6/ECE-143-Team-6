import json
from pandas.io.json import json_normalize
import pandas as pd
from pandas import ExcelWriter
import xlsxwriter
import collections
import numpy as np
import copy
def main():
    '''
        Loading data and taking averages,median, and percentages
    '''
    
    json_file = 'sadscore_data.json'
    write_to_excel = False

    # Make data from json file into Data frame
    df = pd.read_json(json_file, orient='columns')
   
    # pd.Series of responses
    responses_data = df['responses']
    
    # Drop NaN responses
    responses_data = responses_data.dropna()

    # Get all id's
    id_numbers = df['_id']
    
    # Drop first index since its not valid data
    id_numbers = id_numbers.drop(0)
    
    # Convert id's to list
    id_numbers = id_numbers.values.tolist()
   
    # Create a list of dictionaries for all responses
    response_list = responses_data.values.tolist()
    
    # Evaluate first response
    first_response = response_list.pop()
    
    # List of str's of each category
    categories = list(first_response.keys())
    
    # Empty data frame
    response_score = pd.DataFrame(index = id_numbers, columns=categories)

    # Collect data from first response
    for key, val in first_response.items():
        response_score.loc[id_numbers[0],key] = val['score']
    
    # Erase first response since already recorded
    id_numbers.pop(0)
    
    # Deep copy
    response_list_temp = copy.deepcopy(response_list)
    
    # Go thru the every id response
    for elem in response_list_temp:
        _dict = response_list.pop(0)
        id_ = id_numbers.pop()
        
        # Store the score for every category with respective id
        for category, val in _dict.items():
            
            # Store score in data frame
            response_score.loc[id_, category] = val['score']

    
    # Write an excel sheet of Data Frame
    if write_to_excel == True: 
        write_excel_sheet(df)

    

    
def write_excel_sheet(df):

    # Write an excel file to see data
    writer = ExcelWriter('PythonExport.xlsx',engine='xlsxwriter')
    
    # Create sheet for data frame
    df.to_excel(writer,sheet_name='Sheet1')
    
    # Save sheet
    writer.save()

    
    


main()