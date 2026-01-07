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

## 6. Lambda Handlers

**CRITICAL: Must be created BEFORE CDK stack, or CDK deployment will fail**

CDK expects Lambda code at `lambda/{vertical}/` when creating the infrastructure. If this directory doesn't exist, CDK synth/deploy will fail with "Cannot find asset" error.

### 6.1 Create Lambda handler directory

Create `lambda/{vertical}/` with these files:

**__init__.py** - Module initialization:
```python
"""Healthcare vertical Lambda handlers"""
```

**entities.py** - Business logic for domain operations:
```python
"""Shared business logic for healthcare domain operations"""

def upsert_patient_for_appointment(storage, body):
    """Extract patient data and upsert patient record"""
    patient_email = body.get("patientEmail")
    if patient_email:
        patient = storage.upsert_customer(patient_email, {
            "name": body.get("patientName"),
            "email": patient_email
        })
        body.pop("patientName", None)
        body.pop("patientEmail", None)
        return patient["id"]
    return None

# Add similar functions for other domain objects
```

**handler.py** - Main Lambda API handler:
```python
"""Healthcare vertical API handler"""
import json
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from entities import upsert_patient_for_appointment
from chatbot import handle_chat as handle_healthcare_chat
from customer_chatbot import handle_customer_chat as handle_patient_chat

# Domain mapping: healthcare names -> DynamoDB table env vars
HEALTHCARE_DOMAIN_MAPPING = {
    "patient": "CUSTOMERS_TABLE",
    "appointment": "QUOTES_TABLE",       # Reuse quotes table
    "medical_record": "POLICIES_TABLE",  # Reuse policies table
    "prescription": "CLAIMS_TABLE",      # Reuse claims table
    "billing": "PAYMENTS_TABLE",
    "case": "CASES_TABLE"
}

storage = DynamoDBBackend(domain_mapping=HEALTHCARE_DOMAIN_MAPPING)
HEALTHCARE_ENTITIES = ["patient", "appointment", "medical_record", "prescription", "billing", "case"]

def handler(event, context):
    """Main Lambda handler for Healthcare vertical API"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    # POST /chat -> staff chatbot
    if path == "chat" and method == "POST":
        return handle_healthcare_chat(event, storage)

    # POST /customer-chat -> patient chatbot
    if path == "customer-chat" and method == "POST":
        return handle_patient_chat(event, storage)

    # Parse body
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {"raw": event["body"]}

    parts = [p for p in path.split("/") if p]

    # Root endpoint
    if not parts:
        return _resp(200, {
            "name": "Silvermoat Healthcare",
            "vertical": "healthcare",
            "endpoints": [f"/{e}" for e in HEALTHCARE_ENTITIES] + ["/chat", "/customer-chat"]
        })

    domain = parts[0]

    # Validate domain
    if domain not in HEALTHCARE_ENTITIES:
        return _resp(404, {"error": "unknown_domain", "domain": domain})

    # GET /{domain} -> list all
    if method == "GET" and len(parts) == 1:
        items = storage.list(domain)
        return _resp(200, {"items": items, "count": len(items)})

    # POST /{domain} -> create
    if method == "POST" and len(parts) == 1:
        default_status = {"patient": "ACTIVE", "appointment": "SCHEDULED"}.get(domain, "PENDING")

        if domain == "patient":
            patient_email = body.get("email")
            if patient_email:
                item = storage.upsert_customer(patient_email, body)
            else:
                item = storage.create(domain, body, default_status)
        else:
            item = storage.create(domain, body, default_status)

        _emit(f"{domain}.created", {"id": item["id"]})
        return _resp(201, {"id": item["id"], "item": item})

    # GET /{domain}/{id} -> read
    if method == "GET" and len(parts) == 2:
        item = storage.get(domain, parts[1])
        if not item:
            return _resp(404, {"error": "not_found"})
        return _resp(200, item)

    # DELETE /{domain}/{id} -> delete
    if method == "DELETE" and len(parts) == 2:
        storage.delete(domain, parts[1])
        return _resp(200, {"deleted": True})

    return _resp(400, {"error": "unsupported_operation"})
```

**chatbot.py** - Staff chatbot using Bedrock:
```python
"""Healthcare staff chatbot using AWS Bedrock"""
import boto3
from shared.responses import _resp

bedrock = boto3.client("bedrock-runtime")
BEDROCK_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

TOOLS = [
    {
        "name": "search_appointments",
        "description": "Search appointments by patient name or date",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string"},
                "date": {"type": "string"}
            }
        }
    },
    # Add more tools as needed
]

def execute_tool(tool_name, tool_input, storage):
    """Execute tool and return results"""
    if tool_name == "search_appointments":
        items = storage.scan("appointment")
        # Filter logic here
        return {"results": items[:10]}
    return {"error": "Unknown tool"}

def handle_chat(event, storage):
    """Handle staff chatbot requests"""
    body = json.loads(event.get("body", "{}"))
    user_message = body.get("message", "")

    # Use Bedrock converse API with tools
    response = bedrock.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[{"role": "user", "content": user_message}],
        system=[{"text": "You are a healthcare staff assistant..."}],
        toolConfig={"tools": [{"toolSpec": tool} for tool in TOOLS]}
    )

    # Process response and tool calls
    # Return final response
```

**customer_chatbot.py** - Patient chatbot:
```python
"""Healthcare patient chatbot using AWS Bedrock"""
# Similar to chatbot.py but with patient-scoped tools
# - search_my_appointments
# - search_my_prescriptions
# - view_billing
# All tools filtered by patient email for privacy
```

### 6.2 Domain entity mapping

Each vertical reuses the same DynamoDB tables with different semantics:

| Healthcare Entity | DynamoDB Table | Insurance Equivalent | Retail Equivalent |
|-------------------|----------------|---------------------|-------------------|
| patient | CUSTOMERS_TABLE | customer | customer |
| appointment | QUOTES_TABLE | quote | product |
| medical_record | POLICIES_TABLE | policy | order |
| prescription | CLAIMS_TABLE | claim | inventory |
| billing | PAYMENTS_TABLE | payment | payment |
| case | CASES_TABLE | case | case |

### 6.3 Testing Lambda handlers locally

Before deploying, test handler locally:
```bash
cd lambda/{vertical}
python3 -c "import handler; print(handler.handler({'path': '/', 'httpMethod': 'GET'}, {}))"
```

## 7. CDK Infrastructure Stack

**CRITICAL: Lambda handlers must exist (section 6) before CDK can deploy**

### 7.1 Create vertical stack file

Create `cdk/stacks/{vertical}_stack.py` following the pattern from `retail_stack.py`:

```python
"""Healthcare vertical CDK stack - completely independent"""
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as lambda_,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
)
from constructs import Construct
from config.base import SilvermoatConfig
from .vertical_stack import VerticalStack


class HealthcareStack(Stack):
    """Healthcare vertical stack - completely self-contained"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        config: SilvermoatConfig,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Healthcare-specific Lambda Layer
        self.layer = lambda_.LayerVersion(
            self,
            "HealthcareLayer",
            code=lambda_.Code.from_asset("../lambda/layer"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            description="Shared utilities for Healthcare Lambda functions",
        )

        # Healthcare Vertical Stack
        self.healthcare = VerticalStack(
            self,
            "HealthcareVertical",
            vertical_name="healthcare",
            app_name=config.app_name,
            stage_name=config.stage_name,
            layer=self.layer,
            api_deployment_token=config.api_deployment_token,
        )

        # CloudFront Distribution (Production Only)
        self.certificate = None
        self.distribution = None

        if config.create_cloudfront and config.domain_name:
            # Determine the domain for this vertical
            if config.domain_name.startswith("*"):
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                cert_domain = f"healthcare.{base_domain}"
            else:
                cert_domain = config.domain_name

            # Create certificate for this vertical
            self.certificate = acm.Certificate(
                self,
                "HealthcareCertificate",
                domain_name=cert_domain,
                validation=acm.CertificateValidation.from_dns(),
            )

            # CloudFront origin pointing to S3 website endpoint
            s3_origin = origins.HttpOrigin(
                self.healthcare.ui_bucket.bucket_website_domain_name,
                protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
            )

            # CloudFront distribution
            self.distribution = cloudfront.Distribution(
                self,
                "HealthcareDistribution",
                default_behavior=cloudfront.BehaviorOptions(
                    origin=s3_origin,
                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                    allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                    cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                ),
                domain_names=[cert_domain],
                certificate=self.certificate,
                minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
                price_class=cloudfront.PriceClass.PRICE_CLASS_100,
                error_responses=[
                    cloudfront.ErrorResponse(
                        http_status=403,
                        response_http_status=200,
                        response_page_path="/index.html",
                    ),
                    cloudfront.ErrorResponse(
                        http_status=404,
                        response_http_status=200,
                        response_page_path="/index.html",
                    ),
                ],
            )

        # Outputs
        CfnOutput(
            self,
            "HealthcareApiUrl",
            value=self.healthcare.api_url,
            description="Healthcare API Base URL",
            export_name=f"{self.stack_name}-HealthcareApiUrl",
        )

        CfnOutput(
            self,
            "HealthcareUiBucketName",
            value=self.healthcare.ui_bucket.bucket_name,
            description="Healthcare UI S3 Bucket",
            export_name=f"{self.stack_name}-HealthcareUiBucketName",
        )

        CfnOutput(
            self,
            "HealthcareUiBucketWebsiteURL",
            value=self.healthcare.ui_bucket.bucket_website_url,
            description="Healthcare UI S3 Website URL",
            export_name=f"{self.stack_name}-HealthcareUiBucketWebsiteURL",
        )

        # WebUrl: Use CloudFront if available, otherwise S3
        web_url = self.healthcare.ui_bucket.bucket_website_url
        if self.distribution:
            web_url = f"https://{self.distribution.distribution_domain_name}"

        CfnOutput(
            self,
            "WebUrl",
            value=web_url,
            description="Healthcare Web URL",
        )

        # CloudFront Outputs (if enabled)
        if self.certificate:
            CfnOutput(
                self,
                "HealthcareCertificateArn",
                value=self.certificate.certificate_arn,
                description="Healthcare ACM Certificate ARN",
                export_name=f"{self.stack_name}-CertificateArn",
            )

        if self.distribution:
            CfnOutput(
                self,
                "HealthcareCloudFrontDistributionId",
                value=self.distribution.distribution_id,
                description="Healthcare CloudFront Distribution ID",
                export_name=f"{self.stack_name}-CloudFrontDistributionId",
            )

        # Custom Domain Output (if configured)
        if config.domain_name:
            if config.domain_name.startswith("*"):
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                CfnOutput(
                    self,
                    "CustomDomainUrl",
                    value=f"https://healthcare.{base_domain}",
                    description="Healthcare vertical custom domain URL",
                )
```

### 7.2 Update CDK app.py

Add healthcare to `cdk/app.py`:

```python
# Add import
from stacks.healthcare_stack import HealthcareStack

# Add deploy variable
deploy_healthcare = vertical is None or vertical == "healthcare"

# Add stack instantiation (after retail, before landing)
if deploy_healthcare:
    healthcare_config = get_config(f"{stack_name}-healthcare", stage_name)
    HealthcareStack(
        app,
        f"{stack_name}-healthcare",
        config=healthcare_config,
        env=env,
    )
```

### 7.3 Key components in vertical stack

The `VerticalStack` (inherited) automatically creates:
- **7 DynamoDB tables**: Patients, Appointments, Prescriptions, Providers, Cases, Conversations, Documents
- **4 Lambda functions**: patient-handler, appointment-handler, documents-handler, ai-handler
- **API Gateway**: REST API with resource-based routes
- **S3 buckets**: UI bucket (website hosting) + documents bucket
- **IAM roles**: Lambda execution roles with least-privilege access

### 7.4 Update deploy-stack.sh

Add vertical deployment block to `scripts/deploy-stack.sh`:

```bash
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "healthcare" ]; then
  echo "→ Deploying Healthcare Stack..."
  cdk deploy "${BASE_STACK_NAME}-healthcare" --require-approval never
  echo "✓ Healthcare stack deployed"
  echo ""
fi
```

## 8. E2E Tests

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

## 8. File Checklist

**Required files:**

### UI Files
- [ ] `ui-{vertical}/package.json` (with dependencies)
- [ ] `ui-{vertical}/src/App.jsx`
- [ ] `ui-{vertical}/src/pages/Landing/Landing.jsx`
- [ ] `ui-{vertical}/src/components/common/ArchitectureViewer.jsx`
- [ ] `ui-{vertical}/public/silvermoat-logo.png`

### Lambda Handler Files (CRITICAL - must exist before CDK)
- [ ] `lambda/{vertical}/__init__.py`
- [ ] `lambda/{vertical}/handler.py`
- [ ] `lambda/{vertical}/entities.py`
- [ ] `lambda/{vertical}/chatbot.py`
- [ ] `lambda/{vertical}/customer_chatbot.py`

### CDK Files
- [ ] Create `cdk/stacks/{vertical}_stack.py`
- [ ] Update `cdk/app.py` (add import, deploy variable, stack instantiation)

### Scripts
- [ ] Update `scripts/generate-architecture-diagram.py`
- [ ] Update `scripts/deploy-ui.sh`
- [ ] Update `scripts/deploy-stack.sh` (add vertical deployment block)

### Main Landing
- [ ] Update `ui-landing/src/pages/Landing/Landing.jsx`
- [ ] Update `ui-landing/src/components/common/ArchitectureViewer.jsx`

### Workflows
- [ ] Update `.github/workflows/deploy-test.yml` (5 changes: detect-changes, deploy-infra, deploy-ui, cleanup-test, landing-ui)
- [ ] Update `.github/workflows/deploy-production.yml` (6 changes: detect-changes, deploy-infra, configure-dns, deploy-ui, cleanup-test, landing-ui)

### Tests
- [ ] Update `tests/e2e/tests/test_landing_workflows.py`

## 9. Color Scheme Conventions

- **Insurance**: Blue (`#003d82`, `#667eea → #764ba2` gradient)
- **Retail**: Purple (`#722ed1`, `#722ed1 → #531dab` gradient)
- **Healthcare**: Green (`#52c41a`, `#52c41a → #389e0d` gradient)
- **Pattern**: Choose distinct brand color, create gradient variants for consistency

## 10. Infrastructure Requirements

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

## 11. Example: Adding "Healthcare" Vertical

### Step-by-step implementation:

1. **Create UI structure**: Copy `ui-retail/` → `ui-healthcare/`
2. **Update branding**: Green theme (#52c41a), MedicineBoxOutlined icon, Patient/Staff portals
3. **Generate diagrams**: Add `generate_healthcare_only_*_diagram()` functions to script
4. **Update deployment**: Add healthcare block to `deploy-ui.sh` with bucket/API retrieval
5. **Update main landing**: Add Healthcare card to grid with green theme
6. **Update landing viewer**: Add 7 healthcare features, update database count (21 tables)
7. **Create Lambda handlers** (CRITICAL - before CDK):
   - Create `lambda/healthcare/` directory
   - Add `__init__.py`, `handler.py`, `entities.py`, `chatbot.py`, `customer_chatbot.py`
   - Define healthcare entities (patient, appointment, medical_record, prescription, billing, case)
   - Implement domain mapping to reuse DynamoDB tables
8. **Create CDK stack**: Create `cdk/stacks/healthcare_stack.py` following retail pattern
9. **Update CDK app**: Add healthcare import, deploy variable, and stack instantiation to `cdk/app.py`
10. **Update deploy-stack.sh**: Add healthcare deployment block with `cdk deploy` command
11. **Update test workflow**: Add detect-changes output, deploy-healthcare-infra, deploy-healthcare-ui, update cleanup-test matrix, update landing-ui dependencies
12. **Update production workflow**: Same as test + add configure-healthcare-dns job
13. **Update E2E tests**: Add healthcare to `test_landing_vertical_cards_visible()` and add `test_landing_healthcare_link()`
14. **Deploy infrastructure**: Run `VERTICAL=healthcare ./scripts/deploy-stack.sh` to create AWS resources
15. **Deploy UI**: Run `VERTICAL=healthcare ./scripts/deploy-ui.sh` to build and upload UI

**Complete checklist reference**: See section 8 above.

**Estimated effort:**
- UI: 2-3 hours
- Lambda handlers: 1-2 hours
- CDK stack: 30-60 minutes
- Workflows: 1-2 hours
- **Total: 5-8 hours** (following this template)

## 12. Common Pitfalls

### Missing Lambda handlers (CRITICAL)
- **Problem**: `Cannot find asset at /path/to/lambda/{vertical}` during CDK deployment
- **Root cause**: Lambda handler directory doesn't exist when CDK tries to package Lambda code
- **Solution**: **ALWAYS create Lambda handlers BEFORE creating CDK stack** (Section 6 before Section 7)
- **Files required**: `__init__.py`, `handler.py`, `entities.py`, `chatbot.py`, `customer_chatbot.py`

### Missing deploy-stack.sh block
- **Problem**: CDK stack exists but infrastructure never deploys in CI/CD
- **Root cause**: `scripts/deploy-stack.sh` doesn't have deployment block for new vertical
- **Solution**: Add `if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "{vertical}" ]; then cdk deploy ... fi` block

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
