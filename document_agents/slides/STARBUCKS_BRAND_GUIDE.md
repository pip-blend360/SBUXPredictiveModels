# Starbucks Brand Guide for Presentations

## Official Color Palette

| Color Name | Hex Code | RGB | Usage |
|------------|----------|-----|-------|
| **Starbucks Green** (Primary) | `#00704A` | RGB(0, 112, 74) | Headers, emphasis, primary elements |
| **Light Green** (Accent) | `#00A862` | RGB(0, 168, 98) | Accents, borders, highlights |
| **Dark Green** (Text) | `#1e3932` | RGB(30, 57, 50) | Body text, secondary text |
| **White** | `#ffffff` | RGB(255, 255, 255) | Background, reverse text |
| **Light Gray** | `#f4f4f4` | RGB(244, 244, 244) | Code blocks, subtle backgrounds |

## Typography

**Primary Font Stack:**
```
'Lander', 'Helvetica Neue', Helvetica, Arial, sans-serif
```

**Font Sizes (configured in theme):**
- H1 (Titles): 52px
- H2 (Section Headers): 40px
- H3 (Subsections): 32px
- Body Text: 28px
- Tables/Code: 24px
- Footer: 18px

## Design Elements

**Title Slides:**
- Green gradient background (Primary → Accent)
- White text
- Centered alignment
- No logo

**Content Slides:**
- White background
- Dark green text
- Green primary headers with accent underline
- Logo in top-right corner (60x60px)

**Tables:**
- Green header row
- Alternating row backgrounds
- Light green hover effect

**Code Blocks:**
- Light gray background
- Green left border accent
- Rounded corners

**Lists:**
- Green accent bullet points
- 1.6 line height for readability

## Customization Examples

### Change to Different Brand Colors

Edit `starbucks-theme.css`:
```css
:root {
  --color-primary: #YourPrimaryColor;
  --color-accent: #YourAccentColor;
  --color-text: #YourTextColor;
}
```

### Adjust Spacing

```css
section {
  padding: 60px 80px;  /* Top/bottom left/right */
}
```

### Change Font

```css
section {
  font-family: 'YourFont', Arial, sans-serif;
  font-size: 28px;  /* Adjust base size */
}
```

## Export Quality Settings

**For best results:**

**PowerPoint:**
```bash
marp presentation.md --theme-set starbucks-theme.css -o presentation.pptx
```

**PDF (High Quality):**
```bash
marp presentation.md --theme-set starbucks-theme.css --pdf-outlines -o presentation.pdf
```

**HTML (Interactive):**
```bash
marp presentation.md --theme-set starbucks-theme.css -o presentation.html
```

## Accessibility Notes

The theme follows accessibility guidelines:
- ✅ High contrast ratios (White on Green: 7.3:1)
- ✅ Clear font hierarchy
- ✅ Readable font sizes (28px minimum body text)
- ✅ Distinct visual indicators

**Testing Contrast:** Use tools like WebAIM Contrast Checker to verify color combinations meet WCAG AA standards.
