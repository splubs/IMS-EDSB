# Project brief — Telco Customer Churn: Retention Management

## Stakeholder and decision
Stakeholder: Head of Customer Retention. Decision: which existing customers to contact
first under a limited retention budget, conditional on a properly timed risk estimate.

## Course-defined analytical task
- Population: `Customer Status` in {Churned, Stayed}. Do not model Joined.
- Label: Churned=1, Stayed=0.
- Evaluation: customer-level stratified holdout.
- Grain: one record per `Customer ID` after joining five supplied workbooks.

## Working questions
1. Which explainable customer attributes are associated with churn?
2. Which approach ranks churn cases best on held-out records?
3. For a fixed contact capacity (illustrative assumption: top 10%), how many churn
   cases appear among customers with the highest estimated risk?
4. How sensitive are priorities to feature assumptions and contact budget?

## Important limitations
- The only timestamp is Q3 without a calendar year. No history of pre-churn features.
- End-of-quarter features may encode churn outcome or later interactions.
- Churn scores only capture risk association; they do not establish who can be saved.
- CLTV is a previously modeled value and its method and timing are not documented.
- No information on actual retention offer cost, treatment effectiveness or uplift.
- Impact/ROI must be framed as an explicitly hypothetical scenario, not observed savings.

## Modeling extension after audit
Compare logistic regression with a justified tree-based method, on fixed splits.
Choose models and intervention thresholds using training/validation only;
consult the holdout once after finalizing the design. Add PR-AUC, ROC-AUC,
calibration, lift@budget and precision/recall@budget.

## Source
`references/project_guide.pdf`: university project guide. The README and baseline
are additional starter materials, not mandatory deliverables stated by the guide.
