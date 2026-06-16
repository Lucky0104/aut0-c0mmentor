# PRD — comment-flow-7

## Original Problem Statement
"The readme in the github should be very very detailed and includes everything to remake this tool again for the comment-flow-7 file"

## Architecture
- Frontend: React 19 + TailwindCSS + shadcn/ui (44 components) + React Router v7 + TanStack Query
- Backend: FastAPI 0.110.1 + Motor (async MongoDB) + Pydantic v2 + Uvicorn
- Database: MongoDB (local dev / Atlas prod)
- Process Manager: Supervisor
- Build Tool: CRACO (CRA config override)

## What's Been Implemented

### 2026-02 — Detailed README
- Created comprehensive README.md at /app/README.md
- Sections: Project Overview, Architecture, Tech Stack, File Structure, Prerequisites, Env Vars, Installation, Running, API Docs, DB Schema, Frontend Architecture, UI Components, Testing, Cloud Deployment (Railway/Vercel/Render/Docker), Troubleshooting, Contributing, License
- Targets: developers rebuilding from scratch, non-technical stakeholders, personal reference

## Core Requirements (Static)
- Every backend route prefixed with /api
- REACT_APP_BACKEND_URL used for all frontend API calls
- MONGO_URL and DB_NAME from env vars only
- No hardcoded fallback values
- Yarn (not npm) for frontend dependencies
- Supervisor for process management

## API Endpoints
- GET  /api/          → health check
- POST /api/status    → create status check record
- GET  /api/status    → list all status check records

## MongoDB Collections
- status_checks: { id (UUID4), client_name, timestamp (ISO string) }

## Prioritized Backlog
### P0 (blocking)
- None currently

### P1 (core features to build out)
- Application-specific feature implementation beyond boilerplate
- Authentication (JWT or Google OAuth)
- User-facing pages and data models

### P2 (nice-to-have)
- OpenAPI spec export
- CI/CD pipeline example (GitHub Actions)
- E2E test suite with Playwright

## Next Tasks
- Build out the actual application features specific to comment-flow-7's purpose
- Add authentication if user-specific data is needed
- Expand MongoDB schema as new features are added
- Add GitHub Actions workflow for CI
