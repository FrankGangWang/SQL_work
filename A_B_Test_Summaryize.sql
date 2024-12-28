https://medium.com/@foundinblank/using-sql-to-summarize-a-b-experiments-d30428edfb55
https://gist.githubusercontent.com/foundinblank/259c2d0d6e66b513c8ecf0694877ee1f/raw/4471f5c7220bed59b21ca1db4187979ddbbe3e23/create_user_level_table.sql

create table experiments.sundae_wizard_users as

-- Get all users exposed to the experiment
with exposed_users as (

    select
        experiment_name,
        user_id,
        feature_flag_evaluation,
        evaluated_at
    from analytics.fct_experiment_assignments
    where experiment_name = 'sundae_wizard'
        and evaluated_at between '2022-07-01' and '2022-07-15'

),

-- If an user id shows up multiple times, it's because they saw more than one variant
multiple_variants as (

    select
        user_id,
        count(*) as variants
    from exposed_users
    group by 1
    having variants > 1

),

-- Remove users who saw multiple variants
exposed_users_cleaned as (

    select exposed_users.*
    from exposed_users
    left join multiple_variants
        on exposed_users.user_id = multiple_variants.user_id
    where multiple_variants.user_id is null

),

-- Build your users table, and exclude spam users
users as (

    select
        exposed_users_cleaned.user_id,
        iff(exposed_users_cleaned.feature_flag_evaluation, 'test', 'control') as cohort,
        exposed_users_cleaned.evaluated_at as assigned_at,
        dim_users.created_at,
        dim_users.city_name,
        dim_users.signup_marketing_channel,
        dim_users.first_order_at
    from analytics.dim_users
    inner join exposed_users
        on dim_users.user_id = exposed_users.user_id
    where dim_users.is_spam = false 

),

-- Last, join order metrics for all orders during the experiment period (excluding any orders prior to exp. assignment)
final as (

    select
        users.*,
        count(iff(fct_orders.order_type = 'sundae', fct_orders.order_id, null)) as cnt_sundae_orders,
        count(fct_orders.order_id) as cnt_orders,
        coalesce(sum(fct_orders.order_value), 0) as total_order_value,
        cnt_orders > 0 as is_user_converted
    from users
    left join analytics.fct_orders
        on users.user_id = fct_orders.user_id
        and fct_orders.order_placed_at between '2022-07-01' and '2022-07-15'
        and fct_orders.order_placed_at > users.assigned_at
    group by 1, 2, 3, 4, 5, 6, 7

)

select * from final;

select
    cohort,
    count(user_id) as cnt_users,
    sum(cnt_sundae_orders) as total_sundae_orders,
    sum(cnt_orders) as total_orders,
    sum(total_order_value) as total_order_value,
    sum(is_user_converted::int) as cnt_converted_users,
    total_sundae_orders / cnt_users as avg_sundae_orders,
    total_orders / cnt_users as avg_orders,
    total_order_value / total_orders as avg_order_value, 
    cnt_converted_users / cnt_users as conversion_rate
from experiments.sundae_wizard_users
group by 1
order by 1  -- This keeps cohorts in the same order every time you run this code
;

╔═════════╦═══════════╦═════════════════════╦══════════════╦═══════════════════╦═════════════════════╦═══════════════════╦════════════╦═════════════════╦═════════════════╗
║ cohort  ║ cnt_users ║ total_sundae_orders ║ total_orders ║ total_order_value ║ cnt_converted_users ║ avg_sundae_orders ║ avg_orders ║ avg_order_value ║ conversion_rate ║
╠═════════╬═══════════╬═════════════════════╬══════════════╬═══════════════════╬═════════════════════╬═══════════════════╬════════════╬═════════════════╬═════════════════╣
║ control ║     4,707 ║               3,671 ║        4,848 ║            42,616 ║               4,566 ║              0.78 ║       1.03 ║            8.79 ║            0.97 ║
╠═════════╬═══════════╬═════════════════════╬══════════════╬═══════════════════╬═════════════════════╬═══════════════════╬════════════╬═════════════════╬═════════════════╣
║ test    ║     4,681 ║               3,885 ║        4,868 ║            43,863 ║               4,353 ║              0.83 ║       1.04 ║            9.01 ║            0.93 ║
╚═════════╩═══════════╩═════════════════════╩══════════════╩═══════════════════╩═════════════════════╩═══════════════════╩════════════╩═════════════════╩═════════════════╝

If you’re lucky enough to work at a place that runs many experiments, you’ll find yourself writing the same SQL many times. 
The natural next step is how to automate that. I’ve used a range of different approaches for how to automate user-level tables and 
summary metrics over an unknown x number of experiments: brute force (processing all experiment/feature flag names), 
relying on dbt seeds and dbt macros, relying on an in-house experimentation platform, or using experimentation platform apps 
like Eppo or GrowthBook.

The next steps after calculating summary metrics are testing for significance and reporting lift & incrementality. 
I’ll write another post about how to do that.

Then comes the most important part. Through deep-dives and good ol’ data analysis work, we build a story about how and why 
we’ve gotten these metrics. The summary metrics and statistical significance are just starting points; the ✨ valuable insights ✨ lie in figuring out the how and why!

