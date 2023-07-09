# Import libraries
import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os

# page configurations
st.set_page_config(page_title = 'Date Profiler', layout = 'wide')

# file type validation
def is_file_csv(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    return ext == '.csv'

# get file size
def get_file_size(file):
    size_bytes = sys.getsizeof(file)
    size_MB = size_bytes/(1024*1024)
    return size_MB

# Side bar
with st.sidebar:
    uploaded_file = st.file_uploader('Upload a CSV File')

    if uploaded_file is not None:
        st.write('Modes of Operations')

        # Minimal report or detailed report
        minimal = st.checkbox('Do you need a minimal report?')
        
        # Display mode
        display_mode = st.radio('Display mode:' , options = ('Primary', 'Dark', 'Orange'))
        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False

        

if uploaded_file is not None:

    # Display error messasge if the file is not of the type CSV
    if is_file_csv(uploaded_file):

        file_size = get_file_size(uploaded_file)

        if file_size <= 10:
            # Read the file in dataframe
            df = pd.read_csv(uploaded_file)

            # Display dataframe with first five rows
            # st.dataframe(df.head(5))

            # Generate a report
            with st.spinner('Generating profile report'):
                pr = ProfileReport(df, minimal = minimal, dark_mode=dark_mode, orange_mode=orange_mode)

            # Generate report in streamlit
            st_profile_report(pr)
            
        else:
            st.warning(f'Please upload a file that is under 10 MB. The current file size is {round(file_size, 0)} MB.')

    else:
        st.warning('The file upload should be of the type CSV')

else:
    st.title('Data Profiler')
    st.info('Upload your data in the left side bar to generate profiling report.')