#Finding User Purchases
#Interview Question Date: December 2020
https://platform.stratascratch.com/coding/10322-finding-user-purchases?code_type=2

#Identify returning active users by finding users who made a second purchase within 7 days of any previous purchase. 
Output a list of these user_ids.
#id	user_id	item	created_at	revenue
#1	109	milk	2020-03-03 00:00:00	123
import pandas as pd
import numpy as np
from datetime import datetime

amazon_transactions["created_at"] = pd.to_datetime(amazon_transactions["created_at"]).dt.strftime('%m-%d-%Y')
df = amazon_transactions.sort_values(by=['user_id', 'created_at'], ascending=[True, True])
df['prev_value'] = df.groupby('user_id')['created_at'].shift()
df['days'] = (pd.to_datetime(df['created_at']) - pd.to_datetime(df['prev_value'])).dt.days
result = df[df['days'] <= 7]['user_id'].unique()
for user_id in [112, 120, 128, 150]:
    print(df[df['user_id']==user_id])





# Import your libraries
import pandas as pd
import numpy as np
# Start writing code
#amazon_transactions.head()
df = amazon_transactions

g = df.groupby('user_id')
df['rankday'] = g['created_at'].rank('dense')
df1 = df[df['rankday']==1][['user_id', 'created_at']]
df2 = df[df['rankday']==2][['user_id', 'created_at']]
dfm = df1.merge(df2, 'inner', on='user_id').sort_values(by='user_id')
dfx = dfm[(dfm['created_at_y'] - dfm['created_at_x']).dt.days<=7]
print(df[df['user_id']==112])
print(dfm)

#print(dfx.shape, df1.shape, df2.shape)
print(dfx['user_id'])
result = dfx['user_id'].unique()





