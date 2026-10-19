"""Illustrative baseline; not yet a validated intervention recommendation."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score, brier_score_loss
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.data import ROOT, load_core_population
from src.features import NUMERIC, CATEGORICAL, make_xy


def metrics(y_true, risks, budget_fraction=0.10):
    """Ranking metrics and how many churn cases occur among the highest-risk 10%."""
    y = np.asarray(y_true, dtype=int)
    p = np.asarray(risks, dtype=float)
    n = max(1, int(np.ceil(len(y)*budget_fraction)))
    selected = np.argsort(-p,kind='stable')[:n]
    base_rate = float(y.mean())
    precision_at_budget = float(y[selected].mean())
    return {'n_customers':int(len(y)),'prevalence':base_rate,
            'pr_auc':float(average_precision_score(y,p)),
            'roc_auc':float(roc_auc_score(y,p)),
            'brier_score':float(brier_score_loss(y,p)),
            'selected_top10pct':n,
            'precision_at_top10pct':precision_at_budget,
            'recall_at_top10pct':float(y[selected].sum()/y.sum()),
            'lift_at_top10pct':float(precision_at_budget/base_rate)}


def main():
    """Train on training rows; reserve test metrics until explicitly unlocked."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evaluate-holdout',action='store_true',
                        help='Use only once after finalizing feature/model/decision choices')
    args = parser.parse_args()
    data = load_core_population()
    x,y = make_xy(data)
    indices = np.arange(len(x))
    development, test = train_test_split(indices, test_size=.20, random_state=42, stratify=y)
    train, val = train_test_split(development, test_size=.25, random_state=42,
                                stratify=y.iloc[development])
    preprocess = ColumnTransformer([
        ('number',Pipeline([('impute',SimpleImputer(strategy='median')),
                           ('scale',StandardScaler())]),NUMERIC),
        ('category',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),
                             ('onehot',OneHotEncoder(handle_unknown='ignore'))]),CATEGORICAL)])
    model = Pipeline([('preprocess',preprocess),('model',LogisticRegression(max_iter=2000))])
    model.fit(x.iloc[train],y.iloc[train])
    val_risk = model.predict_proba(x.iloc[val])[:,1]
    val_metrics = metrics(y.iloc[val],val_risk)
    output = ROOT/'reports'/'generated'
    output.mkdir(parents=True,exist_ok=True)
    result={'design':'stratified 60/20/20 train/validation/test; seed 42',
            'caution':'single end-of-quarter snapshot; no forward-looking validation; not causal',
            'train_size':int(len(train)), 'validation_size':int(len(val)),
            'reserved_holdout_size':int(len(test)),'validation':val_metrics}
    if args.evaluate_holdout:
        # Run ONLY after development choices have been frozen. Do not select
        # models or thresholds based on these numbers.
        test_risk = model.predict_proba(x.iloc[test])[:,1]
        result['test'] = metrics(y.iloc[test],test_risk)
        pd.DataFrame({'Customer ID':data.iloc[test]['Customer ID'].to_numpy(),
                      'actual_churn':y.iloc[test].to_numpy(),
                      'predicted_risk':test_risk}).sort_values('predicted_risk',ascending=False).to_csv(
            output/'baseline_holdout_scores.csv',index=False)
    else:
        print('Holdout reservado: não foi avaliado. Opção --evaluate-holdout apenas na fase final.')
    (output/'baseline_metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    print('Outputs in reports/generated/ (ignored by Git)')


if __name__ == '__main__':
    main()
