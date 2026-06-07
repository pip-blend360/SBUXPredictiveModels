# Human - Iteration 1

**Human** Pip Courbois
**Date** 2026-06-07

## Review
* 

# Review - Iteration 1

**Reviewer:** Data Science Principal (Peer Review)
**Date:** 2026-06-06

## Review Summary

This is a well-structured and comprehensive technical specification that successfully expands and clarifies the original predictive models document. The document demonstrates strong technical rigor with clear mathematical formulations, detailed evaluation frameworks, and practical implementation guidance. The hybrid State-based LTV approach is well-articulated and justified. However, there are several areas requiring clarification or expansion before final approval, particularly around model complexity justification, feature drift handling, and some technical details in the transition probability model.

## Technical Strengths

- **Strong conceptual framework**: The hybrid State-based LTV approach (combining State-level values with customer-level transition probabilities) is well-explained and technically sound. The rationale for this approach vs. direct individual LTV prediction is clear.

- **Comprehensive evaluation framework**: Section 8 provides excellent detail on evaluation metrics with specific targets. The distinction between customer-level and State-level accuracy requirements (15% vs 10% MAPE) is appropriate and well-justified.

- **Practical feature engineering**: The feature engineering section (7.2) effectively incorporates insights from the June 2026 analysis (Monetary + Recency achieving R² = 0.57), and correctly notes that consistency metrics add minimal value.

- **Clear use cases**: Section 10 provides concrete, actionable use cases with specific examples and ROI calculations. The churn prevention example is particularly strong.

- **Appropriate time-series methodology**: Section 7.3 correctly emphasizes forward-looking validation and time-series cross-validation to prevent data leakage.

- **Good MLOps coverage**: Section 9.3 addresses model monitoring, drift detection, and retraining triggers with appropriate specificity.

## Technical Concerns / Suggestions

### Critical Issues

**C1. Model Complexity Justification (Section 5.1)**

The document proposes a hybrid State-based framework that combines State-level values with customer-level transition probabilities. While the approach is sound, the justification could be stronger:

- **Concern**: The complexity of maintaining two separate models (State values + transition probabilities) plus the combination logic needs stronger justification against simpler alternatives.
- **Suggestion**: Add a subsection explicitly comparing:
  1. Direct customer-level LTV regression (simplest)
  2. State-average-based prediction (simple but limited)
  3. Proposed hybrid approach (moderate complexity)

  Include estimated performance differences and complexity costs. The current document asserts the hybrid approach is better but doesn't quantify the trade-off.

**C2. State Definition Stability Assumption (Section 5.1.4)**

The framework assumes "State values remain relatively stable over time (requires monitoring)" but doesn't specify:

- **Concern**: How stable is "stable enough"? What happens if State values drift significantly due to external factors (economy, competition, seasonal programs)?
- **Suggestion**:
  1. Define acceptable State value variance thresholds (e.g., ±15% month-to-month)
  2. Specify monitoring frequency for State value recalculation
  3. Describe the recalibration process when drift is detected
  4. Consider whether State values should be time-varying inputs to the model

**C3. Transition Probability Time Horizon Mismatch (Section 5.2)**

There's a potential inconsistency in time horizons:

- **Issue**: Transition probabilities are estimated over a 30-day window (Section 5.2), but LTV predictions are for 90-day or 365-day horizons (Section 5.1).
- **Concern**: The formula `LTV_i = Σ_j (P_ij × Value(S_j))` uses 30-day transition probabilities combined with long-term State values. This implicitly assumes customers transition once and stay in the new State for the remainder of the horizon.
- **Suggestion**:
  1. Clarify whether the LTV calculation uses a single-step transition or multi-step Markov chain
  2. If single-step: explain why this approximation is acceptable
  3. If multi-step: provide the full recursive formulation or matrix exponentiation approach
  4. Consider: `LTV_90d = Σ_(k=0 to 3) P^k × V` where P^k is k-step transition probability

### Major Issues

**M1. Feature Drift and Seasonal Adjustment (Section 7.2)**

- **Concern**: The document mentions "seasonal adjustment factors" for State-level values but doesn't specify how seasonality is handled in customer-level features.
- **Suggestion**: Add a subsection on temporal feature engineering:
  1. How are features normalized for seasonality? (e.g., revenue compared to weekly/monthly average)
  2. Should models include explicit seasonal indicators (month, quarter)?
  3. How is holiday impact handled?

  Example: A customer's frequency might drop in summer due to travel, but this shouldn't signal churn risk.

**M2. New vs. Reactivated State Handling (Section 4.2)**

- **Concern**: "New & Reactivated" lumps together two very different customer types (truly new vs. previously lapsed returning). The document shows this State has high uncertainty (45% stay, but outcomes vary widely).
- **Suggestion**:
  1. Consider splitting into two separate States, or
  2. Add a feature distinguishing new vs. reactivated within the State, or
  3. Provide analysis showing these groups have similar transition dynamics (if that's the case)

**M3. Class Imbalance Handling Details (Section 7.3)**

- **Concern**: Section 7.3 mentions oversampling rare transitions, but this can introduce bias and overfitting in transition probability models.
- **Suggestion**:
  1. Specify which transitions are considered "rare but important" (threshold?)
  2. Recommend class weighting over oversampling to avoid duplicating training examples
  3. Add validation approach to ensure oversampling doesn't degrade calibration
  4. Consider: Train model with class weights, then post-hoc calibrate probabilities

**M4. Transition Matrix Stationarity Assumption (Section 5.2)**

- **Concern**: The model assumes transition dynamics are consistent over time. However, business interventions (new loyalty program, major marketing campaigns) could fundamentally change transition rates.
- **Suggestion**:
  1. Add discussion of when the stationarity assumption is violated
  2. Propose intervention-aware modeling (e.g., separate transition matrices for treated vs. control groups)
  3. Specify how to detect when transition dynamics have permanently shifted

**M5. Cold Start Problem (Section 5.2)**

- **Concern**: New customers (especially in "New & Reactivated" State) have limited historical data for feature calculation. How are transition probabilities estimated for customers with <30 days of history?
- **Suggestion**:
  1. Specify minimum data requirements for prediction
  2. Define fallback strategy (use State-level average? broader cohort average?)
  3. Add confidence intervals that widen for sparse-data customers

### Minor Issues

**m1. Missing Model Serving Latency Justification (Section 9.1)**

- The document specifies <100ms p99 latency for model serving (Phase 2) but doesn't justify why this is necessary for a customer value prediction use case.
- Suggest: Either justify the requirement or relax to <500ms if real-time decisioning isn't needed.

**m2. Baseline Model Specification (Section 7.4)**

- The baseline is described as "Current State average × simple persistence rate" but "simple persistence rate" is not defined.
- Suggest: Specify exactly how persistence rate is calculated (historical % staying in State? exponential decay?)

**m3. Sparse State Transitions (Section 5.2, Appendix C)**

- Appendix C shows some transitions are extremely rare (e.g., Unengaged → Most Valuable = 0%).
- Suggest: Clarify whether zero-probability transitions are hard-coded or if the model can still assign small non-zero probabilities based on individual features.

**m4. A/B Testing Details (Section 9.3)**

- "Route 10% traffic to new model" is mentioned but the mechanism isn't clear for a batch scoring system.
- Suggest: Clarify this means scoring 10% of customers with both models and comparing predictions (not routing traffic in the inference sense).

**m5. Feature Importance Appendix (Appendix B)**

- Table shows R² contributions but these appear to be incremental (conditional on previous features).
- Suggest: Clarify whether these are marginal contributions or individual feature importance values.

**m6. Risk Register Severity Scoring (Appendix E)**

- Impact and Likelihood are High/Medium/Low but no overall risk priority is calculated.
- Suggest: Add risk priority score (e.g., High Impact + High Likelihood = Critical priority).

### Clarity / Presentation Issues

**p1. Notation Consistency**

- Section 5.1 uses `LTV_i(H)` but later sections drop the (H) and use `LTV_i`.
- The same applies to `Value(S_j, H)`.
- Suggest: Maintain consistent notation or explicitly state when dropping the horizon parameter.

**p2. Executive Summary LTV Formula**

- The Executive Summary states: "Expected customer LTV = sum of (transition probabilities × State values)"
- This is accurate for the short-term but may confuse readers expecting a full horizon calculation.
- Suggest: Add a note: "over a short-term transition window; see Section 5.1 for full horizon methodology"

**p3. Missing Diagram Descriptions**

- Section 6 mentions "Include diagrams or visual representations where helpful (describe them in markdown)" but no diagram descriptions are included.
- Suggest: Add at least one diagram description, such as:
  - Data flow architecture (sources → features → models → outputs → activation)
  - Transition probability visualization
  - LTV calculation workflow

**p4. Acronym First Use**

- "ECE" is used in Appendix D table before being defined (Expected Calibration Error first appears in Section 8.2).
- Suggest: Define acronyms on first use or add an acronym table to the Glossary.

## Recommendations for Enhancement (Optional)

These are not blockers but would strengthen the document:

**E1. Model Interpretability**
- Add a subsection on model explainability (SHAP values, feature importance visualization)
- Specify how to explain predictions to business stakeholders (e.g., "Your churn risk increased because your visit frequency dropped 40%")

**E2. Intervention Modeling**
- Consider extending the framework to model counterfactual scenarios: "If we send this offer, how does P_ij change?"
- This would enable ROI optimization beyond the current descriptive approach

**E3. Multi-Market Considerations**
- The document is US-focused (implied by Section 2 scope). Add a subsection on how the framework would extend to international markets (separate models? market-specific State definitions?)

**E4. Model Fairness / Bias**
- Add a brief discussion of potential biases (e.g., are certain customer segments systematically over/under-predicted?)
- Specify fairness metrics to monitor (equity of error rates across segments)

**E5. Confidence Intervals**
- The current specification provides point estimates. Consider adding prediction intervals (e.g., 80% confidence interval for customer LTV)
- This would help business users understand uncertainty

**E6. Real-World Validation Examples**
- Include 1-2 examples of actual prediction outputs on real (anonymized) customer examples
- Show the inputs, model calculations, and final predictions to make the framework concrete

## Decision

**REVIEWER STATUS: NEEDS REVISION**

Please address the **Critical** and **Major** issues listed above before final approval. Specifically:

**Must Address:**
1. **C1**: Strengthen justification for hybrid approach vs. simpler alternatives
2. **C2**: Define State value stability thresholds and monitoring
3. **C3**: Clarify time horizon handling in LTV calculation
4. **M1**: Add seasonality handling details
5. **M3**: Revise class imbalance approach (avoid oversampling)
6. **M5**: Define cold start handling strategy

**Should Address:**
- M2 (New vs. Reactivated distinction)
- M4 (intervention handling)
- Minor issues m1-m6
- Presentation issues p1-p4

**Optional Enhancements:**
- E1-E6 would significantly strengthen the document but are not required for approval

---

**Overall Assessment**: This is strong foundational work that demonstrates deep technical understanding and practical insight. With the revisions above, this will be an excellent technical specification that can guide successful implementation.

**Estimated Revision Effort**: 4-6 hours to address critical and major issues; 2-3 hours for minor/presentation issues.

**Next Steps**: Writer agent should revise the document addressing the above feedback, particularly focusing on the Critical and Major issues.
