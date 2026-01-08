# E2E Test Matrix Parallelization Strategy

## Overview
Split E2E tests into categories (smoke/api/ui/lifecycle) and run them in parallel per vertical using GitHub Actions matrix strategy.

## Test Categories

### Smoke Tests (fast, ~30-60s per vertical)
- Page loads, navigation exists, basic rendering
- No API calls, minimal interactions
- Run on every PR

### API Tests (~2-3min per vertical)
- Create/read/delete via API
- Backend integration, data persistence
- Run on every PR

### UI Tests (~3-4min per vertical)
- Interactive workflows: buttons, forms, modals
- Customer portals, chatbots, data seeding
- Run on every PR

### Lifecycle Tests (~5-7min per vertical)
- Complete user journeys (quote→policy→claim)
- Cross-entity workflows
- Run on main branch merges (optional for PRs)

## Matrix Configuration

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      # Insurance (12 tests total: 2 smoke, 3 api, 4 ui, 1 lifecycle)
      - vertical: insurance
        category: smoke
        deploy_job: deploy-insurance-ui
      - vertical: insurance
        category: api
        deploy_job: deploy-insurance-ui
      - vertical: insurance
        category: ui
        deploy_job: deploy-insurance-ui
      - vertical: insurance
        category: lifecycle
        deploy_job: deploy-insurance-ui

      # Retail (13 tests total: 5 smoke, 5 api, 2 ui, 1 lifecycle)
      - vertical: retail
        category: smoke
        deploy_job: deploy-retail-ui
      - vertical: retail
        category: api
        deploy_job: deploy-retail-ui
      - vertical: retail
        category: ui
        deploy_job: deploy-retail-ui
      - vertical: retail
        category: lifecycle
        deploy_job: deploy-retail-ui

      # Healthcare (11 tests total: 5 smoke, 4 api, 1 ui, 1 lifecycle)
      - vertical: healthcare
        category: smoke
        deploy_job: deploy-healthcare-ui
      - vertical: healthcare
        category: api
        deploy_job: deploy-healthcare-ui
      - vertical: healthcare
        category: ui
        deploy_job: deploy-healthcare-ui
      - vertical: healthcare
        category: lifecycle
        deploy_job: deploy-healthcare-ui

      # Landing (7 tests total: 4 smoke, 3 ui)
      - vertical: landing
        category: smoke
        deploy_job: deploy-landing-ui
      - vertical: landing
        category: ui
        deploy_job: deploy-landing-ui
```

## Benefits

1. **Parallelization**: 14 jobs run concurrently instead of 4 sequential
2. **Fast feedback**: Smoke tests (4 jobs) complete in ~1 min
3. **Targeted reruns**: Failed API tests don't require rerunning UI tests
4. **Resource efficiency**: Lifecycle tests can be main-only
5. **Clear organization**: Failures immediately show which category broke

## Timing Estimates

### PR Workflow (parallel execution):
- Smoke tests: **1 minute** (4 jobs × 30-60s)
- API tests: **3 minutes** (3 jobs × 2-3min)
- UI tests: **4 minutes** (4 jobs × 3-4min)
- **Total PR time: ~4 minutes** (vs 16 minutes sequential)

### Main Branch (adds lifecycle):
- Lifecycle tests: **7 minutes** (3 jobs × 5-7min)
- **Total main time: ~7 minutes** (parallel)

## Test Count Summary

- **Insurance**: 8 → 12 tests (+4 Phase 1)
- **Retail**: 12 → 13 tests (+1 Phase 1)
- **Healthcare**: 6 → 11 tests (+5 Phase 1)
- **Landing**: 7 tests (unchanged)
- **Total**: 33 → 43 tests (+10 Phase 1)

## Implementation

1. ✅ Add api/ui/lifecycle markers to pytest.ini
2. ✅ Tag all existing tests with category markers
3. ✅ Write Phase 1 new tests (10 tests)
4. ✅ Update run-e2e-tests action to support category parameter
5. 🔄 Replace individual test jobs with matrix in deploy-test.yml
6. 🔄 Replace individual test jobs with matrix in deploy-production.yml
7. ⏳ Verify all tests pass in new structure
