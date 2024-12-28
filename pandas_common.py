# https://platform.stratascratch.com/coding/10354-most-profitable-companies/official-solution?code_type=2

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
