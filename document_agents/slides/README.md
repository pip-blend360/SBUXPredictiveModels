# Predictive Models Presentation

This folder contains a presentation summarizing the technical specification for Customer States Predictive Models.

## Files

- `presentation.md` - Marp-formatted slide deck (20 slides) with Starbucks theme
- `starbucks-theme.css` - Custom Starbucks-branded theme with colors, fonts, styling
- `logo.png` - Place your Starbucks logo here (optional - see LOGO_INSTRUCTIONS.md)
- `STARBUCKS_BRAND_GUIDE.md` - Color palette, typography, and customization guide
- `LOGO_INSTRUCTIONS.md` - Detailed instructions for adding/removing logo
- `README.md` - This file

## Quick Start

**With Logo:**
1. Save your logo as `logo.png` in this folder
2. Run: `marp presentation.md --theme-set starbucks-theme.css -o presentation.pptx`
3. Open `presentation.pptx` in PowerPoint

**Without Logo:**
1. Run: `marp presentation.md --theme-set starbucks-theme.css -o presentation.pptx`
2. Open `presentation.pptx` in PowerPoint
3. (Optional) Edit `starbucks-theme.css` to remove logo placeholder - see LOGO_INSTRUCTIONS.md

## How to Use

## Starbucks Branding

The presentation uses a custom Starbucks theme with:
- **Primary color:** #00704A (Starbucks Green)
- **Accent color:** #00A862 (Light Green)
- **Fonts:** Lander/Helvetica Neue/Arial
- **Logo placement:** Top-right corner of each slide

### Adding Your Logo

1. Save your Starbucks logo as `logo.png` in the `slides/` folder
2. Recommended size: 200x200px (transparent background)
3. The theme will automatically display it in the top-right corner

**If you don't have a logo:**
- The presentation will work fine without it
- Or comment out the logo CSS in `starbucks-theme.css` (lines 152-162)

### Option 1: Export to PowerPoint (Recommended)

**Install Marp CLI:**
```bash
npm install -g @marp-team/marp-cli
```

**Export to PowerPoint (with Starbucks theme):**
```bash
marp presentation.md --theme-set starbucks-theme.css -o presentation.pptx
```

**Export to PDF:**
```bash
marp presentation.md --theme-set starbucks-theme.css -o presentation.pdf
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

### Content Changes
Edit `presentation.md` to modify slide content, add/remove slides, or adjust for different audiences.

### Brand Customization
Edit `starbucks-theme.css` to customize colors, fonts, or styling:

**Change Colors:**
```css
:root {
  --color-primary: #00704A;    /* Your primary brand color */
  --color-accent: #00A862;     /* Your accent color */
  --color-background: #ffffff; /* Background color */
  --color-text: #1e3932;       /* Text color */
}
```

**Change Fonts:**
```css
section {
  font-family: 'YourFont', 'Helvetica Neue', Arial, sans-serif;
}
```

**Adjust Logo Size/Position:**
```css
section:not(.lead)::before {
  top: 30px;        /* Distance from top */
  right: 40px;      /* Distance from right */
  width: 60px;      /* Logo width */
  height: 60px;     /* Logo height */
}
```

**Remove Logo:**
Comment out or delete lines 152-162 in `starbucks-theme.css`

## Notes

- LaTeX equations are supported: `$...$` for inline, `$$...$$` for display
- Tables render automatically
- Code blocks use triple backticks
- `<!-- _class: lead -->` creates centered title slides
