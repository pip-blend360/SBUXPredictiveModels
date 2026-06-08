# Logo Instructions

To add your Starbucks logo to the presentation:

## Option 1: Add Your Logo File

1. Save your logo as `logo.png` in this folder (`slides/`)
2. Recommended specifications:
   - Format: PNG with transparent background
   - Size: 200x200 pixels or larger
   - File name: `logo.png` (exactly)

3. Export your presentation:
   ```bash
   marp presentation.md --theme-set starbucks-theme.css -o presentation.pptx
   ```

The logo will appear in the top-right corner of every slide (except title slides).

## Option 2: Use a Different Logo Format

If your logo is named differently or in a different format:

1. Edit `starbucks-theme.css` (line 158)
2. Change:
   ```css
   background-image: url('logo.png');
   ```
   To:
   ```css
   background-image: url('your-logo-name.svg');  /* or .jpg, .png, etc. */
   ```

## Option 3: No Logo

If you don't want a logo, you have two options:

**A. Comment out the logo CSS:**
1. Open `starbucks-theme.css`
2. Find lines 152-162 (the logo section)
3. Wrap in comments:
   ```css
   /*
   section:not(.lead)::before {
     ...all the logo code...
   }
   */
   ```

**B. Just export without a logo file:**
- The presentation will work fine
- You'll see a broken image icon in the corner (not visible in exported PowerPoint)

## Testing

**Preview with VS Code:**
1. Install "Marp for VS Code" extension
2. Open `presentation.md`
3. Click preview button
4. Check if logo appears correctly

**Test export:**
```bash
marp presentation.md --theme-set starbucks-theme.css -o test.pptx
```

Open `test.pptx` and verify the logo appears on slides 2-19 (not on title/end slides).
