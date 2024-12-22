--Ranking Most Active Guests
--https://platform.stratascratch.com/coding/10159-ranking-most-active-guests?code_type=5
--Rank guests based on the total number of messages they've exchanged with any of the hosts. Guests with the same number of messages as other guests should have the same rank. Do not skip rankings if the preceding rankings are identical.
Output the rank, guest id, and number of total messages they've sent. Order by the highest number of total messages first.

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
