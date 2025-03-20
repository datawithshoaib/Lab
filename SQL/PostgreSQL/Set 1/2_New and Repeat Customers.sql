set search_path = "Intermediate";

create table customer_orders (
	order_id integer,
	customer_id integer,
	order_date date,
	order_amount integer
);

insert into customer_orders values
(1,100,cast('2022-01-01' as date),2000),
(2,200,cast('2022-01-01' as date),2500),
(3,300,cast('2022-01-01' as date),2100),
(4,100,cast('2022-01-02' as date),2000),
(5,400,cast('2022-01-02' as date),2200),
(6,500,cast('2022-01-02' as date),2700),
(7,100,cast('2022-01-03' as date),3000),
(8,400,cast('2022-01-03' as date),1000),
(9,600,cast('2022-01-03' as date),3000);

select * from customer_orders;

-- solution (for understanding)
with first_visit as (
	select customer_id, min(order_date) as first_visit_date
	from customer_orders
	group by customer_id
),

visit_flag as (
	select 
		co.*, 
		fv.first_visit_date,
		case
			when co.order_date = fv.first_visit_date then 1
			else 0
			end as first_visit_flag,
		case
			when co.order_date != fv.first_visit_date then 1
			else 0
			end as repeat_visit_flag
	from 
		customer_orders co 
		inner join first_visit fv
		on co.customer_id = fv.customer_id
)

select 
	order_date,
	sum(first_visit_flag) as new_customer_count,
	sum(repeat_visit_flag) as repeat_customer_count
from 
	visit_flag
group by
	order_date
order by
	order_date;

-- final solution (decreasing query size)
with first_visit as (
	select customer_id, min(order_date) as first_visit_date
	from customer_orders
	group by customer_id
)

select 
	co.order_date,
	sum(case
		when co.order_date = fv.first_visit_date then 1
		else 0
		end) as new_customer_count,
	sum(case
		when co.order_date != fv.first_visit_date then 1
		else 0
		end) as repeat_customer_count
from 
	customer_orders co 
	inner join first_visit fv
	on co.customer_id = fv.customer_id
group by
	co.order_date
order by
	co.order_date;








