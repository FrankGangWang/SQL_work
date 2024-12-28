-- Pandas 
--SQL
SQL COUNT( ) with All
In the following, we discuss the usage of the ALL clause with the  SQL COUNT() function to count only non-NULL values for the specified column. The difference between * (asterisk) and ALL is that * counts both NULL and non-NULL values, while ALL counts only non-NULL values.
COUNT(DISTINCT ...) ignores NULL values, as NULL is not considered a distinct value.
COUNT(DISTINCT ...) can be used with multiple columns to count unique combinations of values across those columns.



--Question:Most Profitable Companies
# https://platform.stratascratch.com/coding/10354-most-profitable-companies/official-solution?code_type=2
# df.rank(): method: min=rank, dense=dense_rank, 
'''

method{‘average’, ‘min’, ‘max’, ‘first’, ‘dense’}, default ‘average’
How to rank the group of records that have the same value (i.e. ties):
average: average rank of the group
min: lowest rank in the group
max: highest rank in the group
first: ranks assigned in order they appear in the array
dense: like ‘min’, but rank always increases by 1 between groups.

     profits  rankdense  rankmin  rankmax  rank1st  rankavg
0       42.7     1        1        1        1        1
20      39.0     2        2        3        2        2
100     39.0     2        2        3        3        2
14      37.0     3        4        4        4        4
1       34.2     4        5        5        5        5
'''
# Import library
import pandas as pd

# Add dense rank to the dataframe
forbes_global_2010_2014['rank'] = forbes_global_2010_2014['profits'].rank(method='dense', ascending=False).astype(int)

# Filter top 3 ranks and exclude rank column from the result
top_companies_with_ties = (
    forbes_global_2010_2014[forbes_global_2010_2014['rank'] <= 3]
    [['company', 'profits']]
    .sort_values(by='profits', ascending=False)
)

# Return the result
top_companies_with_ties

#Workers With The Highest Salaries
#https://platform.stratascratch.com/coding/10353-workers-with-the-highest-salaries/official-solution?code_type=2

import pandas as pd
import numpy as np

title_worker_id = title.rename(columns={"worker_ref_id": "worker_id"})
merged_df = pd.merge(worker, title_worker_id, on="worker_id")
max_salary = merged_df[merged_df["salary"] == merged_df["salary"].max()][
    ["worker_title"]
].rename(columns={"worker_title": "best_paid_title"})
result = max_salary
# my code
# Import your libraries
import pandas as pd
'''
worker_id	first_name	last_name	salary	joining_date	department
1	Monika	Arora	100000	2014-02-20 00:00:00	HR
'''
# Start writing code
df = worker
df['rankdense'] = df['salary'].rank(method='dense', ascending=False)
df1 = df[df['rankdense']==1][['worker_id']]
print(df1)
df1 = df1.reset_index(drop=True)
print(df1)

df1.merge(title, left_on='worker_id', right_on='worker_ref_id')['worker_title']
#title[title['worker_ref_id'] == df1]

--Question: Users By Average Session Time
import pandas as pd
import numpy as np

# Filter rows for 'page_load' and 'page_exit' actions
load_df = facebook_web_log[facebook_web_log['action'] == 'page_load'][['user_id', 'timestamp']]
exit_df = facebook_web_log[facebook_web_log['action'] == 'page_exit'][['user_id', 'timestamp']]

# Merge on user_id, considering only pairs where page_load timestamp is less than page_exit timestamp
df = pd.merge(load_df, exit_df, on='user_id', suffixes=['_load', '_exit'])
df = df[df['timestamp_load'] < df['timestamp_exit']]

# Convert timestamps to dates for grouping by user and date without casting
df['date'] = df['timestamp_load'].dt.floor('d')

# Group by user_id and date, then get the max page_load and min page_exit for each group
df = df.groupby(['user_id', 'date']).agg(timestamp_load=('timestamp_load', 'max'),
                                         timestamp_exit=('timestamp_exit', 'min')).reset_index()

# Calculate duration as the difference between max page_load and min page_exit
df['duration'] = (df['timestamp_exit'] - df['timestamp_load']).dt.total_seconds()  # duration in seconds

# Group by user_id and calculate the average session duration in seconds
result = df.groupby('user_id')['duration'].mean().reset_index()




