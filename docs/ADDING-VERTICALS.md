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

### 5.1 Update detect-changes job

Add stack existence output:
```yaml
outputs:
  {vertical}_stack_exists: ${{ steps.check-stacks.outputs.{vertical}_exists }}
```

Add stack check in check-stacks step:
```bash
# Check {vertical} stack
if aws cloudformation describe-stacks --stack-name "silvermoat-{vertical}" >/dev/null 2>&1; then
  echo "{vertical}_exists=true" >> $GITHUB_OUTPUT
else
  echo "{vertical}_exists=false" >> $GITHUB_OUTPUT
fi
```

### 5.2 Add infrastructure deployment job

```yaml
deploy-{vertical}-infra:
  name: Deploy {Vertical} Infra
  needs: [detect-changes]
  if: |
    always() &&
    needs.detect-changes.result == 'success' &&
    (needs.detect-changes.outputs.infrastructure_changed == 'true' ||
     needs.detect-changes.outputs.{vertical}_stack_exists == 'false')
  runs-on: ubuntu-latest
  timeout-minutes: 20
  outputs:
    stack_name: ${{ steps.deploy.outputs.stack_name }}

  steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup infrastructure deployment
      uses: ./.github/actions/setup-infra-deploy
      with:
        aws-role-arn: ${{ secrets.AWS_ROLE_ARN }}

    - name: Deploy {vertical} production stack
      id: deploy
      env:
        STACK_NAME: silvermoat
        VERTICAL: {vertical}
        STAGE_NAME: prod
        CREATE_CLOUDFRONT: true
        DOMAIN_NAME: silvermoat.net
      run: |
        echo "Deploying {vertical} production stack: silvermoat-{vertical}"
        chmod +x scripts/deploy-stack.sh
        ./scripts/deploy-stack.sh
        echo "stack_name=silvermoat-{vertical}" >> $GITHUB_OUTPUT
```

### 5.3 Add DNS configuration job (production only)

```yaml
configure-{vertical}-dns:
  name: Configure {Vertical} DNS
  needs: [deploy-{vertical}-infra]
  if: always() && needs.deploy-{vertical}-infra.result == 'success'
  runs-on: ubuntu-latest
  timeout-minutes: 5

  steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
        aws-region: us-east-1

    - name: Setup ACM validation ({vertical})
      env:
        CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        CLOUDFLARE_ZONE_ID: ${{ secrets.CLOUDFLARE_ZONE_ID }}
        STACK_NAME: silvermoat-{vertical}
      run: |
        echo "Setting up ACM certificate DNS validation for {vertical}..."
        chmod +x scripts/setup-acm-validation.sh
        ./scripts/setup-acm-validation.sh || echo "⚠️ ACM validation setup failed or not needed"

    - name: Update Cloudflare DNS ({vertical})
      env:
        CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        CLOUDFLARE_ZONE_ID: ${{ secrets.CLOUDFLARE_ZONE_ID }}
        STACK_NAME: silvermoat-{vertical}
        DOMAIN_NAME: silvermoat.net
      run: |
        echo "Running smart DNS update for {vertical}..."
        chmod +x scripts/update-cloudflare-dns.sh
        ./scripts/update-cloudflare-dns.sh
```

### 5.4 Add UI deployment job

```yaml
deploy-{vertical}-ui:
  name: Deploy {Vertical} UI
  needs: [detect-changes, deploy-{vertical}-infra, configure-{vertical}-dns]  # omit DNS for test
  if: |
    always() &&
    (needs.deploy-{vertical}-infra.result == 'success' || needs.deploy-{vertical}-infra.result == 'skipped') &&
    (needs.configure-{vertical}-dns.result == 'success' || needs.configure-{vertical}-dns.result == 'skipped') &&
    (needs.deploy-{vertical}-infra.result == 'success' || needs.detect-changes.outputs.ui_changed == 'true')
  runs-on: ubuntu-latest
  timeout-minutes: 10

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

### 5.5 Update cleanup-test matrix (production workflow)

Add vertical to cleanup matrix:
```yaml
strategy:
  matrix:
    vertical: [insurance, retail, {vertical}, landing]
```

### 5.6 Update deploy-landing-ui dependencies

Add vertical to needs array:
```yaml
deploy-landing-ui:
  needs: [..., deploy-{vertical}-ui]
```

Add vertical check to if condition:
```yaml
if: |
  ...
  (needs.deploy-{vertical}-ui.result == 'success' || needs.deploy-{vertical}-ui.result == 'skipped')
```

## 6. E2E Tests

**Update Landing Page Tests** (`tests/e2e/tests/test_landing_workflows.py`)

Update `test_landing_vertical_cards_visible()` to check for new vertical:
```python
assert "{vertical}" in page_source, "{Vertical} vertical should be displayed"

# Update button count
assert len(enter_portal_elements) >= N  # N = number of verticals
```

Add vertical-specific link test:
```python
@pytest.mark.e2e
@pytest.mark.landing
def test_landing_{vertical}_link(driver, landing_base_url):
    """Test {vertical} card has working link"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    enter_portal_links = driver.find_elements(By.XPATH, "//a[contains(., 'Enter Portal')][@href]")
    all_hrefs = [link.get_attribute('href') for link in enter_portal_links]

    {vertical}_links = [href for href in all_hrefs if href and '{vertical}' in href.lower()]
    assert len({vertical}_links) > 0, f"Should have {vertical} link. Found links: {all_hrefs}"

    href = {vertical}_links[0]
    assert href and len(href) > 0, "{Vertical} link should have valid href"
    assert href.startswith('http'), f"{Vertical} link should be absolute URL, got: {href}"
```

## 7. File Checklist

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
- [ ] Update `.github/workflows/deploy-test.yml` (5 changes: detect-changes, deploy-infra, deploy-ui, cleanup-test, landing-ui)
- [ ] Update `.github/workflows/deploy-production.yml` (6 changes: detect-changes, deploy-infra, configure-dns, deploy-ui, cleanup-test, landing-ui)
- [ ] Update `tests/e2e/tests/test_landing_workflows.py`

## 8. Color Scheme Conventions

- **Insurance**: Blue (`#003d82`, `#667eea → #764ba2` gradient)
- **Retail**: Purple (`#722ed1`, `#722ed1 → #531dab` gradient)
- **Healthcare**: Green (`#52c41a`, `#52c41a → #389e0d` gradient)
- **Pattern**: Choose distinct brand color, create gradient variants for consistency

## 9. Infrastructure Requirements

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

## 10. Example: Adding "Healthcare" Vertical

### Step-by-step implementation:

1. **Create UI structure**: Copy `ui-retail/` → `ui-healthcare/`
2. **Update branding**: Green theme (#52c41a), MedicineBoxOutlined icon, Patient/Staff portals
3. **Generate diagrams**: Add `generate_healthcare_only_*_diagram()` functions to script
4. **Update deployment**: Add healthcare block to `deploy-ui.sh` with bucket/API retrieval
5. **Update main landing**: Add Healthcare card to grid with green theme
6. **Update landing viewer**: Add 7 healthcare features, update database count (21 tables)
7. **Update test workflow**: Add detect-changes output, deploy-healthcare-infra, deploy-healthcare-ui, update cleanup-test matrix, update landing-ui dependencies
8. **Update production workflow**: Same as test + add configure-healthcare-dns job
9. **Update E2E tests**: Add healthcare to `test_landing_vertical_cards_visible()` and add `test_landing_healthcare_link()`
10. **Deploy infrastructure**: Create CDK stack and deploy via `VERTICAL=healthcare ./scripts/deploy-stack.sh`
11. **Deploy UI**: Run `VERTICAL=healthcare ./scripts/deploy-ui.sh`

**Complete checklist reference**: See section 7 above.

**Estimated effort:** 4-6 hours for UI and workflows (following this template). Infrastructure (CDK) adds 2-4 hours.

## 11. Common Pitfalls

### Workflow dependency errors
- **Problem**: `Job 'deploy-{vertical}-ui' depends on unknown job 'deploy-{vertical}-infra'`
- **Solution**: Must add BOTH `deploy-{vertical}-infra` AND `configure-{vertical}-dns` jobs before adding UI job

### Missing stack detection
- **Problem**: Infrastructure job doesn't run when stack doesn't exist
- **Solution**: Add `{vertical}_stack_exists` output to detect-changes job AND add stack check in check-stacks step

### Landing UI circular dependency
- **Problem**: `Job 'deploy-landing-ui' depends on job 'deploy-{vertical}-ui' which creates a cycle`
- **Solution**: Add `(needs.deploy-{vertical}-ui.result == 'success' || needs.deploy-{vertical}-ui.result == 'skipped')` to landing-ui if condition

### E2E test count mismatch
- **Problem**: Tests expect wrong number of "Enter Portal" buttons
- **Solution**: Update assertion to `>= N` where N = total number of verticals
