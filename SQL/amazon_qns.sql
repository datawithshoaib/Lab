-- Question 1
create table emp_attendance
(
	employee 	varchar(10),
	dates 		date,
	status 		varchar(20)
);
insert into emp_attendance values('A1', '2024-01-01', 'PRESENT');
insert into emp_attendance values('A1', '2024-01-02', 'PRESENT');
insert into emp_attendance values('A1', '2024-01-03', 'PRESENT');
insert into emp_attendance values('A1', '2024-01-04', 'ABSENT');
insert into emp_attendance values('A1', '2024-01-05', 'PRESENT');
insert into emp_attendance values('A1', '2024-01-06', 'PRESENT');
insert into emp_attendance values('A1', '2024-01-07', 'ABSENT');
insert into emp_attendance values('A1', '2024-01-08', 'ABSENT');
insert into emp_attendance values('A1', '2024-01-09', 'ABSENT');
insert into emp_attendance values('A1', '2024-01-010', 'PRESENT');
insert into emp_attendance values('A2', '2024-01-06', 'PRESENT');
insert into emp_attendance values('A2', '2024-01-07', 'PRESENT');
insert into emp_attendance values('A2', '2024-01-08', 'ABSENT');
insert into emp_attendance values('A2', '2024-01-09', 'PRESENT');
insert into emp_attendance values('A2', '2024-01-10', 'ABSENT');

SELECT * from emp_attendance;

-- Solution
with cte as
		(select *,
			   row_number() over(partition by employee order by employee, dates) as rn
		from emp_attendance),
	cte_present as
		(select *, row_number() over(partition by employee order by employee, dates),
		rn - row_number() over(partition by employee order by employee, dates) as flag
		from cte
		where status = 'PRESENT'),
	cte_absent as
		(select *, row_number() over(partition by employee order by employee, dates),
		rn - row_number() over(partition by employee order by employee, dates) as flag
		from cte
		where status = 'ABSENT')
select employee,
	FIRST_VALUE(dates) over(partition by employee, flag order by employee, dates) as from_date,
    LAST_VALUE(dates) over(partition by employee, flag order by employee, dates
	range between UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING) as to_date,
    status
from cte_present
union
select employee,
	FIRST_VALUE(dates) over(partition by employee, flag order by employee, dates) as from_date,
    LAST_VALUE(dates) over(partition by employee, flag order by employee, dates
	range between UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING) as to_date,
    status
from cte_absent
order by employee, from_date;

-- ------------------------------------------------------------------------------------------
-- Question 2
