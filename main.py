import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
import analytics

analytics.write_key = '6I7ptc5wcIGC4WZ0N1t0NXvvAbjRGUgX'

st.set_page_config(layout='wide')

# Define custom CSS style for the form
custom_css = """
<style>
    .email-form {
        background-color: #F0F0F0; /* Set background color */
        padding: 20px; /* Add padding */
        border-radius: 10px; /* Add rounded corners */
        font-family: Arial, sans-serif; /* Set font family */
        line-height: 1.6; /* Set line height */
    }
    .email-form h2 {
        color: #1E90FF; /* Set title color */
        text-align: center; /* Center-align title */
    }
    .email-form label {
        font-weight: bold; /* Bold labels */
    }
    .email-form input[type="text"] {
        width: 100%; /* Full width for input field */
        padding: 10px; /* Add padding to input field */
        margin-bottom: 15px; /* Add spacing between input fields */
        border: 1px solid #ccc; /* Add border */
        border-radius: 5px; /* Add rounded corners to input field */
    }
    .email-form button {
        display: block; /* Make button a block element for full width */
        width: 100%; /* Full width button */
        padding: 10px; /* Add padding to button */
        background-color: #1E90FF; /* Button background color */
        color: #fff; /* Button text color */
        border: none; /* Remove border */
        border-radius: 5px; /* Add rounded corners to button */
        cursor: pointer; /* Change cursor on hover */
    }
</style>
"""

# Apply the custom CSS using st.markdown()
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown(
    "<h1 style='color: #FF5733; text-align: center; "
    "font-family: Arial, sans-serif; background-color: #F0F0F0; "
    "padding: 10px; border-radius: 10px;'>Data Cleaning Verification</h1>",
    unsafe_allow_html=True
)

st.markdown("""
<div class="markdown-content">
<h1>This app only allows you to download data after it passes a series of data quality checks.</h1>
<p>After importing data, the app will run a series of checks against your data and prompt you with a set of data cleaning steps.</p>

<p>To use the app, follow the mitosheet below:</p>
<ol>
    <li>Click <strong>Import</strong> &gt; <strong>Import Files</strong> and select an XLSX file from the <code>data</code> folder.</li>
    <li>Click the <strong>Import Button</strong>, and configure the import to skip rows depending on the file you choose.</li>
    <li>Use the Mitosheet to clean the data according to the prompts.</li>
    <li>Once all of the checks pass, download the csv file.</li>
</ol>
</div>
""", unsafe_allow_html=True)

CHECKS_AND_ERRORS = [
    # First column is issue date
    (
        lambda df: df.columns[0] != 'issue date',
        'Please edit the first column name to "issue date".',
        'You can do this by double clicking on the column name.'
    ),
    # Correct dtype
    (
        lambda df: df["issue date"].dtype != "datetime64[ns]",
        'Please change the dtype of the "issue date" column to datetime.',
        'You can do this by clicking on the Filter icon, and then selecting "datetime" from the "dtype" dropdown.'
        ),
    # Delete the Notes column
    (
        lambda df: "Notes" in df.columns,
        'Please delete the "Notes" column, which is the final column of the dataframe.',
        'You can do this by selecting the column header and pressing the Delete key.'
    ),
    # Turn the term column into a number with the formula = VALUE(LEFT(term, 3))
    (
        lambda df: df["term"].dtype != "int64",
        'Please extract the number of months from the "term" column.',
        'To do so, double click on a cell in the column, and write the formula `=INT(LEFT(term, 3))`.'
    ),
]

def run_data_checks_and_display_prompts(df):
    '''
    Runs the data checks and displays prompts for the user to fix the data.
    '''
    for check, error_message, help in CHECKS_AND_ERRORS:
        if check(df):
            st.error(error_message + " "+help)
            return False
    return True

# If the user has not submitted the form yet and an analytics key is set, display the email form
with st.form("email_form"):
    st.write("To be the first to learn about new features, coming changes, and advanced functionality, signup for the Mito for Streamlit email list.")
    email = st.text_input("EMAIL")
    submitted = st.form_submit_button("Sign Up")
    
    if submitted:
        # Send email to segment
        analytics.identify(email, {'location':'streamlit_data_cleaning_verification_demo'})
        
        # Store that the form has been submitted so we don't display it again
        st.success(f"Thanks for signing up {email} ! We'll keep you updated on new features.")
        
@st.cache_data
def convert_df(df):
    return df.to_csv(index = False).encode('utf-8')

# Display the data inside of the spreadsheet so the user can easily fix the data quality issues.
dfs, _ = spreadsheet(import_folder='./data')

# If the user has not yet imported data, prompt them to do so.
if len(dfs)==0:
    st.info("Please import a file to begin. Click **Import** > **Import Files** and select a file from the 'data' folder.")
    
    # Don't run the rest of the app if the user hasn't imported tha data.
    st.stop()
    
# Run the checks on the data and display prompts
df = list(dfs.values())[0]
checks_passed = run_data_checks_and_display_prompts(df)

# If the data passes all checks, allow the user to download the data
if checks_passed:
    st.success("All the checks passed! This data is clean, and ready to be download.")
    
    csv = convert_df(df) 
    
    st.download_button(
        "Press to Download",
        csv,
        "mito_verified_data.csv",
        "text/csv",
        key='download-csv'
    )