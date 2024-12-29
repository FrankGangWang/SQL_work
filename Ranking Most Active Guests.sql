--Ranking Most Active Guests
--https://platform.stratascratch.com/coding/10159-ranking-most-active-guests?code_type=5
--Rank guests based on the total number of messages they've exchanged with any of the hosts. Guests with the same number of messages as other guests should have the same rank. Do not skip rankings if the preceding rankings are identical.
Output the rank, guest id, and number of total messages they've sent. Order by the highest number of total messages first.

-- https://www.amitgrinson.com/blog/window-function-with-groupby/#fn:2
Let’s assume you want to aggregate the data in some way, and then take the top 1 row of some group. So in our case, we want to return users receiving the most funds within a given country:
WITH users_sum as (
SELECT u.user_id,
  u.Country,
  SUM(amount) AS total_funds,
  DENSE_RANK() OVER(PARTITION BY COUNTRY ORDER BY SUM(amount) DESC) as rnk
FROM USERS U 
LEFT JOIN PAYMENTS P ON P.USER_ID = u.user_id
GROUP BY u.user_id, u.country
)
SELECT user_id,  Country,  total_funds FROM USERS_SUM where rnk = 1

“Grouped aggregates operate on groups of rows defined by the GROUP BY clause and return one value per group.
Window aggregates operate on windows of rows and return one value for each row in the underlying query”

Google Cloud’s BigQuery docs says it more explicitly3:
“A window function is evaluated after aggregation.[…] Because aggregate functions are evaluated before window functions, 
    aggregate functions can be used as input operands to window functions.”

Therefore the GROUP BY occurs, and then we SELECT the relevant columns we want in our aggregation, and any window 
    function in the SELECT is evaluated on the post-aggregated data. In a sense we reference the already-aggregated
    column SUM(amount) as a column to sort our ranking window function we’re creating!

https://cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls
Window function calls in BigQuery:
A window function, also known as an analytic function, computes values over a group of rows and returns a single result for each row. 
This is different from an aggregate function, which returns a single result for a group of rows.
A window function includes an OVER clause, which defines a window of rows around the row being evaluated. For each row, 
the window function result is computed using the selected window of rows as input, possibly doing aggregation.
With window functions you can compute moving averages, rank items, calculate cumulative sums, and perform other analyses.
    
    

    

SELECT 
    DENSE_RANK() OVER(ORDER BY SUM(n_messages) DESC) as ranking, 
    id_guest, 
    SUM(n_messages) as sum_n_messages
FROM airbnb_contacts
GROUP BY id_guest
ORDER BY sum_n_messages DESC


-- my code
--select * from airbnb_contacts where id_guest = '62d09c95-c3d2-44e6-9081-a3485618227d'
with t1 AS (
select id_guest, 
   sum(n_messages) as sum_n_messages
from airbnb_contacts
group by id_guest
)

select 
dense_rank() over ( order by sum_n_messages desc) as ranking
, id_guest, sum_n_messages
from t1
order by dense_rank() over ( order by sum_n_messages desc)  
