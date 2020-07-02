import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """
    Loads in two file, merges them and return dataframe
    
    Parameters:
        messsage_filepath: filepath for first csv_file
        categories_filepath: filepath for second csv_file
        
     Returns:
        dataframe including both files merged
     """
    
    # load messages dataset
    messages = pd.read_csv(messages_filepath)
    
    # load categories dataset
    categories = pd.read_csv(categories_filepath)
    
    # merge datasets
    df = pd.merge(messages, categories, on = 'id')
    
    return df

def clean_data(df):
    """ Cleans dataframe of duplicates and sets better categories 
    
    Args:
        dataframe: DataFrame to clean
    """
    
    # DataFrame for the 36 individual category columns
    categories = df["categories"].str.split(";", expand = True)
    
    # select the first row of the categories dataframe
    row = categories.iloc[0]
    
    # Use this row to extract list of new column names
    category_colnames = [x[:-2] for x in row]
    
    # Rename the column of 'categories'
    categories.columns = category_colnames
    
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].astype(str).str.split('-').str[1]
    
        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
        
    # drop the original categories column from `df`
    df.drop(['categories'], axis = 1, inplace=True)
        
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis = 1)

    # drop duplicates
    df = df.drop_duplicates()
    
    return df
  
def save_data(df, database_filename):
    """ 
    Saves the dataframe to a database
    
    Parameters
        df: Dataframe to be saved
        database_filename: Where to save the database
        
    """
    
    engine = create_engine('sqlite:///DisasterResponse.db')
    df.to_sql('Categories', engine, index=False)

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()