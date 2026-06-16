# comment-flow-7

> A production-ready full-stack web application built on the **Emergent Platform** — React 19 frontend, FastAPI backend, and MongoDB database — designed to be cloned and extended into any product.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Overview](#2-architecture-overview)
3. [Tech Stack](#3-tech-stack)
4. [Complete Project Structure](#4-complete-project-structure)
5. [Prerequisites](#5-prerequisites)
6. [Environment Variables](#6-environment-variables)
7. [Installation & Local Development](#7-installation--local-development)
8. [Running the Application](#8-running-the-application)
9. [API Documentation](#9-api-documentation)
10. [Database Schema](#10-database-schema)
11. [Frontend Architecture](#11-frontend-architecture)
12. [UI Component Library (shadcn/ui)](#12-ui-component-library-shadcnui)
13. [Testing](#13-testing)
14. [Deployment to Cloud](#14-deployment-to-cloud)
15. [Troubleshooting](#15-troubleshooting)
16. [Contributing](#16-contributing)
17. [License](#17-license)

---

## 1. Project Overview

**comment-flow-7** is a full-stack web application scaffolded on the Emergent Platform. It provides a fully wired-up, production-grade starting point that includes:

- A **React 19** single-page application with routing, TailwindCSS, and a complete shadcn/ui design system
- A **FastAPI** (Python) REST API backend with async MongoDB integration via Motor
- A **MongoDB** database with a clean async driver setup
- **Process management** via Supervisor (runs frontend dev server and backend API simultaneously)
- **Hot-reload** on both frontend and backend during development
- A **health-check** plugin system for monitoring webpack compilation status
- A centralised **test ID registry** (`data-testid`) for end-to-end automated testing
- A **TanStack Query** setup on the frontend for server-state management

### What problem does it solve?

Built a lightweight automation system that replies to Instagram and Facebook campaign comments automatically.
No need to spend hours responding manually or pay for expensive tools like ManyChat.
It detects campaign-specific comments and sends the right replies in real time.
Designed for marketers who want faster engagement, lead capture, and hands-free comment management.

---

## 2. Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         Browser / Client                         │
│              React 19 SPA  (port 3000 in dev)                    │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │  React Router v7  │  TanStack Query  │  Axios HTTP       │   │
│   │  shadcn/ui  │  Tailwind CSS  │  Framer Motion            │   │
│   └────────────────────────────┬─────────────────────────────┘   │
└────────────────────────────────│─────────────────────────────────┘
                                 │  HTTP  (all /api/* requests)
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│              Python 3.11  (port 8001 in dev)                     │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │  APIRouter  /api/*  │  CORS Middleware  │  Pydantic v2   │   │
│   │  Motor (async)  │  python-dotenv  │  Uvicorn              │   │
│   └────────────────────────────┬─────────────────────────────┘   │
└────────────────────────────────│─────────────────────────────────┘
                                 │  Motor async driver
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                         MongoDB                                  │
│              (localhost:27017 in dev)                            │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │  Database: test_database  │  Collection: status_checks   │   │
│   └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### Request Routing Rules

| Traffic type | Path pattern | Routed to |
|---|---|---|
| Frontend (React) | Any path **without** `/api` prefix | Port 3000 |
| Backend (FastAPI) | Any path **with** `/api` prefix | Port 8001 |

> **Important:** All backend routes **must** be prefixed with `/api`. The Kubernetes ingress (and local proxy) uses this rule to split traffic. Never register routes directly on the FastAPI `app` object without going through `api_router`.

---

## 3. Tech Stack

### Backend

| Package | Version | Purpose |
|---|---|---|
| Python | 3.11 | Runtime |
| FastAPI | 0.110.1 | Web framework & API router |
| Uvicorn | 0.25.0 | ASGI server |
| Motor | 3.3.1 | Async MongoDB driver |
| PyMongo | 4.5.0 | MongoDB driver (sync utilities) |
| Pydantic | ≥ 2.6.4 | Data validation & settings |
| python-dotenv | ≥ 1.0.1 | `.env` file loading |
| python-jose | ≥ 3.3.0 | JWT tokens |
| bcrypt | 4.1.3 | Password hashing |
| passlib | ≥ 1.7.4 | Password utilities |
| PyJWT | ≥ 2.10.1 | JWT encoding/decoding |
| pandas | ≥ 2.2.0 | Data manipulation |
| numpy | ≥ 1.26.0 | Numerical computation |
| requests | ≥ 2.31.0 | HTTP client (sync) |
| python-multipart | ≥ 0.0.9 | File upload support |
| email-validator | ≥ 2.2.0 | Email validation |
| emergentintegrations | 0.2.0 | Emergent Platform LLM integrations |
| pytest | ≥ 8.0.0 | Testing framework |
| black | ≥ 24.1.1 | Code formatter |
| isort | ≥ 5.13.2 | Import sorter |
| flake8 | ≥ 7.0.0 | Linter |
| mypy | ≥ 1.8.0 | Static type checker |

### Frontend

| Package | Version | Purpose |
|---|---|---|
| Node.js | 20 | Runtime |
| React | 19.0.0 | UI framework |
| React DOM | 19.0.0 | DOM renderer |
| React Router DOM | 7.5.1 | Client-side routing |
| TypeScript | — | JS via CRACO/Babel |
| TailwindCSS | 3.4.17 | Utility-first CSS |
| CRACO | 7.1.0 | CRA config override |
| Axios | 1.8.4 | HTTP client |
| TanStack Query | 5.56.2 | Server-state management |
| Framer Motion | 11.18.0 | Animations |
| lucide-react | 0.516.0 | Icon library |
| shadcn/ui (Radix UI) | various | Headless component primitives |
| Recharts | 3.6.0 | Charts |
| React Hook Form | 7.56.2 | Form state management |
| Zod | 3.24.4 | Schema validation |
| date-fns | 4.1.0 | Date utilities |
| dayjs | 1.11.13 | Date manipulation |
| sonner | 2.0.3 | Toast notifications |
| cmdk | 1.1.1 | Command palette |
| embla-carousel-react | 8.6.0 | Carousel |
| vaul | 1.1.2 | Drawer primitive |
| clsx + tailwind-merge | latest | Class name utilities |
| next-themes | 0.4.6 | Dark/light mode |
| SWR | 2.3.8 | Data fetching (alternative) |
| Yarn | 1.22.22 | Package manager |

### Infrastructure / Tooling

| Tool | Purpose |
|---|---|
| Supervisor | Process manager — runs frontend + backend simultaneously |
| MongoDB (local) | Database (dev) |
| PostCSS + Autoprefixer | CSS processing |
| ESLint + react-hooks plugin | Linting |
| Webpack (via CRACO) | Bundler + dev server |
| @emergentbase/visual-edits | Emergent Platform visual editor overlay (dev only) |

---

## 4. Complete Project Structure

```
/app/
├── README.md                        # This file
├── test_result.md                   # Testing state shared between agents
├── yarn.lock                        # Root-level lock file
│
├── backend/
│   ├── server.py                    # FastAPI application entry point
│   ├── requirements.txt             # Python dependencies (pip freeze)
│   └── .env                        # Backend environment variables (DO NOT COMMIT)
│
├── frontend/
│   ├── package.json                 # Node.js dependencies & scripts
│   ├── yarn.lock                    # Frontend lock file
│   ├── tailwind.config.js           # Tailwind CSS configuration
│   ├── postcss.config.js            # PostCSS (autoprefixer)
│   ├── craco.config.js              # CRACO webpack config override
│   ├── jsconfig.json                # Path aliases (@/ → src/)
│   ├── components.json              # shadcn/ui CLI configuration
│   ├── .env                        # Frontend environment variables (DO NOT COMMIT)
│   │
│   ├── public/
│   │   └── index.html               # HTML template
│   │
│   ├── plugins/
│   │   └── health-check/
│   │       ├── health-endpoints.js  # Dev server health API endpoints
│   │       └── webpack-health-plugin.js  # Webpack build status tracker
│   │
│   └── src/
│       ├── index.js                 # React entry point (QueryClientProvider)
│       ├── App.js                   # Root component + React Router setup
│       ├── App.css                  # App-level styles
│       ├── index.css                # Global styles + Tailwind directives + CSS variables
│       │
│       ├── components/
│       │   └── ui/                  # All shadcn/ui components (44 files)
│       │       ├── accordion.jsx
│       │       ├── alert-dialog.jsx
│       │       ├── alert.jsx
│       │       ├── aspect-ratio.jsx
│       │       ├── avatar.jsx
│       │       ├── badge.jsx
│       │       ├── breadcrumb.jsx
│       │       ├── button.jsx
│       │       ├── calendar.jsx
│       │       ├── card.jsx
│       │       ├── carousel.jsx
│       │       ├── checkbox.jsx
│       │       ├── collapsible.jsx
│       │       ├── command.jsx
│       │       ├── context-menu.jsx
│       │       ├── dialog.jsx
│       │       ├── drawer.jsx
│       │       ├── dropdown-menu.jsx
│       │       ├── form.jsx
│       │       ├── hover-card.jsx
│       │       ├── input-otp.jsx
│       │       ├── input.jsx
│       │       ├── label.jsx
│       │       ├── menubar.jsx
│       │       ├── navigation-menu.jsx
│       │       ├── pagination.jsx
│       │       ├── popover.jsx
│       │       ├── progress.jsx
│       │       ├── radio-group.jsx
│       │       ├── resizable.jsx
│       │       ├── scroll-area.jsx
│       │       ├── select.jsx
│       │       ├── separator.jsx
│       │       ├── sheet.jsx
│       │       ├── skeleton.jsx
│       │       ├── slider.jsx
│       │       ├── sonner.jsx
│       │       ├── switch.jsx
│       │       ├── table.jsx
│       │       ├── tabs.jsx
│       │       ├── textarea.jsx
│       │       ├── toast.jsx
│       │       ├── toaster.jsx
│       │       ├── toggle-group.jsx
│       │       ├── toggle.jsx
│       │       └── tooltip.jsx
│       │
│       ├── constants/
│       │   └── testIds/
│       │       ├── index.js         # Central re-export of all test ID registries
│       │       ├── auth.js          # Test IDs: LOGIN, REGISTER, LOGOUT constants
│       │       └── home.js          # Test IDs: HOME constant
│       │
│       ├── hooks/
│       │   └── use-toast.js         # Toast hook (matches shadcn/ui pattern)
│       │
│       └── lib/
│           └── utils.js             # cn() utility (clsx + tailwind-merge)
│
├── memory/
│   ├── PRD.md                       # Product Requirements Document
│   └── test_credentials.md         # Test account credentials (for testing agent)
│
├── tests/
│   └── __init__.py                  # Python test package initializer
│
└── test_reports/
    └── pytest/                      # Pytest output artifacts
```

---

## 5. Prerequisites

Before you can run this project locally, install the following:

### Required

| Requirement | Minimum version | Install guide |
|---|---|---|
| **Git** | 2.x | https://git-scm.com/downloads |
| **Python** | 3.11 | https://www.python.org/downloads/ |
| **pip** | 23+ | Bundled with Python |
| **Node.js** | 20.x | https://nodejs.org/ |
| **Yarn** | 1.22 | `npm install -g yarn` |
| **MongoDB** | 7.x | https://www.mongodb.com/try/download/community |

### Verify installations

```bash
python3 --version   # Python 3.11.x
pip --version       # pip 23.x
node --version      # v20.x.x
yarn --version      # 1.22.x
mongod --version    # db version v7.x.x
git --version       # git version 2.x.x
```

### Optional (recommended)

- **MongoDB Compass** — GUI for browsing your database: https://www.mongodb.com/products/tools/compass
- **Supervisor** — Production process manager: `sudo apt install supervisor` (Linux) or `brew install supervisor` (macOS)

---

## 6. Environment Variables

### Backend (`/app/backend/.env`)

```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
CORS_ORIGINS="*"
```

| Variable | Required | Description |
|---|---|---|
| `MONGO_URL` | Yes | Full MongoDB connection string. Use `mongodb://localhost:27017` for local, or a MongoDB Atlas URI for production (e.g. `mongodb+srv://user:pass@cluster.mongodb.net/`). |
| `DB_NAME` | Yes | Name of the MongoDB database. The Motor client will create it on first write if it doesn't exist. |
| `CORS_ORIGINS` | Yes | Comma-separated list of allowed CORS origins. Use `*` in development. In production, set to your exact frontend domain: `https://yourdomain.com`. |

### Frontend (`/app/frontend/.env`)

```env
REACT_APP_BACKEND_URL=https://your-preview-url.preview.emergentagent.com
WDS_SOCKET_PORT=443
ENABLE_HEALTH_CHECK=false
```

| Variable | Required | Description |
|---|---|---|
| `REACT_APP_BACKEND_URL` | Yes | The **external** URL of the backend API. All Axios calls in the frontend use this. In local development without a reverse proxy, set to `http://localhost:8001`. On Emergent Platform, this is pre-configured to the public preview URL. |
| `WDS_SOCKET_PORT` | Dev only | Port for Webpack DevServer websocket (hot-reload). Set to `443` when running behind an HTTPS reverse proxy. |
| `ENABLE_HEALTH_CHECK` | Dev only | Set to `true` to enable webpack health-check endpoints at `GET /health` on the dev server. Default `false`. |

> **Security note:** Never commit `.env` files to version control. Both files are already listed in `.gitignore`. Create them from the examples above when setting up a new environment.

---

## 7. Installation & Local Development

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-org/comment-flow-7.git
cd comment-flow-7
```

### Step 2 — Set up the backend

```bash
cd backend

# Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# Install all Python dependencies
pip install -r requirements.txt

# Create the backend .env file
cp .env.example .env              # if an example exists, otherwise create manually
# Edit .env with your values (see Section 6)
```

### Step 3 — Set up the frontend

```bash
cd ../frontend

# Install Node dependencies using Yarn (do NOT use npm — it breaks lockfile)
yarn install

# Create the frontend .env file
# Edit .env with your REACT_APP_BACKEND_URL (see Section 6)
```

### Step 4 — Start MongoDB

```bash
# macOS (Homebrew)
brew services start mongodb-community@7.0

# Linux (systemd)
sudo systemctl start mongod

# Verify it's running
mongosh --eval "db.adminCommand('ping')"
```

---

## 8. Running the Application

### Option A — Run each service separately (simplest for development)

**Terminal 1 — Backend:**

```bash
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 — Frontend:**

```bash
cd frontend
yarn start
# Opens http://localhost:3000 automatically
```

### Option B — Run with Supervisor (mirrors production)

Supervisor manages both processes as background daemons and restarts them on crash.

1. Install Supervisor:
   ```bash
   # macOS
   brew install supervisor

   # Ubuntu/Debian
   sudo apt install supervisor
   ```

2. Create a Supervisor config at `/etc/supervisor/conf.d/comment-flow-7.conf`:
   ```ini
   [program:backend]
   command=/path/to/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
   directory=/path/to/comment-flow-7/backend
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/supervisor/backend.err.log
   stdout_logfile=/var/log/supervisor/backend.out.log
   environment=PATH="/path/to/venv/bin"

   [program:frontend]
   command=yarn start
   directory=/path/to/comment-flow-7/frontend
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/supervisor/frontend.err.log
   stdout_logfile=/var/log/supervisor/frontend.out.log
   environment=NODE_ENV="development",PORT="3000"
   ```

3. Reload Supervisor:
   ```bash
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start all
   ```

4. Check status:
   ```bash
   sudo supervisorctl status
   ```

### Accessing the application

| Service | URL |
|---|---|
| Frontend (React) | http://localhost:3000 |
| Backend API (root) | http://localhost:8001/api/ |
| Backend API docs (Swagger) | http://localhost:8001/docs |
| Backend API docs (ReDoc) | http://localhost:8001/redoc |

> FastAPI automatically generates interactive API documentation at `/docs` and `/redoc` — no extra setup required.

---

## 9. API Documentation

All backend routes are mounted on the `/api` prefix via FastAPI's `APIRouter`.

### Base URL

```
http://localhost:8001/api        (local development)
https://your-domain.com/api     (production)
```

---

### `GET /api/`

Health check — confirms the backend is running.

**Request:**
```bash
curl http://localhost:8001/api/
```

**Response `200 OK`:**
```json
{
  "message": "Hello World"
}
```

---

### `POST /api/status`

Creates a new status check record and persists it to MongoDB.

**Request body:**
```json
{
  "client_name": "string"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `client_name` | string | Yes | Identifier of the client making the check |

**Example:**
```bash
curl -X POST http://localhost:8001/api/status \
  -H "Content-Type: application/json" \
  -d '{"client_name": "my-service"}'
```

**Response `200 OK`:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "client_name": "my-service",
  "timestamp": "2026-02-01T12:34:56.789012+00:00"
}
```

| Field | Type | Description |
|---|---|---|
| `id` | string (UUID4) | Auto-generated unique identifier |
| `client_name` | string | Echoed from the request |
| `timestamp` | ISO 8601 datetime | UTC time of creation |

---

### `GET /api/status`

Returns all status check records stored in MongoDB (up to 1000).

**Example:**
```bash
curl http://localhost:8001/api/status
```

**Response `200 OK`:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "client_name": "my-service",
    "timestamp": "2026-02-01T12:34:56.789012+00:00"
  }
]
```

---

### Error Responses

FastAPI returns standard HTTP error responses with a JSON body:

```json
{
  "detail": "error description here"
}
```

| HTTP Code | Meaning |
|---|---|
| `422 Unprocessable Entity` | Request body failed Pydantic validation |
| `500 Internal Server Error` | Unhandled server-side exception |

---

## 10. Database Schema

### Connection

```
Host:     localhost (dev) / MongoDB Atlas (prod)
Port:     27017
Database: test_database   (set via DB_NAME env var)
```

---

### Collection: `status_checks`

Stores every status check record created via `POST /api/status`.

```json
{
  "_id": ObjectId("..."),           // MongoDB auto-generated (excluded from API responses)
  "id": "550e8400-...",             // UUID4 string — the public-facing ID
  "client_name": "my-service",     // Free-text client name
  "timestamp": "2026-02-01T..."    // ISO 8601 UTC string
}
```

| Field | BSON Type | Required | Description |
|---|---|---|---|
| `_id` | ObjectId | Yes (auto) | Internal MongoDB ID — never exposed in API |
| `id` | String | Yes | UUID4 generated by the app at creation time |
| `client_name` | String | Yes | Client identifier from request body |
| `timestamp` | String | Yes | ISO 8601 UTC timestamp stored as string |

**Index recommendations for production:**

```javascript
// Create an index on client_name for fast lookups
db.status_checks.createIndex({ "client_name": 1 })

// Create a TTL index if you want records to expire automatically
db.status_checks.createIndex({ "timestamp": 1 }, { expireAfterSeconds: 2592000 })
```

---

### Notes on MongoDB + Pydantic

The backend uses a pattern to cleanly separate MongoDB's internal `_id` (ObjectId) from the public API model:

```python
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # drops _id when returned from Mongo
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

The `extra="ignore"` config tells Pydantic to silently discard any keys in the MongoDB document that aren't in the model (including `_id`). This means you can pass a raw Mongo document dict straight into the model without a `from_mongo()` helper.

---

## 11. Frontend Architecture

### Entry Point

`src/index.js` bootstraps the React app:

```jsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,         // data stays fresh for 60s
      refetchOnWindowFocus: false,
    },
  },
});

root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
```

All server-state is managed via **TanStack Query** — wrap your fetch calls in `useQuery` / `useMutation` hooks for automatic caching, background refetch, and loading/error states.

---

### Routing

`src/App.js` uses React Router v7:

```jsx
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
  </Routes>
</BrowserRouter>
```

To add a new page:
1. Create `src/pages/MyPage.js`
2. Import it in `App.js`
3. Add `<Route path="/my-page" element={<MyPage />} />`

---

### Making API Calls

The backend URL is centralised at the top of `App.js`:

```js
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
```

Use Axios for all HTTP requests:

```js
import axios from "axios";
const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

// GET request
const { data } = await axios.get(`${API}/status`);

// POST request
const { data } = await axios.post(`${API}/status`, { client_name: "web" });
```

---

### Path Aliases

The `@` alias maps to `src/` — use it everywhere instead of relative paths:

```js
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { HOME } from "@/constants/testIds";
```

This is configured in both `craco.config.js` (webpack) and `jsconfig.json` (IDE autocomplete).

---

### Styling

The project uses **TailwindCSS utility classes** with a **CSS variables-based design token system** (from shadcn/ui).

**CSS Variables** are defined in `src/index.css` and used by Tailwind:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 3.9%;
  --primary: 0 0% 9%;
  --radius: 0.5rem;
  /* ... */
}
```

Reference them in Tailwind classes:
```jsx
<div className="bg-background text-foreground rounded-lg border border-border" />
```

**Dark mode** is supported out of the box. Toggle the `.dark` class on `<html>` using `next-themes`:

```jsx
import { ThemeProvider, useTheme } from "next-themes";
```

---

### State Management

| Concern | Tool |
|---|---|
| Server state (API data) | TanStack Query (`useQuery`, `useMutation`) |
| Client / UI state | React `useState` / `useReducer` |
| Form state | React Hook Form + Zod |
| Toast notifications | `useToast` hook or Sonner |

---

## 12. UI Component Library (shadcn/ui)

The project ships with **44 pre-installed shadcn/ui components** in `src/components/ui/`. These are built on Radix UI primitives and styled with Tailwind.

**shadcn/ui configuration** (`components.json`):

```json
{
  "style": "new-york",
  "rsc": false,
  "tsx": false,
  "tailwind": {
    "baseColor": "neutral",
    "cssVariables": true
  }
}
```

### Available Components

| Component | Import path | Description |
|---|---|---|
| Accordion | `@/components/ui/accordion` | Expandable content sections |
| AlertDialog | `@/components/ui/alert-dialog` | Modal confirmation dialogs |
| Alert | `@/components/ui/alert` | Inline notification banners |
| AspectRatio | `@/components/ui/aspect-ratio` | Fixed ratio containers |
| Avatar | `@/components/ui/avatar` | User avatar with fallback |
| Badge | `@/components/ui/badge` | Status labels |
| Breadcrumb | `@/components/ui/breadcrumb` | Navigation trail |
| Button | `@/components/ui/button` | Buttons with variants |
| Calendar | `@/components/ui/calendar` | Date picker calendar |
| Card | `@/components/ui/card` | Content card container |
| Carousel | `@/components/ui/carousel` | Image/content slider |
| Checkbox | `@/components/ui/checkbox` | Checkbox input |
| Collapsible | `@/components/ui/collapsible` | Toggle-hide sections |
| Command | `@/components/ui/command` | Command palette / search |
| ContextMenu | `@/components/ui/context-menu` | Right-click menus |
| Dialog | `@/components/ui/dialog` | Modal dialogs |
| Drawer | `@/components/ui/drawer` | Bottom/side drawers |
| DropdownMenu | `@/components/ui/dropdown-menu` | Dropdown menus |
| Form | `@/components/ui/form` | React Hook Form wrapper |
| HoverCard | `@/components/ui/hover-card` | Hover preview cards |
| InputOTP | `@/components/ui/input-otp` | OTP code input |
| Input | `@/components/ui/input` | Text input field |
| Label | `@/components/ui/label` | Form labels |
| Menubar | `@/components/ui/menubar` | Horizontal menu bar |
| NavigationMenu | `@/components/ui/navigation-menu` | Top navigation |
| Pagination | `@/components/ui/pagination` | Page navigation |
| Popover | `@/components/ui/popover` | Floating overlays |
| Progress | `@/components/ui/progress` | Progress bar |
| RadioGroup | `@/components/ui/radio-group` | Radio button group |
| Resizable | `@/components/ui/resizable` | Resizable panels |
| ScrollArea | `@/components/ui/scroll-area` | Custom scrollable area |
| Select | `@/components/ui/select` | Dropdown select |
| Separator | `@/components/ui/separator` | Visual divider |
| Sheet | `@/components/ui/sheet` | Side panel overlay |
| Skeleton | `@/components/ui/skeleton` | Loading placeholder |
| Slider | `@/components/ui/slider` | Range slider |
| Sonner | `@/components/ui/sonner` | Toast via Sonner |
| Switch | `@/components/ui/switch` | Toggle switch |
| Table | `@/components/ui/table` | Data table |
| Tabs | `@/components/ui/tabs` | Tabbed navigation |
| Textarea | `@/components/ui/textarea` | Multi-line text input |
| Toast / Toaster | `@/components/ui/toast` | Toast notification |
| Toggle / ToggleGroup | `@/components/ui/toggle` | Toggle buttons |
| Tooltip | `@/components/ui/tooltip` | Hover tooltips |

### Usage example

```jsx
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Status <Badge variant="outline">Active</Badge></CardTitle>
      </CardHeader>
      <CardContent>
        <Button variant="default" onClick={() => {}}>Submit</Button>
        <Button variant="destructive" className="ml-2">Delete</Button>
      </CardContent>
    </Card>
  );
}
```

### Adding new shadcn/ui components

```bash
cd frontend
npx shadcn@latest add <component-name>
# Example: npx shadcn@latest add data-table
```

---

## 13. Testing

### Test ID System

Every interactive and data-displaying UI element **must** have a `data-testid` attribute. The IDs are centralised in `src/constants/testIds/` so they are never hardcoded as magic strings.

**Registry structure:**

```
src/constants/testIds/
├── index.js       ← re-exports all feature modules
├── auth.js        ← LOGIN, REGISTER, LOGOUT objects
└── home.js        ← HOME object
```

**Adding test IDs for a new feature:**

1. Create `src/constants/testIds/my-feature.js`:
   ```js
   export const MY_FEATURE = {
     submitButton: 'my-feature-submit-button',
     resultText:   'my-feature-result-text',
   };
   ```

2. Re-export from `index.js`:
   ```js
   export * from './my-feature';
   ```

3. Use in JSX:
   ```jsx
   import { MY_FEATURE } from '@/constants/testIds';
   
   <button data-testid={MY_FEATURE.submitButton}>Submit</button>
   <p data-testid={MY_FEATURE.resultText}>{result}</p>
   ```

**Naming convention:**
- Keys: `camelCase`
- Values: `kebab-case` shaped as `<feature>-<element>` or `<feature>-<element>-<qualifier>`

---

### Pre-defined Test IDs

**`auth.js`**

| Export | Key | Value |
|---|---|---|
| `LOGIN` | `emailInput` | `login-email-input` |
| `LOGIN` | `passwordInput` | `login-password-input` |
| `LOGIN` | `submitButton` | `login-submit-button` |
| `LOGIN` | `forgotPasswordLink` | `login-forgot-password-link` |
| `LOGIN` | `registerLink` | `login-register-link` |
| `REGISTER` | `nameInput` | `register-name-input` |
| `REGISTER` | `emailInput` | `register-email-input` |
| `REGISTER` | `passwordInput` | `register-password-input` |
| `REGISTER` | `passwordConfirmInput` | `register-password-confirm-input` |
| `REGISTER` | `submitButton` | `register-submit-button` |
| `REGISTER` | `loginLink` | `register-login-link` |
| `LOGOUT` | `button` | `logout-button` |

**`home.js`**

| Export | Key | Value |
|---|---|---|
| `HOME` | `emergentLink` | `home-emergent-link` |

---

### Running Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Linting & Formatting (Backend)

```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8 .

# Type check
mypy server.py
```

### Linting (Frontend)

```bash
cd frontend
yarn lint        # runs ESLint
```

---

## 14. Deployment to Cloud

### Overview

The application consists of three services that need to be deployed:

1. **MongoDB** — managed database service (recommended)
2. **FastAPI backend** — containerised Python service
3. **React frontend** — static build served via CDN or Node server

---

### Option A — Railway (Recommended for full-stack)

Railway can deploy the backend and frontend as separate services, and provides managed MongoDB.

**Step 1 — Push to GitHub**

```bash
git remote add origin https://github.com/your-org/comment-flow-7.git
git push -u origin main
```

**Step 2 — Create Railway project**

1. Go to https://railway.app and create a new project
2. Click **Deploy from GitHub repo** and select your repository

**Step 3 — Add MongoDB**

1. In the Railway dashboard, click **+ New** → **Database** → **MongoDB**
2. Copy the `MONGO_URL` connection string from the MongoDB service variables

**Step 4 — Configure the backend service**

Set the following environment variables in the backend service:
```
MONGO_URL=<paste from Step 3>
DB_NAME=comment_flow_7
CORS_ORIGINS=https://your-frontend-domain.railway.app
```

Set the start command:
```
uvicorn server:app --host 0.0.0.0 --port $PORT
```

**Step 5 — Configure the frontend service**

Set environment variables:
```
REACT_APP_BACKEND_URL=https://your-backend-service.railway.app
```

Set the build command:
```
cd frontend && yarn install && yarn build
```

Set the start command:
```
npx serve -s frontend/build -l $PORT
```

---

### Option B — Vercel (Frontend) + Render (Backend)

**Frontend → Vercel:**

1. Import your GitHub repo at https://vercel.com/new
2. Set **Root Directory** to `frontend`
3. Set **Build Command** to `yarn build`
4. Set **Output Directory** to `build`
5. Add environment variable: `REACT_APP_BACKEND_URL=https://your-backend.onrender.com`

**Backend → Render:**

1. Create a new **Web Service** at https://render.com
2. Connect your GitHub repo
3. Set **Root Directory** to `backend`
4. Set **Build Command** to `pip install -r requirements.txt`
5. Set **Start Command** to `uvicorn server:app --host 0.0.0.0 --port $PORT`
6. Add environment variables: `MONGO_URL`, `DB_NAME`, `CORS_ORIGINS`

**Database → MongoDB Atlas:**

1. Create a free cluster at https://cloud.mongodb.com
2. Create a database user and whitelist `0.0.0.0/0` (or specific IPs)
3. Copy the connection string and set it as `MONGO_URL` on Render

---

### Option C — Docker (any VPS / AWS EC2 / DigitalOcean)

**`backend/Dockerfile`** (create this file):

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8001
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

**`frontend/Dockerfile`** (create this file):

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
ARG REACT_APP_BACKEND_URL
ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL
RUN yarn build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**`docker-compose.yml`** (create at project root):

```yaml
version: "3.9"

services:
  mongodb:
    image: mongo:7
    volumes:
      - mongo_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: comment_flow_7

  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      MONGO_URL: mongodb://mongodb:27017
      DB_NAME: comment_flow_7
      CORS_ORIGINS: http://localhost:80
    depends_on:
      - mongodb

  frontend:
    build:
      context: ./frontend
      args:
        REACT_APP_BACKEND_URL: http://localhost:8001
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mongo_data:
```

**Run with Docker Compose:**

```bash
docker compose up --build
```

---

### Production Checklist

Before going live, verify:

- [ ] `CORS_ORIGINS` is set to your exact frontend domain (not `*`)
- [ ] `MONGO_URL` points to your production MongoDB Atlas cluster with a strong password
- [ ] `DB_NAME` is set to your production database name
- [ ] `REACT_APP_BACKEND_URL` points to your production backend URL (HTTPS)
- [ ] MongoDB Atlas IP whitelist includes your server IP(s)
- [ ] Supervisor or Docker is configured to auto-restart crashed processes
- [ ] HTTPS is enabled on all public endpoints
- [ ] MongoDB user has minimal required permissions (readWrite on your DB only)
- [ ] Python virtual environment is not committed to version control
- [ ] `.env` files are not committed to version control

---

## 15. Troubleshooting

### Backend won't start

**Symptom:** `uvicorn` crashes immediately with a connection error.

**Diagnosis:**
```bash
# Check MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Check backend logs
tail -n 100 /var/log/supervisor/backend.err.log
```

**Common causes:**
- MongoDB is not running → start it with `brew services start mongodb-community` or `sudo systemctl start mongod`
- `MONGO_URL` or `DB_NAME` is missing from `.env` → the app deliberately has no fallback and will crash fast to surface this
- Port 8001 is already in use → `lsof -i :8001` to find the conflicting process

---

### Frontend can't reach the backend

**Symptom:** API calls fail with `net::ERR_CONNECTION_REFUSED` or CORS errors in the browser console.

**Diagnosis:**
```bash
# Test the API directly
curl http://localhost:8001/api/

# Confirm the env var is set correctly
cat frontend/.env | grep REACT_APP_BACKEND_URL
```

**Common causes:**
- `REACT_APP_BACKEND_URL` is wrong or missing in `frontend/.env`
- The backend is not running
- CORS: `CORS_ORIGINS` in `backend/.env` does not include the frontend origin
- You changed `.env` but didn't restart the frontend (`yarn start` must be restarted after `.env` changes — hot reload does not pick up env var changes)

---

### CORS error on POST/PUT/DELETE

**Symptom:** `Access-Control-Allow-Origin` header missing or blocked.

**Fix:** Add the exact frontend origin to `CORS_ORIGINS` in `backend/.env`:

```env
CORS_ORIGINS=http://localhost:3000,https://yourapp.vercel.app
```

Then restart the backend (hot reload does not reload `.env`):
```bash
sudo supervisorctl restart backend
# or
pkill -f uvicorn && uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

---

### Pydantic v2 validation errors (`422`)

**Symptom:** POST requests return `422 Unprocessable Entity`.

**Diagnosis:**
```bash
curl -X POST http://localhost:8001/api/status \
  -H "Content-Type: application/json" \
  -d '{"client_name": "test"}'
```

Check the response `detail` field — it lists every failing field and why.

**Common cause:** Sending wrong types or missing required fields. Pydantic v2 is strict — use the exact field names from the model.

---

### `yarn start` fails with module not found

**Symptom:** `Module not found: Can't resolve '@/components/...'`

**Cause:** The `@` path alias requires CRACO. Make sure you're running `yarn start` (which uses `craco start`), **not** `react-scripts start`.

```bash
# Check your package.json start script — it must be:
"start": "craco start"
```

---

### Hot reload not working for `.env` changes

React's dev server and FastAPI's `--reload` flag both watch source files, **not** `.env` files. After changing any `.env` file:

- **Frontend:** Stop and restart `yarn start`
- **Backend:** Stop and restart uvicorn (or `sudo supervisorctl restart backend`)

---

### MongoDB ObjectId serialization error

**Symptom:** `TypeError: Object of type ObjectId is not JSON serializable`

**Cause:** A raw MongoDB document is being returned from an API endpoint.

**Fix:** Always use Pydantic model serialisation. Never return raw `dict` from MongoDB:

```python
# WRONG — will crash
return await db.collection.find_one({"id": id})

# CORRECT — use Pydantic model
doc = await db.collection.find_one({"id": id}, {"_id": 0})
return MyModel(**doc)
```

---

### Supervisor logs location

```bash
# Backend stdout
tail -f /var/log/supervisor/backend.out.log

# Backend errors
tail -f /var/log/supervisor/backend.err.log

# Frontend stdout
tail -f /var/log/supervisor/frontend.out.log

# Frontend errors
tail -f /var/log/supervisor/frontend.err.log
```

---

## 16. Contributing

### Development workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes following the conventions below
3. Test locally end-to-end
4. Commit with a descriptive message: `git commit -m "feat: add user authentication"`
5. Push and open a pull request

### Code conventions

**Backend (Python)**
- Follow PEP 8. Run `black .` before committing.
- All new API routes go through `api_router`, never directly on `app`
- All Pydantic models use `ConfigDict(extra="ignore")` to safely handle Mongo docs
- Use `datetime.now(timezone.utc)`, never `datetime.utcnow()` (deprecated)
- Store datetimes as ISO strings in MongoDB (consistent with existing collections)

**Frontend (JavaScript/JSX)**
- Use functional components and hooks only (no class components)
- Import components via the `@/` alias, never relative `../../../`
- Every new interactive or data-displaying element needs a `data-testid`
- Register new test IDs in `src/constants/testIds/`
- Use `cn()` from `@/lib/utils` to merge conditional Tailwind classes

**Commit message format:**
```
<type>: <short description>

Types: feat | fix | docs | style | refactor | test | chore
```

---

## 17. License

This project is private. All rights reserved.

---

*Built on the [Emergent Platform](https://emergent.sh) — comment-flow-7*
