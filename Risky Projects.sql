--Risky Projects
-- https://platform.stratascratch.com/coding/10304-risky-projects?code_type=5
--Identify projects that are overbudget. A project is overbudget if the prorated cost of all employees assigned to it exceeds the project’s budget.


To determine this, prorate each employee's annual salary to match the project's duration. For example, if a project with a six-month duration has a budget of $10,000.


Output a list of overbudget projects with the following details: project name, project budget, and prorated total employee expenses (rounded up to the nearest dollar).


Hint: Assume all years have 365 days and disregard leap years.


--select * from linkedin_projects where title = 'Project1'

with m1 AS (
    select 
      title, budget, t_proj.id as proj_id, salary, t_emp.emp_id,
      DATEDIFF(day, start_date, end_date) as tdiff
    from linkedin_projects t_proj
    inner join linkedin_emp_projects t_emp ON
    t_proj.id = t_emp.project_id
    inner join linkedin_employees t_salary ON
    t_emp.emp_id = t_salary.id
)

select title, budget, 
--tdiff/365.0 as part, sum(salary) as totalsalary,
ceiling(sum(salary)*tdiff/365.0) as prorated_employee_expense
from m1 
group by title, budget, tdiff
having ceiling(sum(salary)*tdiff/365.0) > m1.budget
order by title
--Project2	32487	52870



