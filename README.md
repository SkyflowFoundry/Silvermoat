# Silvermoat MVP - E2E Demo Project

A one-shot deployable insurance MVP demo built on AWS CloudFormation, featuring a React SPA frontend and serverless backend.

## Overview

Silvermoat is a complete end-to-end demo MVP that showcases:

- **Infrastructure as Code**: CloudFormation template for all AWS resources
- **Static Website Hosting**: S3 website hosting (no CloudFront required for demo)
- **Serverless API**: API Gateway REST API proxying to a single Lambda function
- **Data Storage**: DynamoDB tables for domain entities (quotes, policies, claims, payments, cases)
- **Document Storage**: S3 bucket for documents/attachments
- **Notifications**: SNS topic for demo notifications
- **Automated Cleanup**: Custom Resource Lambda that empties buckets on stack deletion

## Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  S3 Website │      │ API Gateway  │─────▶│   Lambda    │
│   (UI)      │      │   (REST)     │      │  (Handler)  │
└─────────────┘      └──────────────┘      └──────┬──────┘
                                                    │
       ┌───────────────────────────────────────────┼─────────────┐
       │                                           │             │
       ▼                                           ▼             ▼
┌─────────────┐                          ┌─────────────┐  ┌─────────────┐
│   S3 Docs   │                          │  DynamoDB   │  │     SNS     │
│   Bucket    │                          │   Tables    │  │    Topic    │
└─────────────┘                          └─────────────┘  └─────────────┘
```

## Project Structure

```
Silvermoat/
├── infra/
│   └── silvermoat-mvp-s3-website.yaml  # CloudFormation template
├── ui/
│   ├── package.json                    # React/Vite dependencies
│   ├── vite.config.js                  # Vite build configuration
│   ├── index.html                      # HTML entry point
│   ├── src/
│   │   ├── main.jsx                    # React entry point
│   │   ├── App.jsx                     # Main app component with providers
│   │   ├── config/                     # Configuration files
│   │   │   ├── theme.js                # Ant Design theme customization
│   │   │   ├── routes.jsx              # Route definitions with lazy loading
│   │   │   └── constants.js            # Application constants
│   │   ├── contexts/                   # React Context providers
│   │   │   └── AppContext.jsx          # Global UI state
│   │   ├── hooks/                      # Custom React hooks
│   │   │   ├── queries/                # React Query hooks (data fetching)
│   │   │   └── mutations/              # React Query mutation hooks
│   │   ├── services/                   # API client services
│   │   │   ├── api.js                  # Generic API functions
│   │   │   ├── quotes.js               # Quote-specific API
│   │   │   ├── policies.js             # Policy-specific API
│   │   │   ├── claims.js               # Claim-specific API
│   │   │   ├── payments.js             # Payment-specific API
│   │   │   └── cases.js                # Case-specific API
│   │   ├── components/                 # React components
│   │   │   ├── layout/                 # Layout components
│   │   │   │   ├── AppLayout.jsx       # Main layout wrapper
│   │   │   │   ├── Header.jsx          # Top navigation
│   │   │   │   ├── Sidebar.jsx         # Left sidebar navigation
│   │   │   │   └── Breadcrumbs.jsx     # Breadcrumb navigation
│   │   │   └── common/                 # Reusable components
│   │   │       ├── StatusTag.jsx       # Status badges
│   │   │       ├── EmptyState.jsx      # Empty state component
│   │   │       ├── ErrorBoundary.jsx   # Error boundary
│   │   │       └── LoadingSpinner.jsx  # Loading component
│   │   ├── pages/                      # Page components
│   │   │   ├── Dashboard/              # Dashboard page
│   │   │   ├── Quotes/                 # Quote management
│   │   │   ├── Policies/               # Policy management
│   │   │   ├── Claims/                 # Claim management
│   │   │   ├── Payments/               # Payment management
│   │   │   └── Cases/                  # Case management
│   │   └── utils/                      # Utility functions
│   │       ├── formatters.js           # Date, currency formatting
│   │       ├── seedData.js             # Demo data seeding utility
│   │       └── validators.js           # Custom validators
│   └── dist/                           # Build output (generated)
├── scripts/
│   ├── deploy-stack.sh                 # Deploy CloudFormation stack
│   ├── delete-stack.sh                 # Delete stack
│   ├── get-outputs.sh                  # Get stack outputs
│   ├── deploy-ui.sh                    # Build and deploy UI
│   ├── deploy-all.sh                   # Deploy infrastructure + UI
│   ├── redeploy-all.sh                 # Delete and redeploy everything
│   └── smoke-test.sh                   # Run smoke tests
└── README.md                           # This file
```

## Prerequisites

- **AWS CLI** configured with appropriate credentials
- **AWS Permissions** to create:
  - S3 buckets and policies
  - Lambda functions and IAM roles
  - API Gateway REST APIs
  - DynamoDB tables
  - SNS topics
  - EventBridge events
  - CloudFormation stacks
- **Node.js** 18+ for building the React app
- **npm** or **yarn** for package management
- **jq** (optional, for JSON parsing in scripts)

## Quick Start

### 1. Deploy Infrastructure

Deploy the CloudFormation stack:

```bash
./scripts/deploy-stack.sh
```

Or with custom parameters:

```bash
STACK_NAME=my-silvermoat \
APP_NAME=silvermoat \
STAGE_NAME=prod \
UI_SEEDING_MODE=external \
./scripts/deploy-stack.sh
```

**Parameters:**
- `STACK_NAME`: CloudFormation stack name (default: `silvermoat`)
- `APP_NAME`: Short app name for resource naming (default: `silvermoat`)
- `STAGE_NAME`: API Gateway stage name (default: `demo`)
- `API_DEPLOYMENT_TOKEN`: Token to force API redeployment (default: `v1`)
- `UI_SEEDING_MODE`: `seeded` (Lambda uploads simple HTML) or `external` (React SPA) (default: `external`)

Wait for `CREATE_COMPLETE` status.

### 2. Get Stack Outputs

View stack outputs:

```bash
./scripts/get-outputs.sh
```

Key outputs:
- `WebUrl`: S3 website URL (HTTP)
- `ApiBaseUrl`: API Gateway base URL (HTTPS)
- `UiBucketName`: S3 bucket for UI assets
- `DocsBucketName`: S3 bucket for documents

### 3. Deploy UI

Build and deploy the React SPA:

```bash
./scripts/deploy-ui.sh
```

This will:
1. Install npm dependencies
2. Build the React app
3. Sync to S3 with proper cache headers
4. Display the website URL

### 4. Verify Deployment

Run smoke tests:

```bash
./scripts/smoke-test.sh
```

Or manually test:
- Open the `WebUrl` in a browser
- Create a quote using the form
- Check API responses

## API Endpoints

The API supports basic CRUD operations:

### Create Quote
```bash
POST /quote
Content-Type: application/json

{
  "name": "Jane Doe",
  "zip": "33431"
}
```

### Get Quote
```bash
GET /quote/{id}
```

### Create Other Entities
```bash
POST /policy
POST /claim
POST /payment
POST /case
```

### Update Claim Status
```bash
POST /claim/{id}/status
Content-Type: application/json

{
  "status": "APPROVED"
}
```

### Attach Document to Claim
```bash
POST /claim/{id}/doc
Content-Type: application/json

{
  "text": "Document content"
}
```

## Development

### Local UI Development

Start the Vite dev server:

```bash
cd ui
npm install
npm run dev
```

The UI will be available at `http://localhost:5173`.

**Note**: You'll need to configure the API base URL. Either:
1. Set `VITE_API_BASE_URL` environment variable
2. Or modify `ui/src/App.jsx` to use your deployed API URL

### Building UI

Build for production:

```bash
cd ui
npm run build
```

Output will be in `ui/dist/`.

## UI Architecture

### Technology Stack

The Silvermoat UI is a modern React SPA built with:

- **React 18**: Functional components with hooks
- **React Router v6**: Client-side routing with lazy loading
- **React Query (TanStack Query v5)**: Server state management, caching, and mutations
- **Ant Design v5**: Enterprise-focused component library
- **Vite**: Fast build tool and dev server
- **dayjs**: Lightweight date library

### Design System

**Insurance Industry Standard**: Conservative, trustworthy, data-dense professional interface

**Colors**:
- Primary Blue: `#003d82` (trust, stability)
- Primary Dark: `#002855` (header/footer)
- Accent Gold: `#c5a572` (premium feel)
- Success Green: `#52c41a` (approved)
- Error Red: `#ff4d4f` (denied)
- Warning Orange: `#faad14` (pending)

**Typography**: Inter, Segoe UI, system-ui fallback

**Spacing**: 8px grid system (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px)

### State Management

**Server State (React Query)**:
- All API data fetching and mutations
- Automatic caching with 5-minute stale time
- Optimistic updates for better UX
- Query hooks in `hooks/queries/`
- Mutation hooks in `hooks/mutations/`

**Client State (Context API)**:
- UI state (sidebar collapsed, filters)
- Global app state via `AppContext`
- No Redux/Zustand needed for this complexity level

### Component Patterns

Every entity follows the same consistent pattern:

**1. EntityList.jsx** - Page wrapper
```jsx
- Manages local state for created entities
- Shows/hides form based on route
- Renders EntityTable and EntityForm
```

**2. EntityTable.jsx** - Data table
```jsx
- Ant Design Table with sorting, filtering, pagination
- Status filters using Ant Design filters
- Clickable rows for navigation
- Action buttons for common operations
```

**3. EntityForm.jsx** - Create form
```jsx
- Ant Design Form with validation
- Uses React Query mutation hooks
- Success callback adds to local state
- Form reset on success
```

**4. EntityDetail.jsx** - Detail view
```jsx
- Uses React Query for data fetching
- Ant Design Descriptions for structured data
- Loading and error states
- Navigation to related entities
```

### How to Add a New Entity

Follow these steps to add a new entity type (e.g., "Document"):

#### 1. Add API Service (`services/documents.js`)
```javascript
import { createEntity, getEntity } from './api';

const DOMAIN = 'document';

export const createDocument = (data) => createEntity(DOMAIN, data);
export const getDocument = (id) => getEntity(DOMAIN, id);
```

#### 2. Add React Query Hooks

**Query Hook** (`hooks/queries/useDocument.js`):
```javascript
import { useQuery } from '@tanstack/react-query';
import { getDocument } from '../../services/documents';

export const useDocument = (id, options = {}) => {
  return useQuery({
    queryKey: ['documents', id],
    queryFn: () => getDocument(id),
    enabled: !!id,
    ...options,
  });
};
```

**Mutation Hook** (`hooks/mutations/useCreateDocument.js`):
```javascript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createDocument } from '../../services/documents';

export const useCreateDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createDocument(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      message.success('Document created successfully');
    },
    onError: (error) => {
      message.error(`Failed to create document: ${error.message}`);
    },
  });
};
```

#### 3. Add Constants (`config/constants.js`)
```javascript
export const DOCUMENT_STATUS_OPTIONS = [
  { label: 'Draft', value: 'DRAFT', color: 'default' },
  { label: 'Published', value: 'PUBLISHED', color: 'success' },
  { label: 'Archived', value: 'ARCHIVED', color: 'error' },
];
```

#### 4. Create Page Components

**DocumentTable.jsx**:
```javascript
// Follow the pattern from PaymentTable.jsx
// Add columns for your entity's fields
// Include status filters if applicable
```

**DocumentForm.jsx**:
```javascript
// Follow the pattern from PaymentForm.jsx
// Add Form.Items for each required field
// Use appropriate Ant Design input components
// Call useCreateDocument mutation hook
```

**DocumentDetail.jsx**:
```javascript
// Follow the pattern from PaymentDetail.jsx
// Use useDocument query hook
// Display fields in Descriptions component
// Add navigation to related entities
```

**DocumentList.jsx**:
```javascript
// Follow the pattern from PaymentList.jsx
// Manage form visibility and table display
// Handle success callback to update local state
```

#### 5. Add Routes (`config/routes.jsx`)
```javascript
const DocumentList = lazy(() => import('../pages/Documents/DocumentList'));
const DocumentDetail = lazy(() => import('../pages/Documents/DocumentDetail'));

// Add to routes array:
{
  path: '/documents',
  element: <DocumentList />,
  breadcrumb: 'Documents',
},
{
  path: '/documents/new',
  element: <DocumentList />,
  breadcrumb: 'New Document',
},
{
  path: '/documents/:id',
  element: <DocumentDetail />,
  breadcrumb: 'Document Detail',
},
```

#### 6. Add Navigation (`config/constants.js`)
```javascript
export const NAV_ITEMS = [
  // ... existing items
  {
    key: 'documents',
    label: 'Documents',
    path: '/documents',
    icon: 'FileOutlined',
  },
];
```

#### 7. Update StatusTag (if needed) (`components/common/StatusTag.jsx`)
```javascript
// Add color mapping for your entity's statuses
const getStatusColor = (type, value) => {
  // ... existing mappings
  if (type === 'document') {
    const colorMap = {
      DRAFT: 'default',
      PUBLISHED: 'success',
      ARCHIVED: 'error',
    };
    return colorMap[value] || 'default';
  }
  // ...
};
```

### Demo Data Seeding

The Dashboard includes a "Seed Demo Data" button that creates realistic demo records:

- **Interconnected Data**: Policies reference quotes, claims reference policies, etc.
- **Realistic Values**: Names, dates, amounts, statuses with proper distributions
- **Progress Tracking**: Modal shows progress as entities are created
- **Auto Refresh**: Page reloads after seeding to display new data

**Seed Data Location**: `utils/seedData.js`

To customize seed data:
1. Edit templates in `seedData.js`
2. Adjust quantities in the `seedDemoData` function
3. Modify relationship logic as needed

### Best Practices

**Component Organization**:
- One component per file
- Use functional components with hooks
- Follow the established entity pattern
- Keep components focused and reusable

**State Management**:
- Use React Query for all API data
- Use Context API for UI state only
- Keep local component state minimal
- Avoid prop drilling with Context

**Styling**:
- Use Ant Design components for consistency
- Customize via `config/theme.js`
- Use inline styles sparingly (layout only)
- Follow the insurance industry color palette

**Error Handling**:
- ErrorBoundary catches React errors
- React Query handles API errors
- Show user-friendly messages via Ant Design message/notification
- Log errors to console in development

**Performance**:
- Routes are lazy-loaded via React.lazy()
- React Query caches API responses
- Tables use pagination (default 20 items)
- Large lists use virtualization if needed

## Stack Deletion

Delete the entire stack:

```bash
./scripts/delete-stack.sh
```

**Important**: The stack includes automatic cleanup that:
- Empties both S3 buckets (including all versions and delete markers)
- Wipes all DynamoDB table items
- Ensures buckets are empty before CloudFormation attempts deletion

If deletion fails with "bucket not empty", check CloudWatch logs for the `SeederFunction` Lambda to see if cleanup completed successfully.

## Troubleshooting

### Stack Creation Fails

**Issue**: Custom Resource fails during stack creation

**Solution**:
1. Check CloudWatch logs for `SeederFunction`:
   ```bash
   aws logs tail /aws/lambda/<stack-name>-SeederFunction-<id> --follow
   ```
2. Verify IAM permissions are correct
3. Check that all dependencies are created before the Custom Resource runs

### UI Not Loading

**Issue**: S3 website returns 403 or 404

**Solution**:
1. Verify `UiBucketPolicy` allows public read access
2. Check that `index.html` exists in the bucket:
   ```bash
   aws s3 ls s3://<ui-bucket-name>/
   ```
3. Ensure website hosting is enabled on the bucket

### API Returns CORS Errors

**Issue**: Browser shows CORS errors when calling API

**Solution**: The Lambda function includes CORS headers. If issues persist:
1. Check Lambda logs for errors
2. Verify API Gateway integration is `AWS_PROXY`
3. Ensure the request includes proper headers

### Stack Deletion Stuck on Buckets

**Issue**: Stack deletion fails because buckets are not empty

**Solution**:
1. Check CloudWatch logs for `SeederFunction` cleanup execution
2. Verify the cleanup Lambda has permissions to delete objects
3. Manually empty buckets if needed (shouldn't be necessary):
   ```bash
   aws s3 rm s3://<bucket-name> --recursive
   ```

### React App Can't Find API

**Issue**: UI shows "API base URL not configured"

**Solution**:
1. Ensure `deploy-ui.sh` sets `VITE_API_BASE_URL` during build
2. Or manually set it in `ui/src/App.jsx`
3. Or set `window.API_BASE_URL` in `ui/index.html` before the app loads

## Configuration

### Environment Variables

Scripts support the following environment variables:

- `STACK_NAME`: CloudFormation stack name (default: `silvermoat`)
- `APP_NAME`: App name for resource naming (default: `silvermoat`)
- `STAGE_NAME`: API Gateway stage (default: `demo`)
- `API_DEPLOYMENT_TOKEN`: API deployment token (default: `v1`)
- `UI_SEEDING_MODE`: UI seeding mode (default: `external`)

### CloudFormation Parameters

The template accepts these parameters:

- `AppName`: Short app name used in resource naming
- `StageName`: API Gateway stage name (must match `^[a-zA-Z0-9_-]+$`)
- `ApiDeploymentToken`: Change to force API Gateway redeployment
- `UiSeedingMode`: `seeded` (Lambda uploads HTML) or `external` (deploy separately)

## Important Notes

1. **S3 Website Endpoints**: The S3 website endpoint is HTTP, not HTTPS. This is fine for demo purposes but not suitable for production.

2. **DynamoDB Data Types**: DynamoDB does not accept Python `float` types. Use integers (e.g., `premium_cents: 12550`) or `Decimal` type.

3. **API Gateway Deployment**: When you modify API Gateway methods, change the `ApiDeploymentToken` parameter to force a new deployment.

4. **Bucket Cleanup**: The cleanup Lambda handles:
   - All object versions (if versioning was ever enabled)
   - Delete markers
   - Current objects
   - Empty buckets gracefully

5. **CORS Headers**: The Lambda function returns CORS headers to allow browser requests from the S3 website.

## License

This is a demo project for educational purposes.

## Support

For issues or questions:
1. Check CloudWatch logs for Lambda functions
2. Review CloudFormation stack events
3. Run `smoke-test.sh` to verify basic functionality

