WITH 
users_d0 AS (
SELECT *
FROM test.lending.user_activity AS users
LEFT JOIN test.lending.experiment_assigned_users AS experiment 
ON users.user_id = experiment.user_id
WHERE users.ca_days_since_activation = 0
)

SELECT 
    variant_id,
    COUNT(*) AS all_ids,
    COUNT(variant_id) AS ids_in_experiment,
    SUM(CASE WHEN is_overdraft_eligible = true AND variant_id IS NOT NULL THEN 1 ELSE 0 END) AS ids_in_experiment_and_od_eligible
  FROM users_d0
GROUP BY variant_id
ORDER BY variant_id DESC;