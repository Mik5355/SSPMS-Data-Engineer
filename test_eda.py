import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/final_model_data.csv')
sns.set_theme(style="whitegrid")
print("Building 4 comprehensive charts... Please wait.")

fig, axes = plt.subplots(2, 2, figsize=(20, 16))
fig.subplots_adjust(hspace=0.5, wspace=0.3)

sns.countplot(data=df, x='at_risk', hue='at_risk', palette='Set2', ax=axes[0, 0], legend=False)
axes[0, 0].set_title('Distribution of Final Results', fontsize=14)
axes[0, 0].set_xlabel('Status (0 = Successful, 1 = At Risk)', fontsize=12)
axes[0, 0].set_ylabel('Number of Students', fontsize=12)

sns.histplot(data=df[df['mean_score'] > 0], x='mean_score', hue='at_risk', palette='Set1', kde=True, ax=axes[0, 1])
axes[0, 1].set_title('Distribution of Assessment Scores', fontsize=14)
axes[0, 1].set_xlabel('Mean Score', fontsize=12)
axes[0, 1].set_ylabel('Frequency', fontsize=12)

sns.boxplot(data=df, x='at_risk', y='avg_weekly_clicks', hue='at_risk', palette='Set1', ax=axes[1, 0], legend=False)
axes[1, 0].set_title('Distribution of Weekly Activity', fontsize=14)
axes[1, 0].set_xlabel('Status (0 = Successful, 1 = At Risk)', fontsize=12)
axes[1, 0].set_ylabel('Average Weekly Clicks', fontsize=12)

avg_early = df.groupby('at_risk')['clicks_first_2w'].mean()
avg_late = df.groupby('at_risk')['clicks_last_2w'].mean()
axes[1, 1].plot(['First 2 Weeks', 'Last 2 Weeks'], [avg_early[0], avg_late[0]], marker='o', label='Successful (0)', color='green', linewidth=2)
axes[1, 1].plot(['First 2 Weeks', 'Last 2 Weeks'], [avg_early[1], avg_late[1]], marker='o', label='At Risk (1)', color='red', linewidth=2)
axes[1, 1].set_title('Activity Curves: When They Diverge', fontsize=14)
axes[1, 1].set_ylabel('Average Clicks', fontsize=12)
axes[1, 1].legend()

plt.show()
print("Done! 4 charts are displayed.")