# AB-test

Simple evaluation of an A/B test. 

The hypothetical change to evaluate is the introduction of a new version of the sign up page shown to new customers at an online bank.

In the new version overdraft credit is presented as a default, rather than choice. 

## scripts

* *id_counts.sql* : counts the number of users in the experiment who were included in the analysis
* *ids_in_exp_who_activate_card.sql* : checks that all those in the experiment activate their card
* *exposure.sql* : for each user in the analysis, characteristics at time of sign up (assumed to be the same as day of card activation) and count of how many days they are in the experiment for (only users in the experiment for 30 days are used for some of the metrics). The table is used in all the prop_ queries. I would have normally saved this table and called in the prop_ scripts.
* *metrics.sql* : for each user in the analysis, calculates the metrics the experiment may have moved. This table is used in all the prop_ queries. 
* *prop_at_sign_up.sql* : proportion of all users in the experiment who enabled overdraft
* *prop_at_sign_up_by_cs.sql* : as above, by credit score quintile
* *prop_enabled_or_used_by_30d.sql* : proportion of users in the experiment for at least 30 days who enabled and used overdraft, number of days in overdraft
* *prop_enabled_or_used_by_30d_by_cs.sql* : as above, by credit score quintile
* *power_hyp_test.py* : Hypothesis testing and power analysis of the results in the *prop_* queries 
  