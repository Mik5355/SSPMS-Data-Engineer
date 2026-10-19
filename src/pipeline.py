import pandas as pd
from sklearn.preprocessing import LabelEncoder

def run_pipeline(base_df, weekly_activity_df):
    df = base_df.copy()
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna(df[col].mode()[0])
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].fillna(df[col].median())

    df = df.drop_duplicates(subset=['id_student', 'code_module', 'code_presentation'])

    df['at_risk'] = df['final_result'].apply(lambda x: 1 if x in ['Fail', 'Withdrawn'] else 0)
    
    cols_to_drop = [
        'final_result', 
        'gender', 'disability', 'region', 'imd_band', 'age_band'  
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    weekly_activity_df = weekly_activity_df[weekly_activity_df['week'] <= 6]

    student_weekly = weekly_activity_df.groupby(['id_student', 'code_module', 'code_presentation']).agg(
        avg_weekly_clicks=('total_clicks', 'mean'),
        avg_active_days=('active_days', 'mean'),
        total_materials=('distinct_materials', 'sum')
    ).reset_index()

    df_merged = pd.merge(df, student_weekly, on=['id_student', 'code_module', 'code_presentation'], how='left')
    df_merged = df_merged.fillna(0)

    for col in df_merged.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df_merged[col] = le.fit_transform(df_merged[col].astype(str))

    return df_merged

if __name__ == "__main__":
    from load_data import load_plain_tables, merge_base_tables
    
    courses, assessments, vle, student_info, student_reg, student_assess = load_plain_tables()
    base_data = merge_base_tables(student_info, student_reg, courses)
    
    weekly_data = pd.read_csv('data/processed/weekly_activity.csv')
    
    final_dataset = run_pipeline(base_data, weekly_data)
    
    output_path = 'data/processed/final_model_data.csv'
    final_dataset.to_csv(output_path, index=False)
    
    print("Success")