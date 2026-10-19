import pandas as pd
from load_data import MODULES

PREDICTION_WEEK = 6
CUTOFF_DAY = PREDICTION_WEEK * 7
KEY = ['id_student', 'code_module', 'code_presentation']
PREFINAL_WEIGHT = 60

DROP_FROM_FEATURES = [
    'final_result',
    'date_unregistration', 'date_registration', 'module_presentation_length',
    'gender', 'disability', 'region', 'imd_band', 'age_band',
    'highest_education',
]

def build_assessment_features(student_assess, assessments, week=PREDICTION_WEEK, prefinal_weight=PREFINAL_WEIGHT):
    cutoff = week * 7
    cfg = assessments.copy()

    is_exam = cfg.assessment_type == 'Exam'
    group = ['code_module', 'code_presentation']
    pre_sum = cfg[~is_exam].groupby(group)['weight'].transform('sum')
    exam_sum = cfg[is_exam].groupby(group)['weight'].transform('sum')
    cfg.loc[~is_exam, 'grade_weight'] = cfg.loc[~is_exam, 'weight'] / pre_sum * prefinal_weight
    cfg.loc[is_exam, 'grade_weight'] = cfg.loc[is_exam, 'weight'] / exam_sum * (100 - prefinal_weight)

    due = cfg[cfg['date'] < cutoff]
    s = student_assess.merge(due, on='id_assessment')
    s = s[s['date_submitted'] < cutoff]

    feat = s.groupby(KEY).agg(
        n_submitted=('score', 'count'),
        mean_score=('score', 'mean'),
        min_score=('score', 'min'),
    ).reset_index()

    s['earned'] = s['score'] / 100 * s['grade_weight']
    earned = s.groupby(KEY)['earned'].sum().reset_index(name='points_earned')
    feat = feat.merge(earned, on=KEY, how='left')

    n_due = due.groupby(group).size().reset_index(name='n_due')
    return feat, n_due

def run_pipeline(base_df, weekly_activity_df, student_assess=None, assessments=None, week=PREDICTION_WEEK, modules=None):
    df = base_df.copy()

    if modules:
        df = df[df.code_module.isin(modules)]

    cutoff = week * 7
    left_early = df['date_unregistration'] < cutoff
    print(f"Excluded {int(left_early.sum())} students who left before day {cutoff}")
    df = df[~left_early]

    df = df.drop_duplicates(subset=KEY)
    df['at_risk'] = df['final_result'].isin(['Fail', 'Withdrawn']).astype(int)

    weekly = weekly_activity_df[weekly_activity_df['week'] < week]
    g = weekly.sort_values('week').groupby(KEY)
    student_weekly = g.agg(
        avg_weekly_clicks=('total_clicks', 'mean'),
        total_clicks=('total_clicks', 'sum'),
        avg_active_days=('active_days', 'mean'),
        total_materials=('distinct_materials', 'sum'),
    ).reset_index()
    
    student_weekly['silent_weeks'] = g['total_clicks'].apply(lambda s: int((s == 0).sum())).values
    student_weekly['clicks_last_2w'] = g['total_clicks'].apply(lambda s: float(s.tail(2).sum())).values
    student_weekly['clicks_first_2w'] = g['total_clicks'].apply(lambda s: float(s.head(2).sum())).values
    student_weekly['click_trend'] = (student_weekly['clicks_last_2w'] - student_weekly['clicks_first_2w'])

    df = df.merge(student_weekly, on=KEY, how='left')

    if student_assess is not None and assessments is not None:
        assess_feat, n_due = build_assessment_features(student_assess, assessments, week)
        df = df.merge(assess_feat, on=KEY, how='left')
        df = df.merge(n_due, on=['code_module', 'code_presentation'], how='left')
        df['n_submitted'] = df['n_submitted'].fillna(0)
        df['n_due'] = df['n_due'].fillna(0)
        df['n_missed'] = df['n_due'] - df['n_submitted']
        df['submitted_share'] = (df['n_submitted'] / df['n_due'].replace(0, 1))
        df = df.drop(columns='n_due')

    activity_cols = [c for c in student_weekly.columns if c not in KEY]
    assess_cols = ['n_submitted', 'mean_score', 'min_score', 'points_earned', 'n_missed', 'submitted_share']
    for col in activity_cols + [c for c in assess_cols if c in df.columns]:
        df[col] = df[col].fillna(0)

    df = df.drop(columns=[c for c in DROP_FROM_FEATURES if c in df.columns])

    feature_cols = [c for c in df.columns if c not in KEY + ['at_risk']]
    print(f"Rows: {len(df)}, at_risk: {df.at_risk.mean():.3f}, features: {len(feature_cols)}")
    return df, feature_cols

if __name__ == "__main__":
    from load_data import load_plain_tables, merge_base_tables

    courses, assessments, vle, student_info, student_reg, student_assess = load_plain_tables()
    base_data = merge_base_tables(student_info, student_reg, courses)

    weekly_data = pd.read_csv('data/processed/weekly_activity.csv')

    final_dataset, feature_cols = run_pipeline(
        base_data, weekly_data, student_assess, assessments, modules=MODULES)

    output_path = 'data/processed/final_model_data.csv'
    final_dataset.to_csv(output_path, index=False)

    with open('data/processed/feature_columns.txt', 'w') as f:
        f.write('\n'.join(feature_cols))

    print("Success")