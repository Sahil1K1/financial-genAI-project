import streamlit as st
import tempfile
import os
from pathlib import Path
import pandas as pd
import json

from src.ingestion.load_data2 import load_excel_to_dfs, save_processed
from src.preprocessing.clean_transform import process_sheet
from workflow.pipeline2 import build_combined_df, build_summary_prompt
from src.llm.generate_insights import call_llm

st.markdown('app')

def processing_uploaded_file(uploaded_file):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            st.write(temp_dir)

        # saving uploaded files
            input_path = temp_dir / "input_xyz.xlsx"
            with open(input_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.info('files uploaded successfully and saved')

            # loading files from this temporary memory
            with st.spinner('loading excel files'):
                sheets = load_excel_to_dfs(input_path)
                # st.write(sheets)
                st.success(f"loaded sheets successfully")
            # saving these files to processed directory
            processed_dir = temp_dir / 'processed_new'
            processed_dir.mkdir(exist_ok=True)
            st.write(processed_dir)
            with st.spinner('Processing sheets'):
                save_processed(sheets=sheets, output_dir=processed_dir)
            st.info("sheets are saved")
            # checking all files inside of processed_dir to see if it is correct or not
            # process_files = list(processed_dir.iterdir())
            # for file_path in process_files:
            #     if file_path.is_file():
            #         st.write(f"{file_path.name}")

            all_dfs = {}
            output_dir = temp_dir / "output"
            output_dir.mkdir(exist_ok=True)

            for sheet_name in sheets:
                input_csv = processed_dir / f"{sheet_name.replace(' ','_')}.csv"
                output_csv = output_dir / f"processed_{sheet_name.replace(' ','_')}.csv"
                process_sheet(csv_path=input_csv, out_path=output_csv)
                df = pd.read_csv(output_csv)
                all_dfs[sheet_name] = df
            st.write(all_dfs)
            st.info('dataframe is created successfully')

            # now passing this dataframe to build combined context and then making a prompt
            with st.spinner('building combined context'):
                context = build_combined_df(all_dfs)
                st.info('context combined successfully')
            with st.spinner('building prompt'):
                final_prompt = build_summary_prompt(context)
            
            # generating insights
            with st.spinner('Generating insights'):
                try:
                    llm_response = call_llm(prompt=final_prompt, model='llama3.1:8b')
                    try:
                        analysis = json.loads(llm_response)
                        st.write(analysis)
                    except json.JSONDecodeError:
                        analysis = {'raw_response':llm_response}
                        st.write(analysis)
                    st.success('analysis completed')
                    return analysis, None
                except Exception as e:
                    return None, f"LLM Error: {str(e)}"                

    except Exception as e:
        return None, f"processing error: {str(e)}"

def main():
    uploaded_files = st.file_uploader(label='upload files here', type=['.xlx', 'xlsx'], accept_multiple_files=False)
    if uploaded_files is not None:
        st.write('file is uploaded successfully')
        
        if st.button('Generate insights'):
            output_files = processing_uploaded_file(uploaded_file=uploaded_files)
            st.write('main function run successfully')


if __name__ == '__main__':
    main()