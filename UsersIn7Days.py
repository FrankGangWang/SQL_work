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


-----New Products
--https://platform.stratascratch.com/coding/10318-new-products?code_type=2
import pandas as pd
import numpy as np
from datetime import datetime

df_2020 = car_launches[car_launches['year'].astype(str) == '2020']
df_2019 = car_launches[car_launches['year'].astype(str) == '2019']
df = pd.merge(df_2020, df_2019, how='outer', on=[
    'company_name'], suffixes=['_2020', '_2019']).fillna(0)
df = df[df['product_name_2020'] != df['product_name_2019']]
df = df.groupby(['company_name']).agg(
    {'product_name_2020': 'nunique', 'product_name_2019': 'nunique'}).reset_index()
df['net_new_products'] = df['product_name_2020'] - df['product_name_2019']
result = df[['company_name', 'net_new_products']]


-- My code: groupby, sort, shift
# Import your libraries
import pandas as pd

# Start writing code
car_launches.head()
g = car_launches.groupby(by=['year', 'company_name'], as_index=False)
df = g['product_name'].count()
df.columns = ['year', 'company_name', 'count_products']
df.sort_values(by=['company_name', 'year' ], inplace=True)
df['lag'] = df['count_products'].shift()
#print(df)
result = df[df['year']==2020]
result['net_new_products'] = (result['count_products'] - result['lag']).astype(int)

result = result[['company_name', 'net_new_products']]
#print(result.shape, df.shape, car_launches.shape)

---Top Percentile Fraud
import pandas as pd
import numpy as np
fraud_score["percentile"] = fraud_score.groupby('state')['fraud_score'].rank(pct=True)
df= fraud_score[fraud_score['percentile']>.95]
result = df[['policy_num','state','claim_cost','fraud_score']]

-- my code
# Import your libraries
import pandas as pd

# Start writing code
fraud_score.head()

g = fraud_score.groupby(by='state')
fraud_score['rankpct'] = g['fraud_score'].rank(method='first', ascending=True, pct=True)
fraud_score.sort_values(by=['state', 'rankpct'], ascending=[True, False], inplace=True)

print(fraud_score.shape)
fraud_score = fraud_score[fraud_score['rankpct']>=0.95]
print(fraud_score.shape)
print(fraud_score)

