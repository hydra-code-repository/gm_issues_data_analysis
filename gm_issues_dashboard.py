import pandas as pd
import streamlit as st
import re
import os
import sys
from collections import Counter


# Function to obtain the correct path from the data
def get_data_path(filename):
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, 'data', filename)


# Read the csv file
df = pd.read_csv(get_data_path('df_most_ten_frequent_prescreened_gm_year_model.csv'))

def create_sidebar_selectbox(df):
    # Count the 10 most frequent prescreened year/make/mode/hardware_part_number
    most_ten_frequent_prescreened_gm_brands = df['vehicle_info_joined_hdw'].value_counts().head(10)

    # Create a df from the Series most_ten_frequent_prescreened_gm_brands to show the information organized
    df_most_ten_frequent_prescreened_gm_brands = pd.DataFrame({'Year/Make/Model/HDW_PN#': most_ten_frequent_prescreened_gm_brands.index, 'Quantity': most_ten_frequent_prescreened_gm_brands.values})

    # Create a list with top 10 frequent year/make/mode/hardware_part_number prescreened
    list_most_ten_frequent_prescreened_gm_brands = list(df_most_ten_frequent_prescreened_gm_brands['Year/Make/Model/HDW_PN#'])

    # Return the a sidebar selectbox with the year/make/mode/hardware_part_number
    return st.sidebar.selectbox("Select the Option", list_most_ten_frequent_prescreened_gm_brands)

def create_failures_pairs(df):
    # Join all strings from column 'fs1_ecu_problems' in a big single string.
    # astype() - make sure the data is string
    # .str.lower() - convert all caps letters to lower 
    text = ' '.join(df['fs1_ecu_problems'].dropna().str.lower().str.replace(r'[^\w\s]', '', regex=True))

    # Convert the big string into a single list and each word of the string will become the items of the list.
    # 'ecm no start' - ['ecm', 'no', 'start']
    #            items    0      1      2
    fs1_ecu_problems_string = text.split()

    # Create a list with pair words to identify possible common failures through column fs1_ecu_problems
    pair_list = []

    # Loop to iterate over the big list of strings fs1_ecu_problems_string
    # range() - access the position of the big list only over int objects. len() converts the list to int object.
    # len((words)-1) - shows the total of items in the list = len(['ecm', 'no', 'start']) = total positions 3. 
    # Possible pairs [0]+[1], [1]+[2] = 2 pairs with total of words = 3. Therefore = range(len(words)-1) = range(3)'''
    for str in range(len(fs1_ecu_problems_string)-1):
        # words[str] = positions (0, 1, 2) + words[str+1] = ecm no (+1 to join the next word in the list)
        #                 ecm            +      no      = ecm no'''   
        pair = f"{fs1_ecu_problems_string[str]} {fs1_ecu_problems_string[str+1]}"
        pair_list.append(pair)

    # When it comes to GM brands, immobilizer/starting issues are most likely expected problems and they are in this list. 
    symptoms_list = ['no start', 'no crank', 'not starting', 'not start', 'not cranking', 'immobilizer security,no', 'immobilizer security', 'immobilizer security,']
    
    # Count the pairs using the dependency collections
    pair_counter = Counter(pair_list)
    # Confirm the lenght of the pair_count counter to enter  
    pair_count_length = len(pair_counter)

    results_dict = {}
    for pair, count in pair_counter.most_common(pair_count_length):
        if pair in symptoms_list:
            results_dict[pair] = count
    
    return pd.DataFrame({'Failure': results_dict.keys(), 'Quantity': results_dict.values()})

# Function to show the percentage of immobilizer/starting issues accurence
def percentage_of_ecus_affected_immo_starting(df):
    # Most common known immobilizer/starting issues
    known_symptoms_list = ['no start', 'no crank', 'not starting', 'not start', 'not cranking', 'immobilizer security']

    # Function to check if a string contain the one of the symptoms in the 
    def immo_starting_issue_count(text):
        # Condition to check if the text is a NAN (Not a Number) string
        # NAN = empty rows (technically a float)   
        if pd.isna(text):
            return False
        # Convert any upper letter to lower
        text_lowered = text.lower()
        # any returns a bool value if the string/text contains at least one of the symptoms_list, avoiding overcounting if the text has more than 1 symptoms_list
        # symptoms_list = ['no start', 'no crank'] 
        # text_lowered = 'no crank no start condition'
        # text = 'no start'
        # any returns only 1 true     
        return any(text in text_lowered for text in known_symptoms_list)
    
    # Apply the function to the column where the symptoms were described and sum the tru values
    immo_starting_issues_sum = df['fs1_ecu_problems'].apply(immo_starting_issue_count).sum()
    
    # Count the number of precreen cases 
    prescreen_cases_count = len(df)

    # Percentage of immobilizer/starting issues occurred.
    percentage = f'{round((immo_starting_issues_sum * 100) / prescreen_cases_count)}%'

    return percentage, immo_starting_issues_sum

# Function to create df a with the model given
def filter_year_make_model_hdw_pn(df, year_make_model_hdw_selected):
    return df[df['vehicle_info_joined_hdw'] == year_make_model_hdw_selected]


def dtc_frequency(df):
    # Pattern to get the DTC numbers.
    dtcs_number_pattern = r'[PBCUpbcu]\d{3}[0-9A-Za-z]'
    # List to store the dtcs obtained
    dtcs_list = []

    # Loop to iterate under column 'fs1_dtcs" to get the dtcs
    for data in df['fs1_dtcs']:
        # Confirm if the data found in the row is string
        if isinstance(data, str):
            # Regex to get the dtcs based on the pattern and store in a var
            # Use upper() method to convert the dtcs with lower cases (p0300) to upper case (P0300). 
            dtcs_found = re.findall(dtcs_number_pattern, data.upper(), re.IGNORECASE)
            # .extend() method used to update the list when using re library
            # same as .append() method
            dtcs_list.extend(dtcs_found)

    # Count the dtcs and convert to dict having key: value (dtc: 1). 
    dict_dtcs = dict(Counter(dtcs_list))

    # Convert to df to add a column with the dtcs descriptions
    df_dtcs = pd.DataFrame({'DTC': dict_dtcs.keys(), 'Quantity': dict_dtcs.values()})

    # Return a df 
    return df_dtcs.sort_values(by='Quantity', ascending=False)


def dtc_frequency_percentage(df, total_cases):
    # Create a new column to show the % of dtc frequency
    df['% DTC Frequency'] = pd.NA

    # Iterate under the df with the dtcs, get to get the index and update the new column with the percentage
    for index in df.index:
        df.loc[index, '% DTC Frequency'] = f'{round((df.loc[index, 'Quantity'] * 100) / total_cases)}%'
    return df


# Function to get the quantity of ECUs affected with immobilizer/starting problems
def quantity_of_immo_starting_failures(df_failures_pair):
    return sum(df_failures_pair['Quantity'])

# Function to count the prescreen cases
def count_prescreen_cases(df):
    return len(df)

# Call the function to create the sidebar based on the df
option_selected = create_sidebar_selectbox(df)

# Call the function to filter the df based on the year/make/mode/hardware_part_number selected
df_filtered = filter_year_make_model_hdw_pn(df, option_selected)

# Call the function to create the immo/starting issue pairs (eg: no start, no crank) based on the df selected 
df_failures_pair = create_failures_pairs(df_filtered)

# Call the function to count the prescreen cases based on the year/make/mode/hardware_part_number selected
prescreen_cases = count_prescreen_cases(df_filtered)

# Function to obtain the percentahe of affected ecus with the immo/starting failures.
percentage_of_ecus_affected, immo_starting_issues_count = percentage_of_ecus_affected_immo_starting(df_filtered)

# Function to get the trouble codes frequency on the hardware 
df_trouble_codes_analysis = dtc_frequency(df_filtered)

# Fuction to obtain the percentage of trouble code frequency stored by a given hardware 
df_trouble_codes_analysis_percentage = dtc_frequency_percentage(df_trouble_codes_analysis, prescreen_cases)

#-------------------------------------------- STREAMLIT set up ------------------------------------------------------#

st.info("""
💡 Key Findings
1. The analysis revealed significant **data standardization issues** across three critical diagnostic fields:
- **`fs1_ecu_problems`**: Problem descriptions exhibit inconsistent terminology and varying levels of detail
- **`fs1_dtcs`**: Diagnostic Trouble Codes reported with inconsistent formatting and completeness
- **`resolution`**: Solution descriptions lack standardization across different technicians
2. The **Hybrid Analysis Methodology** with **Word Pairs Analysis**, successfully identified well known immobilizer/starting failure patterns.
""")

# DASHBOARD 1st SECTION: Immobilizer/Starting Failures

# Show the dashboard header 
st.subheader("Immobilizer/Starting Failures")

# Set up the columns above the graph including the title and the results in numbers
columns1, columns2, columns3 = st.columns([1, 2, 3])
columns1.metric(label="Prescreen Cases", value=prescreen_cases, delta=None)
columns2.metric(label="ECUs Affected", value=immo_starting_issues_count, delta=None)
columns3.metric(label="% Immo/Starting ECUs Affected", value=percentage_of_ecus_affected, delta=None)

# Bar chart to show the most common immo/starting failure pairs (eg: no start, no crank, immobilizer security)
st.bar_chart(df_failures_pair, y='Quantity', x='Failure', horizontal=True, stack=False, color="#0011ffef")

# DASHBOARD 2nd SECTION: DTC Frequency
st.info("""
**💡 DTC Analysis Note:** One ECU can generate multiple fault codes simultaneously. 
Total DTC frequency may exceed prescreen cases, revealing the most common fault patterns.
""")
st.subheader("DTCs Frequency")
st.metric(label="Prescreen Cases", value=prescreen_cases, delta=None)
st.table(df_trouble_codes_analysis_percentage.reset_index(drop=True))


# streamlit run "C:\Language_Projects\Language_Projects\Python\Flagship_1\gm_issues_dashboard_app\gm_issues_dashboard.py"


