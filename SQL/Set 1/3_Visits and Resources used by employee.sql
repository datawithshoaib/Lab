set search_path = "Intermediate";

create table entries ( 
	name varchar(20),
	address varchar(20),
	email varchar(20),
	floor int,
	resources varchar(10));

insert into entries values 
('A','Bangalore','A@gmail.com',1,'CPU'),
('A','Bangalore','A1@gmail.com',1,'CPU'),
('A','Bangalore','A2@gmail.com',2,'DESKTOP'),
('B','Bangalore','B@gmail.com',2,'DESKTOP'),
('B','Bangalore','B1@gmail.com',2,'DESKTOP'),
('B','Bangalore','B2@gmail.com',1,'MONITOR');

select * from entries;

-- solution
with tv as (
	select name, count(1) as total_visits
	from entries
	group by name
),
mvf as (
	select name, floor, count(1) as no_of_floor_visit,
		rank() over(partition by name order by count(1) desc) as rnk
		from entries
		group by name, floor
),
distinct_res as (
	select name, string_agg(distinct resources, ',') as dist_resources
	from entries
	group by name
)
select mvf.name,
	tv.total_visits as total_visits,
	mvf.floor as most_visited_floor,
	distinct_res.dist_resources
from mvf 
	inner join tv on mvf.name = tv.name
	inner join distinct_res on mvf.name = distinct_res.name
where rnk = 1
order by name;

-- solution 2 (without using distinct inside string_agg function)
with tv as (
	select name, count(1) as total_visits
	from entries
	group by name
),
mvf as (
	select name, floor, count(1) as no_of_floor_visit,
		rank() over(partition by name order by count(1) desc) as rnk
		from entries
		group by name, floor
),
distinct_res as (
	select distinct name, resources
	from entries
),
used_res as (
	select name, string_agg(resources, ',') as used_resources
	from distinct_res
	group by name
)
select mvf.name,
	tv.total_visits as total_visits,
	mvf.floor as most_visited_floor,
	used_res.used_resources
from mvf 
	inner join tv on mvf.name = tv.name
	inner join used_res on mvf.name = used_res.name
where rnk = 1
order by name;
