import pandas as pd
import os

def load_plain_tables(raw_path='anonymiseddata/'):
    """Load smaller OULAD CSV tables"""
    print("Loading plain tables...")
    
    if not os.path.exists(raw_path):
        print(f"Warning: Path {raw_path} does not exist. Please check your data folder.")

    courses = pd.read_csv(f'{raw_path}courses.csv')
    assessments = pd.read_csv(f'{raw_path}assessments.csv')
    vle = pd.read_csv(f'{raw_path}vle.csv')
    student_info = pd.read_csv(f'{raw_path}studentInfo.csv')
    student_reg = pd.read_csv(f'{raw_path}studentRegistration.csv')
    student_assess = pd.read_csv(f'{raw_path}studentAssessment.csv')
    
    return courses, assessments, vle, student_info, student_reg, student_assess

def load_student_vle_chunked(raw_path='./', chunk_size=1000000):
    """
    Load the large studentVle.csv in chunks.
    Yields chunks to prevent memory overflow (OOM).
    """
    print(f"Loading studentVle in chunks of {chunk_size}...")
    chunks = pd.read_csv(f'{raw_path}studentVle.csv', chunksize=chunk_size)
    
    for chunk in chunks:
        yield chunk

if __name__ == "__main__":
    print("Testing data loaders...")
    
    try:
        courses, assessments, vle, student_info, student_reg, student_assess = load_plain_tables()
        print(f"Success! Loaded studentInfo: {student_info.shape}")
    except FileNotFoundError:
        print("Error: Could not find the CSV files. Did you download OULAD and put it in the correct folder?")
    
    try:
        for chunk in load_student_vle_chunked():
            print(f"Success! First chunk of studentVle loaded. Shape: {chunk.shape}")
            break
    except FileNotFoundError:
         print("Error: Could not find studentVle.csv in the specified folder.")
