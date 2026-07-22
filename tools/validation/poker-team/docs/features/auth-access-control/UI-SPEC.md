---
id: auth-access-control-ui
feature: auth-access-control
title: Auth Access Control UI Specification
summary: Frontend design contract for login, logout, and session management.
status: draft
pillar: platform
domain: auth-access-control-ui
audience:
  - developers
priority: p1
lang: en
owners:
  - web-core
updatedAt: 2026-04-24
dependencies:
  - SPEC.md
  - interfaces.md
  - operations.md
  - states.md
  - STORIES.md
includes: []
constitution: docs/UI-ARCHITECTURE.md
---

# UI Specification: Authentication and Access Control

> Governs the frontend presentation of login, logout, and session management.
> Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

---

## Route Table

| Route    | Page Title | Layout     | Auth Required | Component   |
| -------- | ---------- | ---------- | ------------- | ----------- |
| `/login` | Login      | AuthLayout | No            | `LoginForm` |

Logout is handled via a sidebar action button, not a dedicated page.
Token introspection and permission catalog are admin debug tools (out of MVP scope).

---

## Page Layouts

### /login

```
┌──────────────────────────────────────┐
│            AuthLayout                │
│  ┌──────────────────────────────┐   │
│  │     Logo + App Name          │   │
│  │                              │   │
│  │  ┌────────────────────────┐  │   │
│  │  │     LoginForm          │  │   │
│  │  │  identifier input      │  │   │
│  │  │  password input        │  │   │
│  │  │  [Login] button        │  │   │
│  │  │  error message area    │  │   │
│  │  └────────────────────────┘  │   │
│  └──────────────────────────────┘   │
└──────────────────────────────────────┘
```

---

## Component Inventory

| Component        | Type    | Location                             | Purpose                                            |
| ---------------- | ------- | ------------------------------------ | -------------------------------------------------- |
| `LoginForm`      | Form    | `components/auth/LoginForm.tsx`      | Credential input + submit + error display          |
| `LogoutButton`   | Action  | `components/auth/LogoutButton.tsx`   | Sidebar footer logout trigger                      |
| `AuthProvider`   | Context | `components/auth/AuthProvider.tsx`   | Token storage, session state, login/logout methods |
| `ProtectedRoute` | Guard   | `components/auth/ProtectedRoute.tsx` | Redirect to /login if not authenticated            |

---

## Data Flow

### Login

| Step | Action                    | API Call           | On Success                                         | On Error                          |
| ---- | ------------------------- | ------------------ | -------------------------------------------------- | --------------------------------- |
| 1    | User submits credentials  | `POST /auth/login` | Store token in localStorage, redirect to `/`       | Show error message per error code |
| 2    | Page load (any protected) | —                  | Check localStorage for token, validate not expired | Redirect to `/login`              |

### Logout

| Step | Action             | API Call            | On Success                                     |
| ---- | ------------------ | ------------------- | ---------------------------------------------- |
| 1    | User clicks Logout | `POST /auth/logout` | Clear localStorage token, redirect to `/login` |

---

## Form Contracts

### LoginForm

| Field      | Type   | HTML Input | Validation           | Error Message                   |
| ---------- | ------ | ---------- | -------------------- | ------------------------------- |
| identifier | string | `text`     | Required, min 1 char | "Email or username is required" |
| secret     | string | `password` | Required, min 1 char | "Password is required"          |

**Zod schema:**

```typescript
z.object({
  identifier: z.string().min(1, "Email or username is required"),
  secret: z.string().min(1, "Password is required"),
});
```

### Error Code → UI Message Mapping

| API Error Code        | HTTP Status | UI Message                                      |
| --------------------- | ----------- | ----------------------------------------------- |
| `INVALID_CREDENTIALS` | 401         | "Invalid email or password."                    |
| `PRINCIPAL_DISABLED`  | 401         | "Your account has been disabled."               |
| `FORBIDDEN`           | 403         | "Login temporarily blocked. Try again later."   |
| (unknown)             | 5xx         | "Something went wrong. Please try again."       |

---

## State-to-UI Mapping

| State             | UI Representation                                        |
| ----------------- | -------------------------------------------------------- |
| Not authenticated | Redirect to `/login`, show LoginForm                     |
| Login in progress | Submit button disabled, spinner, inputs disabled         |
| Login failed      | Error alert below form with mapped message               |
| Authenticated     | Redirect to `/`, sidebar shows LogoutButton              |
| Session expired   | Clear token, redirect to `/login` with "Session expired" |

---

## Accessibility Requirements

| Component     | Requirement                                                |
| ------------- | ---------------------------------------------------------- |
| LoginForm     | `role="form"`, `aria-label="Login"`, focus on first input  |
| Error alerts  | `role="alert"`, `aria-live="assertive"`                    |
| Password      | Toggle visibility button with `aria-label="Show password"` |
| Submit button | Disabled state includes `aria-disabled="true"`             |
| LogoutButton  | `aria-label="Logout"` with confirmation if needed          |
