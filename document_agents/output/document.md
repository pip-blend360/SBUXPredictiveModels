# Predictive Models for Customer States
## Technical Specification

**Version:** 2.0
**Date:** June 2026
**Status:** Draft for Review  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Introduction](#introduction)
3. [Business Context and Value](#business-context-and-value)
4. [Customer States Framework Overview](#customer-states-framework-overview)
5. [Proposed Predictive Models](#proposed-predictive-models)
6. [Technical Architecture](#technical-architecture)
7. [Model Development Approach](#model-development-approach)
8. [Evaluation Framework](#evaluation-framework)
9. [Implementation Requirements](#implementation-requirements)
10. [Use Cases and Applications](#use-cases-and-applications)
11. [Timeline and Milestones](#timeline-and-milestones)
12. [Appendix](#appendix)

---

## Executive Summary

This document specifies a predictive intelligence layer for Starbucks Customer States that transforms customer understanding from descriptive to predictive, enabling forward-looking business decisions.

### What We're Building

Two interconnected predictive models:

1. **Lifetime Value (LTV) Model** - Forecasts expected future value of each customer over a defined planning horizon
2. **State Transition-Probability Model** - Estimates likelihood of customer migration between States

### Why It Matters

These models will enable the business to:
- Forecast future customer value and portfolio movement with 5-10% accuracy at State level
- Identify customers at risk of decline or churn before it happens
- Prioritize retention and growth investments based on predicted ROI
- Support data-driven targeting, experimentation, and resource allocation

### How It Works

The framework combines State-level economics with customer-level transition probabilities:
- Each Customer State has an associated average future value
- Each customer has a probability distribution for transitioning between States
- Expected customer LTV = sum of (transition probabilities × State values)
- This approach reduces variance while maintaining predictive power

### Key Innovation

Rather than predicting individual customer LTV directly (high variance), we:
1. Estimate stable State-level average values
2. Predict customer-level transition probabilities
3. Combine them for customer-level expected values

This produces forecasts that are more stable, interpretable, and aligned with how the business actually manages customers.

---

## Introduction

### Background

Customer States provide a shared framework for understanding customer value and engagement across Starbucks. The framework segments customers based on:
- **Value Signals**: Monetary value and recency of engagement
- **Behavioral Signals**: Starbucks Rewards usage, product preferences, and channel behavior

Customer States currently serve as a descriptive tool. This initiative extends States into a **predictive decision system**.

### Objectives

Transform Customer States from "what customers are doing" to "what customers will likely do" by:

1. **Quantifying Future Value**: Estimate expected value contribution over planning horizons (e.g., 90-day, 365-day)
2. **Predicting State Dynamics**: Model customer migration patterns between States
3. **Enabling Intervention**: Identify highest-value opportunities for retention and growth
4. **Supporting Planning**: Provide State-level forecasts for portfolio management

### Scope

**In Scope:**
- Predictive models for Lifetime Value and State transitions
- Customer-level and State-level prediction outputs
- Integration with existing Customer States definitions
- Model evaluation and monitoring framework
- Analytical and operational activation pathways

**Out of Scope (Phase 1):**
- Real-time scoring infrastructure
- Automated decisioning systems
- Multi-year LTV predictions
- Causal inference for intervention effects
- International market expansion

---

## Business Context and Value

### Strategic Alignment

The predictive models support three strategic priorities:

1. **Growth**: Identify customers with highest expansion potential
2. **Retention**: Detect decline risk early and intervene effectively
3. **Efficiency**: Optimize marketing spend and customer investment ROI

### Use Cases by Stakeholder

| Stakeholder | Use Case | Value |
|------------|----------|-------|
| **Marketing** | Prioritize retention offers to high-risk, high-value customers | Reduce churn in top segments |
| **Product** | Identify customers likely to expand category adoption | Increase basket size and frequency |
| **Loyalty** | Forecast Stars Rewards redemption and value impact | Optimize rewards program economics |
| **Finance** | Predict customer portfolio value for planning | Improve revenue forecasting accuracy |
| **Analytics** | Measure campaign effectiveness via State transitions | Quantify marketing ROI |
| **Store Ops** | Understand future demand patterns by customer segment | Optimize staffing and inventory |

### Success Metrics

**Model Performance:**
- State-level value forecast error within 5-10% (MAPE)
- Customer-level predictions statistically better than baseline heuristics
- Transition probability matrices remain stable across scoring windows

**Business Impact:**
- Improved customer retention rate in targeted segments
- Increased campaign ROI through better targeting
- More accurate quarterly revenue forecasts
- Measurable lift in State-to-State transition rates from interventions

---

## Customer States Framework Overview

### State Definitions

Customer States segment the base using five key dimensions:

#### Value Signals (Foundation)
- **Monetary**: Average monthly net revenue over lookback window
- **Recency**: Days since last transaction

#### Behavioral Signals
- **SR & Discount Engagement**: Stars usage, redemption, loyalty tier activity
- **Product Preferences**: Category depth, product exploration, daypart preferences
- **Channel Behavior**: Mobile Order & Pay, drive-through, café usage patterns

### State Hierarchy

**High-Level States (6):**
1. **Most Valuable** - Highest frequency, spend, and engagement across all dimensions
2. **Stable** - Consistent purchasers with strong category engagement
3. **New & Reactivated** - Recent starters/returners with developing patterns
4. **Declining** - Previously consistent customers whose frequency is dropping
5. **Lapsing** - Low recent activity, at risk of full disengagement
6. **Unengaged** - No meaningful engagement in current period

**Detailed States (~20):**
Each high-level State subdivides based on behavioral signal combinations, creating actionable micro-segments for targeting.

### State Characteristics

From the June 2026 framework analysis:

| State | Monetary | Recency | SR Engagement | Product Depth | Channel | Population | Avg. Frequency |
|-------|----------|---------|---------------|---------------|---------|------------|----------------|
| Most Valuable | Highest | Highest | Highest | Highest | Highest | 2.1% | >4 txns/week |
| Stable | High | High | High | High | High | 10.6% | 2.2 txns/week |
| New & Reactivated | Low | High | Medium | Medium | Medium | 11.2% | 1.5 txns/week |
| Declining | Medium | Medium | Low | Low | Low | - | Decreasing |
| Lapsing | Low | Low | Low | Low | Low | - | <0.5 txns/week |

### State Value Drivers

**RFMC Analysis** (June 2026 data):
- Monetary value alone explains ~54% of future 90-day revenue (R²)
- Adding Recency increases explanatory power to 57%
- Behavioral features (SR, Product, Channel) add incremental 3-5% lift
- Consistency metrics (transaction regularity) provide minimal additional value

**Behavioral Insights:**
- **Channel**: Drive-through customers have ~10% higher average order value than café
- **Daypart**: Mid-morning (9-11am) transactions show highest revenue per ticket
- **SR Tier**: Correlation with value, but largely redundant with frequency

---

## Proposed Predictive Models

### Model 1: Lifetime Value (LTV)

#### Definition

For each customer *i*, estimate expected future value over a planning horizon *H*:

```
LTV_i(H) = E[Revenue_i | t, t+H]
```

Where:
- *H* = planning horizon (e.g., 90 days, 365 days)
- *t* = current time/scoring date
- Revenue includes net discounted revenue (after Stars redemptions, discounts)

#### Estimation Approach

**Hybrid State-Based Framework:**

Rather than predicting individual LTV directly, we:

1. **Define State-Level Average Values**
   Each State *j* has expected average future value over horizon *H*:

   ```
   Value(S_j, H) = AVG(FutureRevenue_H | Current State = S_j)
   ```

2. **Predict Customer Transition Probabilities**
   For customer *i* currently in State *k*, estimate probability of transitioning to each State *j* over short-term window (e.g., 30 days):

   ```
   P_ij = P(Customer_i → State_j | current features)
   ```

3. **Calculate Expected Customer Value**
   Combine transition probabilities with State values:

   ```
   ExpectedLTV_i = Σ_j (P_ij × Value(S_j))
   ```

4. **Optional Customer-Level Adjustment**
   Add residual term for within-State variation:

   ```
   LTV_i = ExpectedLTV_i + β × CustomerFeatures_i
   ```

#### Why This Approach?

**Benefits:**
- **Reduces Variance**: State-level values are stable; only transition probabilities vary by customer
- **Improves Interpretability**: Predictions directly linked to Customer States framework
- **Enables Scenario Analysis**: Can model "what-if" State transitions for intervention planning
- **Aligns with Business Process**: Matches how strategies are executed (State-based programs)

**Trade-offs:**
- Assumes State values remain relatively stable over time (requires monitoring)
- Customer-level predictions constrained by State structure (less personalization)

#### Model Features

**For State-Level Value Estimation:**
- Historical average revenue by State
- State persistence/retention rates
- Distribution of customer values within State
- Seasonal adjustment factors

**For Transition Probability Prediction:**

*Value Signals:*
- Recent monetary value (vs. State average)
- Recency trend (increasing/decreasing days between visits)
- Momentum (change in frequency over rolling windows)

*Behavioral Signals:*
- Stars earned and redeemed (recent activity)
- Category exploration (new product trials)
- Channel diversity (number of channels used)
- Daypart shifts (changes in visit timing)
- Promotion responsiveness

*Customer Context:*
- Tenure/lifecycle stage
- Geographic market characteristics
- Seasonality patterns

### Model 2: State Transition Probabilities

#### Definition

For customer *i* currently in State *s*, predict probability distribution over all States after time window *Δt*:

```
P(State_{t+Δt} = j | State_t = s, Features_i)  for all j ∈ States
```

Where:
- *Δt* = transition window (e.g., 30 days - actionable time horizon)
- Output is probability vector summing to 1.0

#### Estimation Approach

**Multi-Class Classification with Ordinal Structure:**

1. **Training Data Construction**
   - Observation window: *t-180 to t* (6 months of feature calculation)
   - Outcome window: *t to t+30* (next 30 days)
   - Label: State assignment at *t+30*

2. **Model Architecture**
   Options (to be evaluated):
   - Softmax regression (baseline)
   - Gradient boosted trees (XGBoost, LightGBM)
   - Neural network with ordinal loss function
   - Mixture of per-State binary classifiers

3. **Ordinal Constraints**
   Encode State ordering (Most Valuable → Unengaged) to:
   - Penalize large jumps more than adjacent transitions
   - Smooth probability distributions
   - Improve stability

4. **Rare Transition Handling**
   - Force very rare transitions (e.g., Lapsing → Most Valuable) to zero probability
   - Prevents unstable predictions from sparse data

5. **Calibration**
   Post-process probabilities to ensure:
   - Aggregate predictions match observed transition rates
   - Within-State probability distributions well-calibrated

#### Model Features

**Same feature set as LTV prediction** (see above), plus:
- Current State assignment
- Time in current State (State persistence)
- State history (previous State, number of State changes)
- Distance from State centroid (how typical customer is for their State)

#### Transition Matrix Structure

Output for State *s*:

| From → To | Most Valuable | Stable | New & Reactivated | Declining | Lapsing | Unengaged |
|-----------|---------------|--------|-------------------|-----------|---------|-----------|
| **Most Valuable** | P_MM (high) | P_MS | P_MN (rare) | P_MD (rare) | ... | P_MU (very rare) |
| **Stable** | P_SM | P_SS (high) | P_SN | P_SD | ... | P_SU (rare) |
| ... | ... | ... | ... | ... | ... | ... |

**Properties:**
- Diagonal elements (stay in State) should be largest
- Adjacent transitions more likely than jumps
- Matrix should be relatively stable across scoring periods

---

## Technical Architecture

### Data Foundation

#### Data Sources

| Source | Data Type | Usage |
|--------|-----------|-------|
| **Transaction System** | Purchase history, order details | RFMC features, spend calculations |
| **Starbucks Rewards** | Stars earned/redeemed, tier status, offers | SR engagement features |
| **Customer Analytics ID** | Unified customer identity | Cross-platform tracking |
| **Product Master** | Category, product attributes | Product preference features |
| **Location Data** | Store type, geography | Contextual features |
| **Marketing** | Campaign exposure, responses | Promotion engagement |

#### Feature Store Requirements

- **Granularity**: Customer-Observation-Date level
- **Update Frequency**: Daily for operational use; weekly for model development
- **Lookback Windows**: 30-day, 90-day, 180-day, 365-day rolling features
- **Latency**: T+1 day for analytical use; near-real-time for activation

#### State Assignment Process

Current State assignment logic (from June 2026 methodology):

1. **Calculate RFMC Features**
   - Monetary: Log(avg monthly revenue over 180 days)
   - Recency: Days since last transaction

2. **Calculate Behavioral Features**
   - SR Score: Weighted combination of Stars usage features
   - Product Depth: Number of distinct categories purchased
   - Channel Diversity: Number of channels used

3. **Apply State Rules**
   - If (Monetary = Highest) AND (Recency = Highest) → "Most Valuable"
   - If (Monetary = High) AND (Recency = High) → "Stable"
   - ... [Rule set to be formalized]

4. **Assign Detailed State**
   - Within high-level State, apply behavioral thresholds

### Model Development Platform

**Environment**: Databricks
- Feature engineering: Spark SQL, PySpark
- Model training: scikit-learn, XGBoost, TensorFlow
- Experiment tracking: MLflow
- Model registry: Databricks ML Registry

**Development Workflow**:
1. Data extraction and feature engineering (Spark jobs)
2. Train/validation/test split (time-based)
3. Hyperparameter tuning (Hyperopt or Optuna)
4. Model evaluation and comparison
5. Model registration and versioning

### Deployment Architecture

**Phase 1 (MVP)**: Batch Scoring
- Daily/weekly batch jobs in Databricks
- Output: Scored customer table in Delta Lake
- Accessible via SQL for analytical consumption

**Phase 2 (Operational)**: Near-Real-Time
- Model serving via Databricks Model Serving or SageMaker
- Feature computation pipeline with low latency
- Integration with activation platforms (Adobe, CRM)

### Integration Points

#### Analytical Outputs

```
scored_customers_daily
├── customer_id (Analytical ID)
├── score_date
├── current_state
├── ltv_90day (predicted)
├── ltv_365day (predicted)
├── transition_probs (JSON: {state: probability})
├── risk_segment (High/Medium/Low churn risk)
├── opportunity_segment (High/Medium/Low growth potential)
└── model_version
```

#### Operational Activation

- **Adobe Journey Optimizer**: Customer segments based on predictions
- **Offer Management**: Targeted offer eligibility
- **Reporting**: State-level aggregates for dashboards

---

## Model Development Approach

### Development Phases

#### Phase 1: Foundation (Month 1-2)

**Objectives:**
- Finalize State definitions and assignment logic
- Complete feature engineering and validation
- Establish baseline performance benchmarks

**Deliverables:**
- Stable State assignment algorithm
- Curated feature dataset
- Baseline model performance (simple heuristics)

#### Phase 2: Model Development (Month 2-3)

**Objectives:**
- Develop and evaluate candidate models
- Optimize hyperparameters
- Select final model architectures

**Deliverables:**
- Trained LTV model
- Trained transition probability model
- Model evaluation reports

**Approach:**

1. **Baseline Models** (Simple Heuristics)
   - LTV: Current State average × persistence probability
   - Transitions: Historical State-to-State rates

2. **Intermediate Models**
   - LTV: Linear regression on RFMC features
   - Transitions: Logistic regression per State

3. **Advanced Models**
   - LTV: Gradient boosted trees with State-based framework
   - Transitions: Multi-class XGBoost with ordinal constraints

4. **Model Selection**
   - Compare on hold-out test set (forward-looking data)
   - Prioritize stability and interpretability over marginal accuracy gains

#### Phase 3: Evaluation and Iteration (Month 3-4)

**Objectives:**
- Validate model performance on out-of-time data
- Assess longitudinal stability
- Refine based on stakeholder feedback

**Deliverables:**
- Validated model performance metrics
- Stability analysis across time windows
- Stakeholder readiness assessment

#### Phase 4: Deployment Preparation (Month 4-5)

**Objectives:**
- Build scoring pipeline
- Integrate with downstream systems
- Establish monitoring framework

**Deliverables:**
- Production-ready scoring code
- Integration with activation platforms
- Monitoring dashboards

### Feature Engineering

#### RFMC Features (Value Foundation)

From June 2026 analysis, the optimal RFMC combination is:
- **Monetary + Recency** (R² = 0.57 for 90-day revenue prediction)

**Implementation:**

```python
# Monetary (90-day lookback)
avg_monthly_revenue_90d = SUM(net_revenue) / 3  # Log-transformed

# Recency
days_since_last_purchase = DATEDIFF(score_date, MAX(transaction_date))

# Additional candidates
transaction_frequency_90d = COUNT(DISTINCT transaction_date)
avg_order_value_90d = SUM(net_revenue) / COUNT(transactions)
```

**Why not Consistency?**
Testing showed consistency metrics (entropy, coefficient of variation) added minimal predictive value (<1% R² gain) - not worth complexity.

#### Behavioral Features

**SR Engagement:**
```python
stars_earned_30d = SUM(stars_earned)
stars_redeemed_30d = SUM(stars_redeemed)
redemption_rate_90d = stars_redeemed / stars_earned  # Null-safe
loyalty_tier = CURRENT_VALUE(tier)  # Green/Gold/Reserve
```

**Product Preferences:**
```python
distinct_categories_90d = COUNT(DISTINCT product_category)
product_exploration_rate = COUNT(new_products_90d) / COUNT(total_transactions_90d)
avg_revenue_by_daypart = [avg for each daypart]  # Mid-morning typically highest
```

**Channel Behavior:**
```python
channel_diversity = COUNT(DISTINCT channel)  # MOP, drive-through, café
mop_frequency_30d = COUNT(transactions WHERE channel='MOP')
channel_shift_indicator = has_used_new_channel_recently  # Boolean
```

**Important Findings** (from June 2026 feature analysis):
- **Daypart**: Mid-morning (9-11am) has highest revenue per transaction
- **Channel**: Drive-through ~10% higher AOV than café
- **SR Tier**: Correlated with value but redundant with frequency in models

#### Temporal Features

```python
tenure_days = DATEDIFF(score_date, first_transaction_date)
days_in_current_state = DATEDIFF(score_date, state_entry_date)
```

#### Feature Preprocessing

- **Log transformations**: Monetary, frequency (reduce skew)
- **Standardization**: Z-score normalization for regression models
- **Null handling**: Median imputation for missingness <5%; drop feature if >20%
- **Outlier treatment**: Winsorize at 1st/99th percentile

### Training Methodology

#### Time-Based Splits

**Critical**: Use forward-looking validation to match deployment reality

```
Training:   [Jan 2025 ────────── Dec 2025]
Validation: [Jan 2026 ── Mar 2026]
Test:       [Apr 2026 ── May 2026]
```

**Observation vs. Outcome Windows:**
- Observation (features): 180-day lookback from split date
- Outcome (target): 30-90 days forward from split date
- Gap (optional): 0-7 days between observation and outcome

#### Cross-Validation

Given temporal nature, use **time-series cross-validation**:
- Roll forward by month
- 5-6 folds across 2025-2026
- Prevent data leakage from future to past

#### Handling Class Imbalance (Transition Model)

State distributions are imbalanced (e.g., 2% Most Valuable, 30% Unengaged).

**Strategies:**
- Stratified sampling by current State
- Class weights proportional to inverse frequency
- Oversample rare but important transitions (e.g., Stable → Most Valuable)

#### Regularization

- L2 regularization (Ridge) for linear models
- Tree depth limits and learning rate for GBMs
- Dropout for neural networks
- Prefer simpler models to reduce overfitting

### Model Comparison

Compare candidate models on:

1. **Accuracy Metrics** (see Evaluation Framework)
2. **Stability Metrics**: Performance consistency across folds
3. **Interpretability**: Feature importance, Shapley values
4. **Computational Cost**: Training time, inference latency
5. **Business Alignment**: Stakeholder feedback on outputs

**Selection Criteria:**
- Must beat baseline by statistically significant margin
- State-level aggregates should be well-calibrated
- Predictions should align with business intuition
- Model should be explainable to non-technical stakeholders

---

## Evaluation Framework

### LTV Model Evaluation

#### Accuracy Metrics

**Primary Metrics:**

1. **Mean Absolute Percent Error (MAPE)** - Interpretable, scale-invariant
   ```
   MAPE = (1/N) × Σ |Actual_i - Predicted_i| / Actual_i × 100%
   ```
   **Target**: <15% at customer level, <10% at State level

2. **Mean Absolute Error (MAE)** - Dollar impact
   ```
   MAE = (1/N) × Σ |Actual_i - Predicted_i|
   ```

3. **R-Squared** - Variance explained
   ```
   R² = 1 - (SS_residual / SS_total)
   ```
   **Target**: >0.55 (beating RFMC-only baseline of 0.57)

**Secondary Metrics:**
- **Rank-Order Correlation** (Spearman's ρ): Are high-value customers ranked correctly?
- **Decile Analysis**: MAPE by predicted value decile (ensure accuracy across spectrum)

#### Calibration

**State-Level Calibration**:
Aggregate predictions by State should match observed average:

```
For each State s:
  Predicted_Avg_s ≈ Actual_Avg_s  (within 5%)
```

**Calibration Plot**: Binned predicted vs. actual values should lie on diagonal

#### Stability Metrics

**Longitudinal Consistency**:
- Retrain model on new data each month
- Track MAPE across retraining periods
- **Target**: MAPE variance <2% month-to-month

**Forecast Consistency**:
- For same customer scored at *t* and *t+7 days*, predictions should be similar
- **Target**: <10% change in LTV unless major behavioral shift

#### Lift Over Baseline

Compare advanced model to simple heuristics:

**Baseline**: Current State average value × simple persistence rate

**Lift Metric**:
```
Lift = (MAPE_baseline - MAPE_model) / MAPE_baseline × 100%
```

**Target**: >15% lift over baseline

### Transition Probability Evaluation

#### Accuracy Metrics

**Primary Metrics:**

1. **Multi-Class Log-Loss** - Probabilistic accuracy
   ```
   LogLoss = -(1/N) × Σ_i Σ_j y_ij × log(p_ij)
   ```
   Where *y_ij* = 1 if customer *i* transitioned to State *j*, else 0

2. **Brier Score** - Mean squared error of probabilities
   ```
   Brier = (1/N) × Σ_i Σ_j (y_ij - p_ij)²
   ```

3. **Accuracy** - Percent correct if taking argmax
   ```
   Accuracy = % customers where predicted_state = actual_state
   ```

**Secondary Metrics:**
- **Per-State Precision/Recall**: Especially for rare but important transitions
- **AUC-ROC**: For each State-specific binary classifier

#### Calibration

**Reliability Diagram**: For predicted probability bins, check observed frequency matches

**Expected Calibration Error (ECE)**:
```
ECE = Σ_b (n_b / N) × |accuracy_b - confidence_b|
```

**Target**: Well-calibrated (ECE < 0.10)

#### Transition Matrix Stability

**Matrix Consistency Across Time**:
Compare transition matrices from different training periods using:

```
Frobenius Norm Distance = √(Σ_ij (P1_ij - P2_ij)²)
```

**Target**: Matrix changes <0.15 month-to-month (indicates stable customer dynamics)

**Diagonal Dominance**:
For each State *s*, ensure: `P(stay in s) > Σ P(leave s) / (num_states - 1)`

#### Rare Transition Detection

**Confusion Matrix Analysis**: Ensure rare but critical transitions are not missed

Example: Stable → Declining is important to catch even if infrequent

**Precision-Recall Trade-off**: Tune threshold for high-value segments

### State-Level Aggregate Evaluation

#### Portfolio Forecasting Accuracy

Aggregate customer-level predictions to State level:

```
For each State s at time t:
  Predicted_Total_Value_s = Σ (LTV_i for all i in State s)
  Actual_Total_Value_s = Σ (Observed_Revenue_i)

  State_MAPE_s = |Predicted - Actual| / Actual × 100%
```

**Target**: State-level MAPE <5-10%

#### State Size Stability

Predicted State sizes (number of customers) should match observed:

```
For each State s:
  Predicted_Size_s = Σ P(i → s)  (sum of transition probs)
  Actual_Size_s = COUNT(customers in State s at t+Δt)
```

### Business Validation

#### Segment Prioritization Accuracy

**Use Case**: Marketing wants to target top 10% of customers by predicted value

**Metric**: Overlap between predicted top 10% and actual top 10%

```
Precision@10% = |Predicted_Top10 ∩ Actual_Top10| / |Predicted_Top10|
```

**Target**: >70% precision

#### Intervention Sensitivity

**Test**: Do predictions respond appropriately to behavioral changes?

**Example**: Customer increases frequency by 50% → LTV should increase meaningfully

**Approach**: Synthetic scenario testing with business stakeholders

#### Stakeholder Feedback

**Qualitative Assessment**:
- Are predictions aligned with business intuition?
- Do surprising predictions have reasonable explanations?
- Are model outputs actionable?

---

## Implementation Requirements

### Data Requirements

#### Minimum Data Quality Standards

| Data Element | Completeness | Accuracy | Latency |
|-------------|--------------|----------|---------|
| Transaction history | >99% | High (source of truth) | T+1 day |
| Analytical ID linkage | >95% | Medium (some unlinkable) | T+1 day |
| Starbucks Rewards data | >90% SR members | High | T+1 day |
| Product master | 100% | High | Weekly refresh OK |
| Channel indicators | >98% | High | T+1 day |

#### Data Retention

- **Transaction history**: Minimum 2 years rolling for model training
- **Feature store**: Minimum 1 year of calculated features
- **Model predictions**: Minimum 6 months for monitoring

#### Data Governance

- **PII Handling**: All models use Analytical ID (not PII)
- **Data Access**: Role-based access control via Databricks
- **Audit Trail**: Track data lineage for reproducibility

### Infrastructure Requirements

#### Compute

**Model Training**:
- Databricks cluster: 4-8 workers, 32 GB RAM each
- Training frequency: Monthly retraining initially
- Training time budget: <6 hours per model

**Batch Scoring**:
- Daily scoring: 1-2 hour runtime for full customer base
- Auto-scaling cluster based on demand

#### Storage

- **Feature store**: ~500 GB (100M customers × 50 features × multiple windows)
- **Model artifacts**: <10 GB per model version
- **Predictions**: ~50 GB per monthly snapshot

#### Model Serving (Phase 2)

- **Throughput**: 1000 predictions/second
- **Latency**: <100ms p99
- **Availability**: 99.9% uptime

### MLOps Requirements

#### Model Monitoring

**Drift Detection**:
- **Data Drift**: Feature distributions changing over time
  - Monitor: Mean, stddev, percentiles for key features
  - Alert: >2 standard deviations from training distribution

- **Prediction Drift**: Model output distributions changing
  - Monitor: Average predicted LTV, State transition rates
  - Alert: >10% change from baseline

- **Performance Drift**: Accuracy degrading
  - Monitor: MAPE on recent data (rolling 30-day window)
  - Alert: >15% increase in error rate

**Calibration Monitoring**:
- Weekly: Check State-level aggregate accuracy
- Monthly: Full recalibration analysis

**Dashboard Requirements**:
- Real-time model performance metrics
- Feature distribution comparisons (training vs. production)
- Prediction quality trends over time
- Alerting for anomalies

#### Model Retraining

**Trigger Conditions**:
1. **Scheduled**: Monthly retraining (default)
2. **Performance-Based**: MAPE degrades >20% from baseline
3. **Data-Based**: Significant drift detected
4. **Business-Based**: Major program changes (new loyalty tier, etc.)

**Retraining Process**:
1. Pull latest data (trailing 12 months)
2. Recreate features with updated logic if needed
3. Train new model version
4. Validate on hold-out set
5. Compare to current production model
6. Deploy if performance is better or comparable

#### Versioning

- **Model versions**: Semantic versioning (v1.0.0, v1.1.0, etc.)
- **Feature versions**: Track feature calculation logic changes
- **Data versions**: Snapshot training data for reproducibility

#### A/B Testing

Before full deployment of model updates:
- Champion/Challenger framework
- Route 10% traffic to new model
- Compare predictions and business outcomes
- Gradual rollout if successful

### Deployment Workflow

#### Development → Production Pipeline

1. **Development** (Databricks notebooks)
   - Experiment with model variations
   - Track experiments in MLflow

2. **Staging** (Databricks Jobs)
   - Scheduled retraining jobs
   - Automated evaluation on validation set
   - Model registration to ML Registry

3. **Production** (Scheduled batch scoring)
   - Daily/weekly scoring jobs
   - Write predictions to production Delta tables
   - Trigger downstream processes (e.g., Adobe sync)

4. **Monitoring** (Databricks SQL + Dashboards)
   - Performance metrics
   - Drift detection
   - Business KPI tracking

### Integration with Activation Platforms

#### Analytical Activation

**Databricks SQL Access**:
```sql
-- Example: Identify high-value, at-risk customers
SELECT
    customer_id,
    current_state,
    ltv_90day,
    prob_decline,
    CASE
        WHEN ltv_90day > PERCENTILE(ltv_90day, 0.75)
             AND prob_decline > 0.30
        THEN 'High Value At Risk'
        ELSE 'Other'
    END AS segment
FROM scored_customers_daily
WHERE score_date = CURRENT_DATE
```

**Tableau/Power BI Dashboards**:
- Connect to scored customer tables
- Build segment-level performance views
- Enable business users to explore predictions

#### Operational Activation

**Adobe Journey Optimizer**:
- Daily sync of scored customers
- Create audience segments based on predictions:
  - "Predicted to churn in 30 days"
  - "High growth potential"
  - "Ready for Stars Rewards offer"

**Offer Management Systems**:
- Use transition probabilities to determine offer eligibility
- Dynamic offer optimization based on predicted LTV

**CRM Systems**:
- Enrich customer profiles with predictions
- Enable personalized outreach

---

## Use Cases and Applications

### Use Case 1: Churn Prevention

**Objective**: Identify high-value customers at risk of lapsing and intervene with targeted retention offers

**Approach**:
1. Identify customers with:
   - Current State = "Stable" or "Most Valuable"
   - P(Transition to Declining or Lapsing) > 25%
   - LTV > 75th percentile

2. Prioritize by expected value loss: `Current LTV × Churn Probability`

3. Design intervention:
   - Personalized offer (based on product preferences)
   - Channel: Email or Mobile App push
   - Timing: Trigger when probability crosses threshold

**Success Metrics**:
- Retention rate lift in targeted segment
- ROI: (Incremental revenue from retained customers) / (Cost of offers)
- Transition rate: % moving from at-risk back to Stable

**Example**:
```
Customer #12345:
- Current State: Stable
- LTV_90day: $240
- P(Declining): 35%
- Expected value loss: $240 × 0.35 = $84
- Action: Send $10 offer to incentivize next visit
- Expected ROI: ($84 saved - $10 offer) / $10 = 7.4x
```

### Use Case 2: Growth Opportunity Identification

**Objective**: Find customers with high expansion potential for category cross-sell

**Approach**:
1. Identify customers with:
   - P(Transition to higher State) > 20%
   - Low product depth (<3 categories)
   - High engagement in specific daypart

2. Recommend products from unexplored categories

3. Measure: Transition rate to higher States post-campaign

**Example**:
```
Customer #67890:
- Current State: New & Reactivated
- P(Transition to Stable): 28%
- Current categories: Coffee only
- Action: Promote food pairing at morning daypart
- Outcome: Expand to 2-3 categories → increase transition probability
```

### Use Case 3: Loyalty Program Optimization

**Objective**: Forecast Stars Rewards redemption and optimize tier benefits

**Approach**:
1. Predict State transitions for next quarter

2. Estimate Stars accrual and redemption by State:
   ```
   Expected_Redemptions = Σ (P(State_j) × Avg_Redemption_Rate_j × Customer_Count)
   ```

3. Model impact of tier benefit changes on State transitions

4. Optimize: Maximize engagement uplift per dollar of rewards cost

**Success Metrics**:
- Forecasting accuracy for quarterly Stars liability
- Incremental State transitions attributable to program changes

### Use Case 4: Revenue Forecasting

**Objective**: Improve accuracy of quarterly revenue forecasts using customer-level predictions

**Approach**:
1. Aggregate predicted LTV to customer base total:
   ```
   Forecast_Revenue_Q3 = Σ LTV_90day (for all active customers)
   ```

2. Adjust for:
   - New customer acquisition estimates
   - Seasonality factors
   - Known marketing campaigns

3. Compare to historical forecasting method (e.g., trend projection)

**Success Metrics**:
- MAPE improvement over baseline forecasting
- Confidence intervals for revenue range

**Example**:
```
Historical Forecast Method MAPE: 8%
Customer States LTV Forecast MAPE: 6%
→ 25% improvement in forecast accuracy
→ Better planning for operations, staffing, inventory
```

### Use Case 5: Campaign Measurement via State Transitions

**Objective**: Measure marketing campaign effectiveness by observing State transitions

**Approach**:
1. **Pre-Campaign**: Score all customers, record current States

2. **Campaign Execution**: Target specific segment (e.g., "Declining" customers)

3. **Post-Campaign**: Rescore after 30 days, measure:
   - Transition rate in targeted vs. control group
   - Average LTV change in targeted vs. control

4. **Calculate ROI**:
   ```
   Incremental Value = (Avg_LTV_Treated - Avg_LTV_Control) × Num_Customers_Treated
   ROI = (Incremental Value - Campaign Cost) / Campaign Cost
   ```

**Success Metrics**:
- Statistically significant State transition lift (p < 0.05)
- Positive ROI
- Learnings for future campaign optimization

**Example**:
```
Campaign: "Win-back offer" for Declining customers
- Treated group: 50,000 customers
- Control group: 50,000 customers (no offer)

Results after 30 days:
- Treated: 15% transitioned back to Stable (vs. 8% in control)
- 7% lift → 3,500 additional customers retained
- Avg incremental LTV per customer: $50
- Total incremental value: 3,500 × $50 = $175,000
- Campaign cost: $50,000
- ROI: ($175K - $50K) / $50K = 250%
```

---

## Timeline and Milestones

### Phase 1: Foundation (Months 1-2)

**Month 1:**
- ✅ Finalize Customer States definitions (High/Medium/Low categories)
- ✅ Complete RFMC feature analysis
- ✅ Begin behavioral feature engineering (SR, Product, Channel)

**Month 2:**
- Complete full feature dataset creation
- Validate State assignment logic on historical data
- Establish baseline performance benchmarks
- Stakeholder alignment on framework

**Deliverables:**
- Documented State definitions and assignment rules
- Feature engineering codebase (Databricks notebooks)
- Baseline model performance report

### Phase 2: Model Development (Months 2-3)

**Month 2-3:**
- Develop candidate LTV models (linear → GBM → hybrid State-based)
- Develop candidate transition probability models (softmax → XGBoost)
- Hyperparameter tuning and model selection
- Evaluation on hold-out test set

**Deliverables:**
- Trained LTV model (final architecture selected)
- Trained transition probability model
- Model evaluation report with accuracy, calibration, stability metrics
- Model registry entries (MLflow)

### Phase 3: Validation and Iteration (Months 3-4)

**Month 3:**
- Out-of-time validation (April-May 2026 data)
- Longitudinal stability testing across time periods
- Stakeholder review of predictions (business validation)
- Refinement based on feedback

**Month 4:**
- Finalize model parameters
- Document model cards (methodology, performance, limitations)
- Prepare model handoff to production team

**Deliverables:**
- Validated model performance on recent data
- Stakeholder sign-off on model outputs
- Model documentation and lineage

### Phase 4: Deployment Preparation (Months 4-5)

**Month 4-5:**
- Build production scoring pipeline (Databricks Jobs)
- Integrate with downstream systems (Adobe, CRM)
- Set up monitoring dashboards
- Conduct user acceptance testing

**Month 5:**
- Deploy to production (batch scoring)
- Initial scoring run for full customer base
- Enable analytical and operational access
- Monitor for issues

**Deliverables:**
- Production scoring pipeline (daily/weekly jobs)
- Scored customer tables accessible to business users
- Monitoring dashboards operational
- Deployment runbook and support documentation

### Phase 5: Operationalization (Month 6+)

**Ongoing:**
- Monthly model retraining
- Performance monitoring and drift detection
- Use case enablement (campaigns, forecasting, reporting)
- Iteration based on business feedback and results

**Success Review (Month 6):**
- Evaluate business impact from initial use cases
- Assess model performance in production
- Plan enhancements and new use cases

---

## Appendix

### A. Mathematical Notation Reference

| Symbol | Definition |
|--------|------------|
| *i* | Customer index |
| *j*, *s* | State index |
| *t* | Time (current scoring date) |
| *H* | Planning horizon (e.g., 90 days, 365 days) |
| *Δt* | Transition time window (e.g., 30 days) |
| LTV_i | Lifetime value for customer *i* |
| Value(S_j) | Average value of State *j* |
| P_ij | Probability customer *i* transitions to State *j* |
| MAPE | Mean Absolute Percent Error |
| MAE | Mean Absolute Error |
| R² | Coefficient of determination |

### B. Feature Importance Summary (June 2026 Analysis)

From feature selection analysis on 500K customer sample:

**Top Features for 90-Day Revenue Prediction:**

| Rank | Feature | R² Contribution | Cumulative R² |
|------|---------|-----------------|---------------|
| 1 | Avg Monthly Revenue (90d) | 0.54 | 0.54 |
| 2 | Days Since Last Purchase | 0.03 | 0.57 |
| 3 | Transaction Frequency (90d) | 0.02 | 0.59 |
| 4 | Stars Redeemed (30d) | 0.01 | 0.60 |
| 5 | Channel Diversity | 0.01 | 0.61 |

**Key Findings:**
- Monetary value dominates (54% of variance explained)
- Recency adds meaningful signal (3%)
- Behavioral features provide incremental lift but diminishing returns
- Consistency metrics (entropy, CV) not worth complexity (<0.5% gain)

### C. State Transition Baseline Rates (Historical Data)

From Jan-May 2026 observed transitions (30-day windows):

**Transition Matrix (from → to):**

| From \ To | Most Valuable | Stable | New & Reactivated | Declining | Lapsing | Unengaged |
|-----------|---------------|--------|-------------------|-----------|---------|-----------|
| **Most Valuable** | 78% | 12% | 2% | 5% | 2% | 1% |
| **Stable** | 8% | 72% | 5% | 10% | 3% | 2% |
| **New & Reactivated** | 5% | 25% | 45% | 10% | 10% | 5% |
| **Declining** | 3% | 15% | 5% | 50% | 20% | 7% |
| **Lapsing** | 1% | 5% | 10% | 15% | 40% | 29% |
| **Unengaged** | 0% | 1% | 15% | 5% | 10% | 69% |

**Observations:**
- Diagonal elements (stay in State) are highest (40-78%)
- Adjacent transitions more common than large jumps
- Most Valuable and Stable States show high persistence
- New & Reactivated has most uncertainty (diverse outcomes)
- Unengaged and Lapsing risk full disengagement

### D. Model Performance Targets Summary

| Model | Metric | Target | Rationale |
|-------|--------|--------|-----------|
| **LTV** | Customer-level MAPE | <15% | Industry standard for LTV prediction |
| | State-level MAPE | <10% | Higher accuracy needed for planning |
| | R² | >0.55 | Beat RFMC baseline (0.57 including behaviors) |
| | Lift over baseline | >15% | Justify model complexity |
| **Transition** | Log-Loss | TBD | Benchmark against baseline rates |
| | Accuracy (argmax) | >60% | Better than random (16% for 6 States) |
| | ECE (calibration) | <0.10 | Well-calibrated probabilities |
| | Matrix stability | <0.15 Frobenius distance | Ensure consistent dynamics |
| **Both** | Longitudinal stability | MAPE variance <2% | Predictions remain reliable |

### E. Risks and Mitigation Strategies

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Data Quality Issues** | High | Medium | Implement data validation checks; establish SLAs with source systems |
| **Model Overfitting** | High | Medium | Use time-series CV; regularization; simple model selection |
| **State Definitions Change** | High | Low | Version State assignment logic; retrain models when States change |
| **Concept Drift** | High | Medium | Continuous monitoring; monthly retraining; drift detection alerts |
| **Business Misinterpretation** | Medium | Medium | Stakeholder education; clear documentation; use case examples |
| **Integration Failures** | Medium | Low | Thorough testing; fallback mechanisms; SLA with platform teams |
| **Insufficient Training Data** | High | Low | Ensure 2+ years history; augment with synthetic scenarios if needed |
| **Model Complexity Barrier** | Low | Medium | Prefer interpretable models; provide feature importance; Shapley values |

### F. Glossary

**Analytical ID**: Unified customer identifier used for analytics (not PII)

**Bias-Variance Trade-off**: Balance between systematic error (bias) and sensitivity to noise (variance)

**Calibration**: Alignment between predicted probabilities and observed frequencies

**Customer States**: Segmentation framework based on value and behavioral signals

**Expected Value**: Probability-weighted sum of possible outcomes

**Feature Engineering**: Creating predictive variables from raw data

**Lifetime Value (LTV)**: Expected future revenue from a customer over a time horizon

**MAPE (Mean Absolute Percent Error)**: Average prediction error as percentage of actual value

**Markov Model**: Model where future state depends only on current state (not history)

**MLOps**: Practices for deploying and maintaining ML models in production

**R-Squared (R²)**: Proportion of variance in outcome explained by model

**State Transition**: Customer moving from one Customer State to another

**Transition Probability**: Likelihood of moving from one State to another in given time window

---

**WRITER STATUS: READY FOR REVIEW**

This document represents a comprehensive rewrite of the original predictive models specification with:
- Enhanced structure and clarity
- Expanded technical details and methodology
- Comprehensive evaluation framework
- Clear implementation guidance
- Concrete use cases and business value articulation

Next step: Reviewer Agent evaluation and feedback.
