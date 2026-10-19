"""Baseline-only model inputs; no status-derived predictors or post-churn data."""
import pandas as pd

NUMERIC = [
    'Age','Number of Dependents','Number of Referrals','Tenure in Months',
    'Avg Monthly Long Distance Charges','Avg Monthly GB Download','Monthly Charge',
]
CATEGORICAL = [
    'Gender','Married','Phone Service','Multiple Lines','Internet Service',
    'Internet Type','Online Security','Online Backup','Device Protection Plan',
    'Premium Tech Support','Streaming TV','Streaming Movies','Streaming Music',
    'Unlimited Data','Contract','Paperless Billing','Payment Method',
]
FEATURES = NUMERIC + CATEGORICAL
FORBIDDEN = {'Customer ID','Customer Status','Churn Value','Churn Label',
             'Churn Score','Churn Category','Churn Reason','Satisfaction Score','CLTV'}
assert not (set(FEATURES) & FORBIDDEN)


def make_xy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return explainable candidate predictors X and binary churn target y."""
    if not df['Customer Status'].isin(['Stayed','Churned']).all():
        raise ValueError('The core population must exclude Joined')
    x = df[FEATURES].copy()
    y = df['Customer Status'].eq('Churned').astype(int)
    return x,y
