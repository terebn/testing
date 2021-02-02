SELECT
    users.user_id,
    COUNTIF(users.has_overdraft_enabled AND ca_days_since_activation = 0) AS od_at_signup, -- 0/1 flag, 1 = enabled od at signup
    COUNTIF(users.has_overdraft_enabled AND ca_days_since_activation <= 30) AS od_by_30d, -- number of days has OD in 30 days. Note: becasue of timing, some users do not have a full month in the experiment. These are taken out of stats.  
    COUNTIF(users.is_in_overdraft AND ca_days_since_activation <= 30) AS used_in_30d -- number of days in OD in first 30 days
FROM test.lending.user_activity AS users
GROUP BY user_id;
