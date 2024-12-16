set search_path = "Intermediate";

create table icc_world_cup
(
Team_1 Varchar(20),
Team_2 Varchar(20),
Winner Varchar(20)
);
INSERT INTO icc_world_cup values('India','SL','India');
INSERT INTO icc_world_cup values('SL','Aus','Aus');
INSERT INTO icc_world_cup values('SA','Eng','Eng');
INSERT INTO icc_world_cup values('Eng','NZ','NZ');
INSERT INTO icc_world_cup values('Aus','India','India');

select * from icc_world_cup;

-- solution (case statement)
with teams as
	(select 
		team_1 as team_name,
		case
			when team_1 = winner then 1
			else 0
		end as win_flag
	from 
		icc_world_cup
	union all
	select 
		team_2 as team_name,
		case
			when team_2 = winner then 1
			else 0
		end as win_flag
	from 
		icc_world_cup)

select
	team_name,
	count(0) as matches_played,
	sum(win_flag) as no_of_wins,
	count(0) - sum(win_flag) as no_of_losses
from
	teams
group by 
	team_name
order by 
	no_of_wins desc, 
	no_of_losses;

-- solution (join)
select
	teams.team_name,
	count(*) as matches_played,
	sum(
		case
			when teams.team_name = icc.winner then 1
			else 0
		end
	) as no_of_wins,
	count(*) - 
	sum(
		case
			when teams.team_name = icc.winner then 1
			else 0
		end
	) as no_of_losses
from
	(
		select distinct team_1 as team_name from icc_world_cup
		union
		select distinct team_2 as team_name from icc_world_cup
	) teams
join
	icc_world_cup icc
on 
	teams.team_name = icc.team_1 or teams.team_name = icc.team_2
group by
	teams.team_name
order by
	no_of_wins desc,
	no_of_losses;
