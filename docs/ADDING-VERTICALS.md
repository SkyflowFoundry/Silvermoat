# Adding New Verticals

Quick reference for adding a new vertical (e.g., healthcare, logistics) to Silvermoat.

## 1. UI Structure

Create `ui-{vertical}/` directory with:

**Landing Page** (`src/pages/Landing/Landing.jsx`)
- Customer/Employee portal selector (2-column cards)
- Vertical-specific gradient background
- Floating architecture info icon (bottom-right)

**ArchitectureViewer** (`src/components/common/ArchitectureViewer.jsx`)
- Vertical-specific project overview
- 7-10 key features list
- Technology stack section
- References `/architecture-{vertical}.png` and `/data-flow-{vertical}.png`

**App Routing** (`src/App.jsx`)
- Root `/` renders Landing (no layout)
- Customer routes: `/customer/*` (no AppLayout)
- Employee routes with AppLayout: `/dashboard`, `/entity/*`

**Branding**
- Landing gradient: `linear-gradient(135deg, {color1}, {color2})`
- Customer portal icon: Blue gradient
- Employee portal icon: Vertical-specific color
- Logo: `/silvermoat-logo.png`

## 2. Architecture Diagrams

**Script Updates** (`scripts/generate-architecture-diagram.py`)

Add vertical-specific diagram functions:
```python
def generate_{vertical}_only_architecture_diagram():
    # Shows only {vertical} vertical infrastructure
    # Output: docs/architecture-{vertical}.png

def generate_{vertical}_only_data_flow_diagram():
    # Shows only {vertical} data flow
    # Output: docs/data-flow-{vertical}.png
```

Update main() argparse to include new vertical:
```python
choices=["insurance", "retail", "{vertical}", "all"]
```

Update multi-vertical diagrams to include new vertical in the full architecture view.

## 3. Deployment Configuration

**deploy-ui.sh Updates**

Add vertical deployment block:
```bash
# Deploy {Vertical} UI
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "{vertical}" ]; then
  deploy_vertical_ui "{Vertical}" "$PROJECT_ROOT/ui-{vertical}" "${VERTICAL}_BUCKET" "${VERTICAL}_API_URL"

  # Copy vertical-specific architecture diagrams
  if [ -f "$PROJECT_ROOT/docs/architecture-{vertical}.png" ]; then
    echo "Copying {vertical} architecture diagrams..."
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/architecture-{vertical}.png" "s3://${VERTICAL}_BUCKET/architecture-{vertical}.png"
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/data-flow-{vertical}.png" "s3://${VERTICAL}_BUCKET/data-flow-{vertical}.png"
    echo ""
  fi
fi
```

Get bucket/API URL from stack outputs (add near top):
```bash
{VERTICAL}_BUCKET=$(aws cloudformation describe-stacks ...)
{VERTICAL}_API_URL=$(aws cloudformation describe-stacks ...)
```

## 4. Main Landing Integration

**Update Main Landing** (`ui-landing/src/pages/Landing/Landing.jsx`)

Add vertical to grid:
```javascript
const verticals = [
  // ... existing verticals
  {
    name: '{Vertical}',
    icon: <YourIcon style={{ fontSize: 48, color: '#yourcolor' }} />,
    description: 'Brief description (1-2 lines)',
    url: {vertical}Url,
    color: '#yourcolor',
  },
];
```

Add environment variable handling:
```javascript
const {vertical}Url = import.meta.env.VITE_{VERTICAL}_URL;
```

**Update Main Landing ArchitectureViewer**
- Add vertical-specific features to combined feature list
- Update database count (7 tables per vertical)
- Multi-vertical diagrams auto-include new vertical

## 5. GitHub Actions Workflows

**deploy-test.yml & deploy-production.yml**

Add vertical-specific jobs:
```yaml
deploy-{vertical}-ui:
  name: Deploy {Vertical} UI
  needs: [deploy-{vertical}-infra, ...]
  steps:
    - name: Install dependencies
      uses: ./.github/actions/install-deps

    - name: Build and deploy {vertical} UI
      env:
        STACK_NAME: ${{ needs.detect-changes.outputs.base_stack_name }}
        VERTICAL: {vertical}
      run: |
        chmod +x scripts/deploy-ui.sh
        ./scripts/deploy-ui.sh
```

Add to change detection logic for selective deployment.

## 6. File Checklist

**Required files:**
- [ ] `ui-{vertical}/package.json` (with dependencies)
- [ ] `ui-{vertical}/src/App.jsx`
- [ ] `ui-{vertical}/src/pages/Landing/Landing.jsx`
- [ ] `ui-{vertical}/src/components/common/ArchitectureViewer.jsx`
- [ ] `ui-{vertical}/public/silvermoat-logo.png`
- [ ] Update `scripts/generate-architecture-diagram.py`
- [ ] Update `scripts/deploy-ui.sh`
- [ ] Update `ui-landing/src/pages/Landing/Landing.jsx`
- [ ] Update `ui-landing/src/components/common/ArchitectureViewer.jsx`
- [ ] Update `.github/workflows/deploy-test.yml`
- [ ] Update `.github/workflows/deploy-production.yml`

## 7. Color Scheme Conventions

- **Insurance**: Blue (`#003d82`, `#667eea → #764ba2` gradient)
- **Retail**: Purple (`#722ed1`, `#722ed1 → #531dab` gradient)
- **Pattern**: Choose distinct brand color, create gradient variants for consistency

## 8. Infrastructure Requirements

Each vertical needs:
- CDK stack: `{vertical}_stack.py`
- Lambda handlers (4-6 typical)
- DynamoDB tables (7 typical)
- S3 buckets (UI + documents)
- CloudFront distribution
- API Gateway
- ACM certificate (SSL)
- Route53 DNS: `{vertical}.silvermoat.net`

See existing insurance/retail stacks for patterns.

## Example: Adding "Healthcare" Vertical

1. Copy `ui-insurance/` → `ui-healthcare/`
2. Update branding (green theme, medical icons)
3. Add `generate_healthcare_only_*_diagram()` functions
4. Add healthcare block to `deploy-ui.sh`
5. Update main landing grid with Healthcare card
6. Add healthcare workflows to GitHub Actions
7. Deploy infrastructure via CDK
8. Deploy UI via `VERTICAL=healthcare ./scripts/deploy-ui.sh`

**Estimated effort:** 4-6 hours for experienced developer following this template.
