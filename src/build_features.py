import pandas as pd
import os

def build_weekly_activity(raw_path='data/raw/'):
    print("Building weekly activity features...")
    
    if not os.path.exists(f'{raw_path}studentVle.csv'):
        print(f"Error: Could not find studentVle.csv at {raw_path}")
        return None

    chunks = pd.read_csv(f'{raw_path}studentVle.csv', chunksize=1000000)
    weekly_data = []
    
    for chunk in chunks:
        chunk['week'] = (chunk['date'] // 7) + 1
        chunk['week'] = chunk['week'].clip(lower=0) 
        
        grouped = chunk.groupby(['id_student', 'code_module', 'code_presentation', 'week']).agg(
            total_clicks=('sum_click', 'sum'),
            active_days=('date', 'nunique'),
            distinct_materials=('id_site', 'nunique')
        ).reset_index()
        
        weekly_data.append(grouped)
        
    final_weekly = pd.concat(weekly_data)
    
    final_weekly = final_weekly.groupby(['id_student', 'code_module', 'code_presentation', 'week']).agg(
        total_clicks=('total_clicks', 'sum'),
        active_days=('active_days', 'sum'),
        distinct_materials=('distinct_materials', 'sum')
    ).reset_index()
    
    print(f"Done! Generated {len(final_weekly)} weekly records.")
    return final_weekly

if __name__ == "__main__":
    weekly_df = build_weekly_activity()
    
    if weekly_df is not None:
        os.makedirs('data/processed', exist_ok=True)
        
        output_path = 'data/processed/weekly_activity.csv'
        weekly_df.to_csv(output_path, index=False)
        print(f"Saved to {output_path}")
        
        print("\nFirst 5 rows:")
        print(weekly_df.head())
