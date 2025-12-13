# Palette's Journal

## 2025-12-11 - Canvas Accessibility
**Learning:** Canvas elements are invisible to screen readers by default. Adding `role="img"` and a descriptive `aria-label` provides necessary context.
**Action:** Always verify canvas elements have fallback content or ARIA labels.

## 2024-05-23 - Expression Validation
**Learning:** Users entering mathematical expressions need immediate syntax feedback. Silent failures (defaulting to 0) confuse users.
**Action:** Validate expressions on input using `new Function` (carefully) and toggle `aria-invalid` along with visual error states.

## 2025-10-27 - Discoverable Help vs Tooltips
**Learning:** `title` attributes are poor for discoverability and accessibility (no keyboard support). Complex inputs need visible helper text.
**Action:** Replace `title` tooltips with visible, aria-describedby helper text for complex input fields.
