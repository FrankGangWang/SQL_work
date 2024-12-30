''' Cookbook Recipes
https://platform.stratascratch.com/coding/2089-cookbook-recipes?code_type=2

You are given the table with titles of recipes from a cookbook and their page numbers. You are asked to represent how the recipes will be distributed in the book.
Produce a table consisting of three columns: left_page_number, left_title and right_title. The k-th row (counting from 0), should contain the number and the title of the page with the number 
2×k in the first and second columns respectively, and the title of the page with the number 
2×k+1 in the third column.
Each page contains at most 1 recipe. If the page does not contain a recipe, the appropriate cell should remain empty (NULL value). Page 0 (the internal side of the front cover) is guaranteed to be empty.
'''
# Import your libraries
import pandas as pd
#page_number	title
#1, Scrambled eggs

#left_page_number, left_title and right_title.
# number=k, title at 2k, title at 2k+1
# Start writing code
df = cookbook_titles
df2 = pd.DataFrame(range(df.page_number.max()), columns=['page_number'])
df2 = df2.merge(df, how='outer', on='page_number')
df2['right_title'] = df2.title.shift(-1)
result = df2[df2.index%2==0]

-- solution
import pandas as pd

series = pd.DataFrame({'page_number': range(max(cookbook_titles.page_number) + 1)})
df = series.merge(cookbook_titles, how='left', on='page_number')
df['row_num'] = df.page_number // 2
df_left = df[df.page_number % 2 == 0].groupby('row_num').first().reset_index()

df_right = df[df.page_number % 2 == 1].groupby('row_num').first().reset_index()

result = df_left.merge(df_right, how='outer', on='row_num').sort_values(by='row_num')[['page_number_x','title_x', 'title_y']].rename(columns={'page_number_x': 'left_page_number', 'title_x': 'left_title', 'title_y': 'right_title'})
