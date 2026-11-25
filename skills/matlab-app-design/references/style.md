# Default look for a MATLAB app with an HTML screen

Use these values when the project has no style of its own. The aim is a
calm scientific tool: light surfaces, one accent colour, the data as the
most visible thing on screen.

## Tokens

```css
:root {
  --bg-primary: #E8EBED;  --bg-secondary: #F2F4F6;  --bg-tertiary: #EBF0F4;
  --text-primary: #1E293B;  --text-secondary: #64748B;  --text-tertiary: #94A3B8;
  --accent-primary: #42A5F5;  --accent-secondary: #90CAF9;
  --border-color: #E2E8F0;  --shadow-color: rgba(0, 0, 0, 0.05);
  --ok-color: #10B981;  --warning-color: #F59E0B;  --error-color: #EF4444;

  --space-1: 4px;  --space-2: 8px;  --space-3: 16px;
  --space-4: 24px; --space-5: 32px; --space-6: 48px;
  --radius-input: 8px;  --radius-button: 12px;  --radius-panel: 16px;
  --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  --font-mono: 'SF Mono', 'Consolas', monospace;
}
[data-theme="dark"] {
  --bg-primary: #0F172A;  --bg-secondary: #1E293B;  --bg-tertiary: #334155;
  --text-primary: #F1F5F9;  --text-secondary: #CBD5E1;  --text-tertiary: #94A3B8;
  --accent-primary: #60A5FA;  --accent-secondary: #93C5FD;
  --border-color: #334155;  --shadow-color: rgba(0, 0, 0, 0.3);
  --ok-color: #34D399;  --warning-color: #FBBF24;  --error-color: #F87171;
}
```

## Type

- Base text 14 px, line height 1.5. Titles 24 / 20 / 18 px at line
  height 1.2. Small text 13 and 12 px; nothing under 11 px.
- Weights 400, 500, 600, 700; at most three of them on one screen.
- Numbers the person reads or types (parameters, values, axes) in the
  monospace stack, so digits line up.

## Space and shape

- Spacing only from the scale (4, 8, 16, 24, 32, 48 px). Panel padding
  24, card padding 20, input padding 12.
- Panels: `--bg-secondary`, 1 px border, radius 16, a soft shadow.
- Buttons: radius 12. One primary button per screen (accent colour);
  the rest neutral. Hover lifts 2 px; transitions `0.2s ease`.
- Inputs: radius 8, a focus ring in the accent colour.
- Icons come with a text label.

## Plots

- One colour per meaning, the same on every screen: data in the accent
  colour, a fitted or estimated curve in the error red, a result in the
  ok green, context curves in grey at low opacity.
- Grid lines faint (`rgba(0, 0, 0, 0.08)`), axis text in
  `--text-secondary`, axis labels with units.
- A selected region is a pale fill with a stronger border, not a change
  of the curve's colour.

## Rules

- Contrast at least 4.5 to 1 for text, 3 to 1 for large text and for the
  edges of controls. Colour is not the only carrier of a meaning: add a
  word, an icon or a line style.
- No pure black or pure white. No `!important`. Sizes in px.
- Class names by block and part (`panel`, `panel__title`,
  `button--primary`).
- Designed for a window at least 1280 px wide; say so if the layout does
  not hold below that.
- Visible focus on every control; the whole app reachable with Tab and
  Enter.

## Before calling it done

- The same spacing, radius and colours on every screen, all from the
  variables.
- Light and dark both looked at in a picture.
- No text cut off at the smallest supported width.
- Empty, loading, error and result states each have a designed look.
