import pandas as pd
import os

MODULES = ['AAA', 'BBB', 'CCC']

def load_plain_tables(raw_path='data/raw/'):
    """Load smaller OULAD CSV tables"""
    print("Loading plain tables...")
    
    if not os.path.exists(raw_path):
        print(f"Warning: Path {raw_path} does not exist.")

    courses = pd.read_csv(f'{raw_path}courses.csv')
    assessments = pd.read_csv(f'{raw_path}assessments.csv')
    vle = pd.read_csv(f'{raw_path}vle.csv')
    student_info = pd.read_csv(f'{raw_path}studentInfo.csv')
    student_reg = pd.read_csv(f'{raw_path}studentRegistration.csv')
    student_assess = pd.read_csv(f'{raw_path}studentAssessment.csv')
    
    return courses, assessments, vle, student_info, student_reg, student_assess

def load_student_vle_chunked(raw_path='data/raw/', chunk_size=1000000):
    """Load the large studentVle.csv in chunks"""
    print(f"Loading studentVle in chunks of {chunk_size}...")
    chunks = pd.read_csv(f'{raw_path}studentVle.csv', chunksize=chunk_size)
    for chunk in chunks:
        yield chunk

def merge_base_tables(student_info, student_reg, courses):

    print("Merging studentInfo, studentRegistration, and courses...")

    merged = pd.merge(student_info, student_reg, 
                      on=['id_student', 'code_module', 'code_presentation'], 
                      how='left')
    
    merged = pd.merge(merged, courses, 
                      on=['code_module', 'code_presentation'], 
                      how='left')
    
    print(f"Merged base table shape: {merged.shape}")
    return merged

if __name__ == "__main__":
    print("Testing data loaders...")
    
    try:
        courses, assessments, vle, student_info, student_reg, student_assess = load_plain_tables()
        print(f"Success! Loaded studentInfo: {student_info.shape}")

        base_data = merge_base_tables(student_info, student_reg, courses)
        
    except FileNotFoundError:
        print("Error: Could not find the CSV files.")

    try:
        for chunk in load_student_vle_chunked():
            print(f"Success! First chunk of studentVle loaded. Shape: {chunk.shape}")
            break
    except FileNotFoundError:
         print("Error: Could not find studentVle.csv.")