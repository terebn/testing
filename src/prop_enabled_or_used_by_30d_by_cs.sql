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
    credit_score_quintile_d0,
    (1.0 * COUNTIF(od_by_30d > 0)) / COUNT(*) AS prop_enabled,
    (1.0 * COUNTIF(used_in_30d > 0)) / COUNT(*) AS prop_used,
    (1.0 * COUNTIF(used_in_30d > 0)) / COUNTIF(od_by_30d > 0) AS prop_with_od_used,
    AVG(used_in_30d) AS avg_days_od_use,
    COUNT(*) AS num_exposed,
    COUNTIF(od_by_30d > 0) AS num_enabled,
    COUNTIF(used_in_30d > 0) AS num_used,
    SUM(used_in_30d) AS sum_days,
    COUNT(od_by_30d) AS num_days
FROM exposure 
LEFT JOIN metrics using (user_id)
WHERE num_days >= 30
GROUP BY variant_id, credit_score_quintile_d0
ORDER BY credit_score_quintile_d0, variant_id;