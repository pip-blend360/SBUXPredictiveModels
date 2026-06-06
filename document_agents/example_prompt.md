# Example Prompts for Document Writing System

This file contains example prompts you can use with the document writing system. Copy and modify these for your needs.

## Example 1: Technical Specification

```
Write a technical specification document for a Starbucks customer churn prediction model.

The document should include:
- Problem statement and business objectives
- Data requirements and sources
- Model architecture and algorithm selection
- Feature engineering approach
- Training and validation strategy
- Performance metrics and success criteria
- Deployment considerations
- Maintenance and monitoring plan

Use the materials in the background/ folder for context. The specification should be comprehensive enough for a data science team to implement the solution.
```

## Example 2: Model Evaluation Report

```
Create a comprehensive model evaluation report for our customer segmentation models.

Include:
- Executive summary
- Model performance comparison (accuracy, precision, recall, F1)
- Feature importance analysis
- Confusion matrices and ROC curves
- Business impact assessment
- Recommendations for production deployment
- Identified limitations and risks

Target audience: Both technical data scientists and non-technical stakeholders.
```

## Example 3: Data Pipeline Documentation

```
Document the end-to-end data pipeline for customer behavior tracking.

Cover:
- Data sources and ingestion methods
- ETL processes and transformations
- Data quality checks and validation
- Storage architecture
- Access patterns and query optimization
- Monitoring and alerting
- Error handling and recovery
- Security and compliance considerations

Format as technical documentation for data engineers.
```

## Example 4: Experimental Design

```
Design an A/B test experiment for evaluating a new customer retention strategy.

Document:
- Hypothesis and success metrics
- Sample size calculation
- Randomization and assignment strategy
- Control and treatment group definitions
- Data collection plan
- Statistical analysis approach
- Timeline and milestones
- Risk mitigation strategies

Include statistical rigor and practical implementation details.
```

## How to Use

1. **Choose a prompt** from above or create your own
2. **Customize** it for your specific needs
3. **Add background materials** to `background/` folder
4. **Run the orchestrator**:
   ```bash
   # Copy your chosen prompt
   # Then run (replace with your actual command):
   claude-code skills/orchestrator.md --prompt "Your prompt here"
   ```

## Tips for Good Prompts

- **Be specific** about document type and purpose
- **List key sections** you want included
- **Specify audience** (technical vs. non-technical)
- **Reference background materials** when available
- **Define success criteria** for the document
- **Include formatting preferences** (diagrams, code examples, etc.)

## Prompt Template

```
Write a [DOCUMENT TYPE] for [PROJECT/TOPIC].

The document should include:
- [Section 1]
- [Section 2]
- [Section 3]
- ...

Target audience: [AUDIENCE]
Purpose: [PURPOSE]

Use materials in background/ folder for context.
Additional requirements: [ANY SPECIFIC REQUIREMENTS]
```
