SELECT 
    experiment.user_id,
    variant_id,
    ntile(5) OVER (ORDER BY users.credit_score) AS credit_score_quintile_d0, -- includes NULL in bucket 1 
    users.credit_score AS credit_score_d0,
    users.app_version AS app_version_d0, 
    users.user_mobile_phone_os AS user_mobile_phone_os_d0, 
    user_days.num_days
FROM test.lending.experiment_assigned_users AS experiment  
LEFT JOIN test.lending.user_activity AS users
ON (users.user_id = experiment.user_id AND users.ca_days_since_activation = 0)
LEFT JOIN (
    SELECT
        user_id,
        MAX(ca_days_since_activation) AS num_days
    FROM test.lending.user_activity
    GROUP BY user_id
    ) AS user_days ON (experiment.user_id = user_days.user_id)
WHERE users.is_overdraft_eligible = true;
