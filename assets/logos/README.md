# Logo Assets

Source logo files for Silvermoat Insurance branding.

## Files

### Production Logo

- **silvermoat-full-color.svg** - Full color logo with gradient (pink → purple → teal)
  - Optimized version deployed to `ui/public/silvermoat-logo.svg` (10.3KB)
  - Used across all UI locations (favicon, header, landing page)

### Variant Logos (Not Currently Used)

- **silvermoat-monochrome-dark.svg** - Dark monochrome (#1B1B2E)
- **silvermoat-monochrome-light.svg** - Light monochrome (white)

## Specifications

- **Dimensions**: 6800×2000 viewBox
- **Format**: SVG
- **Gradient Colors**: #D99AD3 → #989DFC → #42A1B8
- **File Size**: ~14-15KB (source), 10.3KB (optimized)

## Optimization

To optimize logos for production:

```bash
cd ui
npx svgo "../assets/logos/[filename].svg" -o public/[output].svg
```

## Usage

The full-color logo is currently used in:

1. Browser favicon
2. Loading screen
3. Header navigation
4. Landing page hero

Monochrome variants are available for future theme/branding needs.
