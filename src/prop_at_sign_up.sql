WITH 
exposure AS(
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
WHERE users.is_overdraft_eligible = true
),
metrics AS (
SELECT
    users.user_id,
    COUNTIF(users.has_overdraft_enabled AND ca_days_since_activation	 = 0) AS od_at_signup,
    COUNTIF(users.has_overdraft_enabled AND ca_days_since_activation	 <= 30) AS od_by_30d,
    COUNTIF(users.is_in_overdraft AND ca_days_since_activation <= 30) AS used_in_30d
FROM test.lending.user_activity AS users
GROUP BY user_id
)

SELECT 
    variant_id,
    (1.0 * COUNTIF(od_at_signup > 0)) / COUNT(*) AS prop_enabled,
    COUNT(*) AS num_exposed,
    COUNTIF(od_at_signup > 0) AS num_signup
FROM exposure 
LEFT JOIN metrics using (user_id)
GROUP BY variant_id
ORDER BY variant_id;