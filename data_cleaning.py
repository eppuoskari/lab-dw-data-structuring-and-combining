import pandas as pd

def clean_column_names(df):
    """
    Cleans column names by:
    - Stripping whitespace
    - Converting to lowercase
    - Replacing spaces with underscores
    - Renaming specific known columns (like 'st' to 'state')
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.rename(columns= {'st': 'state'}, inplace=True)
    return df


def clean_customer_data(df):
    """
    Cleans and standardizes key columns in the customer dataset.
    -Normalizes and standardizes 'gender', 'state', 'education', 'customer_lifetime_value', and 'vehicle_class' columns.
    """

    # Clean 'gender' column
    df['gender'] = df['gender'].str.strip().str.lower()
    df['gender'] = df['gender'].replace({
        'm': 'M', 
        'male': 'M',
        'f': 'F', 
        'female': 'F', 
        'femal': 'F'
    })

    # Clean 'state' column
    df['state'] = df['state'].astype(str).str.strip().str.lower()
    df['state'] = df['state'].replace({
        'az': 'Arizona',
        'cali': 'California',
        'wa': 'Washington'
    })
    df['state'] = df['state'].str.title()

    # Clean 'education' column
    df['education'] = df['education'].replace({
        'Bachelors': 'Bachelor'
    })

    # Clean 'customer_lifetime_value' column
    df['customer_lifetime_value'] = (
        df['customer_lifetime_value']
        .astype(str)
        .str.replace('%', '', regex=False)
        .str.strip()
    )

    # Clean 'vehicle_class' column
    df['vehicle_class'] = df['vehicle_class'].astype(str).str.strip()
    df['vehicle_class'] = df['vehicle_class'].replace({
        'Sports Car': 'Luxury',
        'Luxury SUV': 'Luxury',
        'Luxury Car': 'Luxury'
    })

    return df

def format_data_types(df):
    """
    Clean and convert specific columns to proper data types:
    - 'customer_lifetime_value': convert to float
    - 'number_of_open_complaints': extract middle value from string like '1/5/00' and convert to numeric
    """

    # Convert customer_lifetime_value to float
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')

    # Extract the middle value from 'number_of_open_complaints' and convert to numeric
    df['number_of_open_complaints'] = (
        df['number_of_open_complaints']
        .astype(str)
        .apply(lambda x: x.split('/')[1] if '/' in x else x)
    )
    df['number_of_open_complaints'] = pd.to_numeric(df['number_of_open_complaints'], errors='coerce')

    return df

def format_data_types(df):
    """
    Clean and convert specific columns to proper data types:
    - 'customer_lifetime_value': convert to float
    - 'number_of_open_complaints': extract middle value from string like '1/5/00' and convert to numeric
    """

    # Convert customer_lifetime_value to float
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')

    # Extract the middle value from 'number_of_open_complaints' and convert to numeric
    df['number_of_open_complaints'] = (
        df['number_of_open_complaints']
        .astype(str)
        .apply(lambda x: x.split('/')[1] if '/' in x else x)
    )
    df['number_of_open_complaints'] = pd.to_numeric(df['number_of_open_complaints'], errors='coerce')

    return df

def create_active_df(df):
    """
    Drop rows with missing values in key columns to isolate active customers,
    and convert numeric columns to integers if possible.
    """
    # Define the relevant columns to check for activity
    required_cols = [
        "customer", "customer_lifetime_value", "monthly_premium_auto",
        "number_of_open_complaints", "policy_type", "total_claim_amount"
    ]

    # Drop rows where any of the required fields are missing
    df = df.dropna(subset = required_cols)

    # Try to convert all columns to numeric where possible
    df = df.apply(pd.to_numeric, errors='ignore')

    # Convert numeric columns to int if they have no missing values
    for col in df.select_dtypes(include='number').columns:
        if df[col].isnull().sum() == 0:
            df[col] = df[col].astype(int)

    return df

def remove_duplicates(df):
    """
    Removes duplicate rows from the DataFrame and returns the cleaned DataFrame.
    """
    return df.drop_duplicates()


def clean_all(df):
    df = clean_column_names(df)
    df = clean_customer_data(df)
    df = format_data_types(df)
    df = create_active_df(df)
    df = remove_duplicates(df)
    return df