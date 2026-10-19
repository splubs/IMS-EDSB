# Initial data audit — confirmed against supplied workbooks

- Four customer-level workbooks have 7,043 unique Customer IDs each.
- Population contains 1,671 distinct ZIP codes, joined through `Zip Code`.
- Customer-level join returns 7,043 rows, preserving the intended grain.
- Outcomes: Stayed=4,720; Churned=1,869; Joined=454.
- Core analytic sample: 6,589 rows; churn prevalence = 1,869 / 6,589 = 28.37%.
- Literal `None` must be preserved (`Offer`: 3,877; `Internet Type`: 1,526).
- `Churn Category` and `Churn Reason` are empty for all 4,720 stayed customers,
  and are outcome-derived, not usable as predictor features.
- `Satisfaction Score` strongly separates outcomes: score 1/2 occurs only among
  churned, score 4/5 occurs only among stayed; this is a significant timing risk.
- Additional questions: when are billing, tenure, status and satisfaction measured
  relative to churn? Is any field truly available at targeting time?

To regenerate checks: `python -m src.data` and `python -m unittest discover`.
