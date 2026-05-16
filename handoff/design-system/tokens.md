# ZPOTS Design Tokens

Quick reference for humans. The machine-readable versions live in `shared.css` (CSS custom properties / utility classes) and `tailwind.config.ts` (Tailwind theme).

## Color

| Token | Hex | Tailwind | Use |
|---|---|---|---|
| Lime | `#CFFC00` | `zpots-lime` | Primary CTA, AI accents, status glow |
| Moss | `#2E6B00` | `zpots-moss` | Primary text-on-light emphasis, brand green |
| Forest | `#1E4A00` | `zpots-forest` | Text on lime buttons |
| Night | `#0D1F0D` | `zpots-night` | Owner sidebar, dark surfaces |
| Surface | `#F2F9EE` | `zpots-surface` | Page background (light mode) |
| Mint | `#E3F0DE` | `zpots-mint` | Thin dividers on KPI cards |
| Ink | `#1C2526` | `zpots-ink` | Body text |
| Muted | `#3D4455` | `zpots-muted` | Secondary text |

## Type

| Role | Family | Weight | Use |
|---|---|---|---|
| Display | Space Grotesk | 600–700 | Headings, KPI numbers |
| Body | Inter | 400–500 | Paragraphs, UI text |
| Eyebrow | Lexend | 600 | Small-caps labels, status text |
| Icons | Material Symbols Rounded | — | UI iconography |

## Spacing & radius

- Card radius: `16px` (`rounded-card`)
- Pill radius: `9999px` (`rounded-pill`)
- Card shadow: `0 4px 16px rgba(28,37,38,0.06)` (`shadow-card`)

## Signature moves

- **AI features** wear the lime glow: `.ai-tag` (small-caps label with a lime dot).
- **Owner AI optimizer** callouts use `.zpots-card-lime` (lime gradient card).
- **Login screens** have a dark night-sky gradient with a glass card.
- **Court imagery** is a gradient + sport emoji placeholder — swap for real photography in production.
- **Dashboard KPIs** use white cards with a 1px `zpots-mint` border (not shadow-heavy).
