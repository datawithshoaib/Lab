CREATE TABLE examples.transactions(
	transaction_id INT,
	user_id INT,
	amount INT,
	transaction_date TIMESTAMP
);

select * from examples.transactions;

select *
from (
select *,
	row_number() over(partition by user_id order by amount desc) as rnk
	from examples.transactions
) ranked
where rnk <= 3;
