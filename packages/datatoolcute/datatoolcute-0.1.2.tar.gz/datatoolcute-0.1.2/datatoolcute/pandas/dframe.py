import pandas as pd
import Levenshtein

def set_header(
    data: pd.DataFrame,
    header_columns: list[str | int]
):
    
    # check whether the header is already set
    if set(header_columns) == set(data.columns):
        return data

    # find where the header columns is first found as a row on the datafrane
    header_index = data[data.isin(header_columns).sum(axis=1) == len(header_columns)].index[0]
    # set this row as the header
    data.columns = data.loc[header_index]
    # drop the rows before the header and then reset index
    return data.loc[header_index + 1:].reset_index(drop=True)

def levenshtein_on_list(words_list: list[str], template: str, cutoff: float = 0.7):
    return sorted(list(words_list), key=lambda column: Levenshtein.ratio(column, template, score_cutoff=cutoff))

def reduce_synonyms(
    data: pd.DataFrame,
    base_column: str,
    synonyms: list[str],
    cutoff: float = 0.7
) -> pd.DataFrame:
    
    # Check if the base column already exists in the DataFrame
    s1, s2 = set(base_column), set(data.columns)
    if s1.issubset(s2) or s2.issubset(s1):
        return data

    # Find the closest match from the synonyms list to the columns in the DataFrame
    close_match = levenshtein_on_list(data.columns, base_column)[-1]
    
    # If a close match is found, rename the closest column to the base_column
    if close_match:
        data = data.rename(columns={close_match[0]: base_column})
    else:
        # If no exact or close match is found in the column names, search through synonyms
        for synonym in synonyms:
            close_match = levenshtein_on_list(data.columns, synonym)[-1]
            if close_match:
                data = data.rename(columns={close_match[0]: base_column})
                break

    return data

def drop_all_columns_with_repeated_names(df: pd.DataFrame) -> pd.DataFrame:
    
    # Get a count of all column names
    column_counts = df.columns.value_counts()
    
    # Identify columns that appear more than once
    duplicate_columns = column_counts[column_counts > 1].index
    
    # Drop all columns that are duplicates
    df = df.drop(columns=duplicate_columns)
    
    return df

if __name__ == '__main__':
    pass