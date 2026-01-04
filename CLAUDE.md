# CLAUDE.md

Behavioral guidance for Claude Code when working in this repository.

## Global Rules

- Be extremely concise.
- Sacrifice grammar for concision.
- Prefer bullets over prose.
- No filler. No restating the obvious.

## Planning First

- Never write code until a plan is approved.
- Default to plan mode for non-trivial work.
- Explore the codebase before proposing a plan.
- Identify ambiguities early.

## Plans

Every plan MUST include:
1. Goal (1 line)
2. Assumptions (if any)
3. Phases (numbered)
4. File-level changes per phase
5. Unresolved questions with recommended answers (required)

### Plan Communication
- **Always post final plan to GitHub issue** before requesting approval.
- Create new issue or update existing one.
- Format: Use markdown with task checkboxes for phases.

### Unresolved Questions
- Always include an **Unresolved Questions** section.
- Questions must be concise.
- Ask only what blocks execution.
- Always include recommended answers per question.
- Stop after listing questions.

## Multi-Phase Work

- If work may exceed one context window:
  - Explicitly break into phases, using Github Issues to preserve plan/context.
  - Each phase should be independently executable.
  - Later phases may depend on artifacts from earlier phases.

## Execution

- Do not execute until explicitly told:
  - "Execute phase X"
  - or "Proceed with implementation"
- When executing:
  - Make minimal, correct changes.
  - Leave TODO markers for future phases.
  - Do not refactor unless required.

## Git & GitHub

- Primary interface: GitHub CLI (`gh`)
- **Always use GitHub Issues for plan communication:**
  - Create issue with full plan before requesting approval.
  - Update issue as phases complete.
  - Use task checkboxes (`- [ ]` / `- [x]`) for phases.
  - Persists across context resets.
- Commit messages: One-line summary only.

## Context Discipline

- Avoid unnecessary verbosity.
- Do not repeat earlier content unless asked.
- If context may be stale:
  - Ask to re-read files.
  - Do nothing else.

## If Unsure

- Ask.
- Do not guess.

## Validation Strategy

**Never run local CDK validation.** Use CI/CD pipeline for validation:
- Open PR and monitor GitHub Actions build job
- CDK synth/deploy runs in CI with proper AWS credentials
- Local validation wastes time and requires complex setup

## Testing

**Always add tests for new functionality** that fits existing test categories:

**1. JavaScript Unit Tests** (`ui/src/**/*.test.js`)
- Pure utility functions, data generators, helpers
- Pattern: Vitest, test all exported functions

**2. E2E Tests** (`tests/e2e/tests/*.py`)
- User-facing UI interactions, forms, navigation
- Pattern: Selenium, test all user workflows

**3. API Contract Tests** (`tests/api/test_*.py`)
- API endpoints (CRUD), request/response validation, error handling
- Pattern: One test file per resource
- **IMPORTANT**: New resource/entity = new API contract tests

**Examples:**
- DO: New utility → unit test | New form → E2E test | New API endpoint → contract test
- DON'T: New test framework/environment without justification

**Checklist before completing feature:**
1. UI components? → E2E tests
2. Utility functions? → Unit tests
3. API endpoints? → Contract tests
4. Similar resources have equivalent coverage? → Add tests
