# Data Cleanliness Verification

This Streamlit App allows you to import data, and clean it using the mitosheet library. The app is preconfigured with a set of data checks and prompts you to fix up specific issues in the data.

This tool guarantees that your dataset adheres to the specified criteria:

1. The initial column corresponds to the issue date and is formatted as datetime.
2. The issue date column is accurately configured as a datetime data type.
3. The issue date column is devoid of any null values.
4. The Notes column is omitted from the dataframe entirely.
5. The term column is represented as an integer.


### Why is this app useful?
This application serves as the initial phase in a data engineering workflow. As a data engineer, you can aid data analysts in verifying that their data aligns with a defined schema before progressing with their analysis.

Within this application, data can be exported to a CSV file only after all identified data discrepancies have been rectified. There is potential to enhance this application for data export into a database, providing a more expansive range of functionalities.

### Mito Streamlit Package 
Learn more about the Mito Streamlit package [here](https://docs.trymito.io/mito-for-streamlit/getting-started) or following the [getting started guide](https://docs.trymito.io/mito-for-streamlit/create-an-app).

### Run Locally 
1. Create a virtual environment:
```
conda create -p 'virtual environment name' python==3.9
```

2. Start the virtual environment:
```
conda activate 'your virtual environment name'
```

3. Install the required python packages:
```
pip install -r requirements.txt
```

4. Start the streamlit app
```
streamlit run main.py
```