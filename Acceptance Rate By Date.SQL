--https://platform.stratascratch.com/coding/10285-acceptance-rate-by-date?code_type=5
-- Acceptance Rate By Date
--What is the overall friend acceptance rate by date? Your output should have the rate of acceptances by the date the request was sent. Order by the earliest date to latest.
--Assume that each friend request starts by a user sending (i.e., user_id_sender) a friend request to another user (i.e., user_id_receiver) that's logged in the table with action = 'sent'. If the request is accepted, the table logs action = 'accepted'. If the request is not accepted, no record of action = 'accepted' is logged.




WITH sent_cte AS
  (SELECT date, user_id_sender,
                user_id_receiver
   FROM fb_friend_requests
   WHERE action='sent' ),
accepted_cte AS
  (SELECT date, user_id_sender,
                user_id_receiver
   FROM fb_friend_requests
   WHERE action='accepted' ),
m1 AS (SELECT a.date, 
a.user_id_sender s1, a.user_id_receiver r1, 
b.user_id_sender s2, b.user_id_receiver r2
FROM sent_cte a
LEFT JOIN accepted_cte b ON 
    a.user_id_sender=b.user_id_sender
    AND a.user_id_receiver=b.user_id_receiver
)

select date, count(r2)/cast(count(s1) AS decimal) from m1
group by date

--count(b.user_id_receiver) as c1, count(a.user_id_sender) as c2, 
--count(b.user_id_receiver)/CAST(count(a.user_id_sender) AS decimal) AS percentage_acceptance
