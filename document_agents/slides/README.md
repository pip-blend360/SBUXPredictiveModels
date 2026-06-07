# Predictive Models Presentation

This folder contains a presentation summarizing the technical specification for Customer States Predictive Models.

## Files

- `presentation.md` - Marp-formatted slide deck (20 slides)

## How to Use

### Option 1: Export to PowerPoint (Recommended)

**Install Marp CLI:**
```bash
npm install -g @marp-team/marp-cli
```

**Export to PowerPoint:**
```bash
marp presentation.md -o presentation.pptx
```

**Export to PDF:**
```bash
marp presentation.md -o presentation.pdf
```

### Option 2: Present as HTML

```bash
marp presentation.md -o presentation.html
# Open presentation.html in browser
```

### Option 3: Preview in VS Code

1. Install the "Marp for VS Code" extension
2. Open `presentation.md`
3. Click the preview button (top right)

### Option 4: Copy to PowerPoint Manually

If you don't want to install Marp, you can:
1. Open `presentation.md` in any text editor
2. Copy slide content (between `---` separators)
3. Paste into PowerPoint slides
4. Format as needed

## Slide Overview

1. **Title** - Project overview
2. **Objective** - Two models (LTV + Transitions)
3. **Business Problem** - Stakeholder needs
4. **Hybrid Approach** - Key innovation formula
5. **Customer States** - Framework overview
6. **Model 1: LTV** - Mathematical formulation
7. **Model 2: Transitions** - Probability prediction
8. **State-Level Aggregation** - Key requirement
9. **Feature Engineering** - RFMC + Seasonality
10. **Evaluation** - Metrics and targets
11. **Architecture** - Databricks stack
12. **MLOps** - Monitoring and retraining
13. **Use Case: Churn** - ROI example (250%)
14. **Use Case: Forecasting** - 25% error reduction
15. **Timeline** - 5 months to production
16. **Success Criteria** - Model + business metrics
17. **Why This Works** - Technical/business strengths
18. **Next Steps** - Phase 1 kickoff
19. **Questions** - Final slide

## Customization

Edit `presentation.md` to:
- Change theme (add `theme: gaia` or other Marp themes)
- Adjust colors (`backgroundColor`, `color`)
- Add company logo
- Modify content per audience

## Notes

- LaTeX equations are supported: `$...$` for inline, `$$...$$` for display
- Tables render automatically
- Code blocks use triple backticks
- `<!-- _class: lead -->` creates centered title slides
