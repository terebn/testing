import numpy as np
import pandas as pd
from statsmodels.stats.proportion import power_proportions_2indep as power2p
from statsmodels.stats.proportion import proportions_ztest as test2p
import seaborn as sns
import matplotlib.pyplot as plt

# Count users in experiment 

df = pd.read_csv('id_counts.csv')

sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.set_style("ticks")
ax = df.set_index('variant_id').T.plot(kind='bar', stacked=True)
plt.tight_layout()
ax.figure.savefig('ids.png')

df['all_ids_prop'] = df['all_ids'] / sum(df['all_ids'])
df['ids_in_experiment_prop'] = df['ids_in_experiment'] / sum(df['ids_in_experiment'])
df['ids_in_experiment_and_od_eligible_prop'] = df['ids_in_experiment_and_od_eligible'] / sum(df['ids_in_experiment_and_od_eligible'])

# Define a function to do hypothesis test and power analysis 

def prop_test(trials, successes):

    props = successes / trials

    power = power2p(
        diff=props[1] - props[0],
        prop2=props[1],
        nobs1=trials[0],
        ratio=trials[1]/trials[0],
        alpha=0.05,
        alternative='two-sided'
    )

    test = test2p(
        count=successes, 
        nobs=trials,
        alternative='two-sided'
    )

    print(f"Control rate {props[0]:.2%}")
    print(f"Test rate {props[1]:.2%}")
    print(f"Lift {props[1]/props[0] - 1:.2%}")
    print(f"Power against measured difference: {power.power:.2%}")
    print(f"P-value of two-sided test: {test[1]:.2%}")

# Proportion who enabled OD at sign up 
# Note: the basis is everybody who was eligible for OD at sign up

df = pd.read_csv('prop_at_sign_up.csv')

prop_test(
    trials = np.array(df['num_exposed']),
    successes = np.array(df['num_signup'])
)

# Proportion who enabled OD at sign up by credit score quintile

df = pd.read_csv('prop_at_sign_up_by_cs.csv')

for i in range(1,6):
    print('-------------------------------')
    print(f'For credit score quantile: {i}')
    print('-------------------------------')
    print('-> Proportion who enabled OD at sign up')
    prop_test(
        trials = np.array(df[df['credit_score_quintile_d0']== i]['num_exposed']),
        successes = np.array(df[df['credit_score_quintile_d0']== i]['num_signup'])
    )

# Proportion who enabled or used OD within 30 days of activation
# Note: the base is consumers who were in the experiment for at least 30 days

df = pd.read_csv('prop_enabled_or_used_by_30d.csv')

# Proportion of users who enabled OD
print('-> Proportion of users who enabled OD')
prop_test(
    trials = np.array(df['num_exposed']),
    successes = np.array(df['num_enabled'])
)

# Proportion of users who used OD
print('-> Proportion of users who used OD')
prop_test(
    trials = np.array(df['num_exposed']),
    successes = np.array(df['num_used'])
)

# Proportion of users who used OD of those who enabled it
print('-> Proportion of users who used OD of those who enabled it')
prop_test(
    trials = np.array(df['num_enabled']),
    successes = np.array(df['num_used'])
)

# Average number of days in OD 
print('-> Average number of days in OD')
props = np.array(df['sum_days']) / np.array(df['num_days'])

print(f"Control rate {props[0]:.2}")
print(f"Test rate {props[1]:.2}")
print(f"Lift {props[1]/props[0] - 1:.2%}")

# Proportion who enabled or used OD within 30 days of activation by credit score quintile
# Note: the base is consumers who were in the experiment for at least 30 days

df = pd.read_csv('prop_enabled_or_used_by_30d_by_cs.csv')

for i in range(1,6):
    print('-------------------------------')
    print(f'For credit score quantile: {i}')
    print('-------------------------------')
    print('-> Proportion of users who enabled OD')
    prop_test(
        trials = np.array(df[df['credit_score_quintile_d0']== i]['num_exposed']),
        successes = np.array(df[df['credit_score_quintile_d0']== i]['num_enabled'])
    )
    print('-> Proportion of users who used OD')
    prop_test(
        trials = np.array(df[df['credit_score_quintile_d0']== i]['num_exposed']),
        successes = np.array(df[df['credit_score_quintile_d0']== i]['num_used'])
    )
    print('-> Proportion of users who used OD of those who enabled it')
    prop_test(
        trials = np.array(df[df['credit_score_quintile_d0']== i]['num_enabled']),
        successes = np.array(df[df['credit_score_quintile_d0']== i]['num_used'])
    )
    print('-> Average number of days in OD')
    props = np.array(df[df['credit_score_quintile_d0']== i]['sum_days']) / np.array(df[df['credit_score_quintile_d0']== i]['num_days'])

    print(f"Control rate {props[0]:.2}")
    print(f"Test rate {props[1]:.2}")
    print(f"Lift {props[1]/props[0] - 1:.2%}")


def test_lift(trials, successes):
    
    props = successes / trials

    res = pd.DataFrame({"Lift": [props[1]/props[0]- 1]})

    return res

# Lift in Proportion of users who enabled OD

lift_table = pd.DataFrame(columns = ["Lift", "Credit score quintile"])

for i in range(1,6):
    res["Lift"] = test_lift(
                    trials = np.array(df[df['credit_score_quintile_d0']== i]['num_exposed']),
                    successes = np.array(df[df['credit_score_quintile_d0']== i]['num_enabled'])
                    )
    res["Credit score quintile"] = i
    res["Metric"] = "Enabling OD within 30 days"

    lift_table = lift_table.append(res)

# Lift in Proportion of users who used OD of those who enabled it

for i in range(1,6):
    res["Lift"] = test_lift(
                    trials = np.array(df[df['credit_score_quintile_d0']== i]['num_enabled']),
                    successes = np.array(df[df['credit_score_quintile_d0']== i]['num_used'])
                    )
    res["Credit score quintile"] = i
    res["Metric"] = "Usage for those who enable OD"

    lift_table = lift_table.append(res)

sns.set(rc={'figure.figsize':(9,6)})
sns.set_style("ticks")
ax = sns.barplot(x="Credit score quintile",
                 y="Lift",
                 hue="Metric",
                 data=lift_table)
ax.figure.savefig("test_lift.png")

tdf = df[df["variant_id"]=="disabled"][["credit_score_quintile_d0", "num_enabled", "num_used"]]

tdf = tdf.rename(columns={"credit_score_quintile_d0":"Credit score quintile",
                          "num_enabled":"Enabled OD",
                          "num_used": "Used OD"})

tdf = pd.melt(tdf, id_vars="Credit score quintile", 
                   value_vars=["Enabled OD", "Used OD"],
                   value_name="Users in control group")

sns.set(rc={'figure.figsize':(9,6)})
sns.set_style("ticks")
ax = sns.barplot(x="Credit score quintile",
                 y="Users in control group", 
                 hue="variable", 
                 data=tdf)
ax.figure.savefig("control_count.png")