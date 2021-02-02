WITH experiment_ids AS (
SELECT experiment.user_id AS user_id_exp,
       users.user_id AS user_id_user,
       users.is_overdraft_eligible,
       experiment.variant_id
FROM test.lending.experiment_assigned_users AS experiment 
LEFT JOIN test.lending.user_activity AS users
ON users.user_id = experiment.user_id
WHERE users.ca_days_since_activation = 0
)

SELECT COUNT(user_id_exp) AS ids_in_exp,
       COUNT(user_id_user) AS ids_in_exp_and_users
FROM experiment_ids
WHERE is_overdraft_eligible = true AND variant_id IS NOT NULL;