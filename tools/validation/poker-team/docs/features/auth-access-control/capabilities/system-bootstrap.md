---
id: auth-access-control
feature: auth-access-control
title: System Bootstrap Capability
summary: Auto-seed admin principal and role-based permission grants on application startup.
status: in-progress
pillar: platform
domain: auth-access-control-capabilities
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - platform-core
updatedAt: 2026-04-16
dependencies:
  - ../SPEC.md
includes: []
---

# System Bootstrap

Auto-create the admin principal and all role → permission grant mappings on first application boot. Subsequent boots ensure role grants are complete (idempotent sync).

## Aspects

| Aspect    | Concept                                                | Summary                                             |
| --------- | ------------------------------------------------------ | --------------------------------------------------- |
| Domain    | [RoleDefinition](../domain.md#roledefinition)          | 4 predefined roles with permission sets             |
| Operation | [SeedSystemBootstrap](../operations.md#seedsystembootstrap) | Creates admin principal + seeds all role grants |

## Key Behaviors

1. **First boot**: No admin principal exists → generate random password (C1), create admin principal (C2), seed all role grants (C3), log password to stdout.
2. **Subsequent boot**: Admin exists (R1 skip) → sync role grants only (R4). Missing grants are added, no grants are removed.
3. **Password**: Generated with `crypto.randomBytes(32).toString('base64url')` — 256-bit entropy. Never persisted in plaintext.
4. **Credential hash**: bcrypt with cost factor 12.
5. **Env override**: `ADMIN_USERNAME` defaults to `admin`.

## Role Permission Table

See [RoleDefinition](../domain.md#roledefinition) for the complete role → permission mapping.

## Error Behavior

| Condition              | Behavior                              |
| ---------------------- | ------------------------------------- |
| Database unreachable   | App fails to start with explicit error |
| Admin already exists   | Skip creation, sync role grants       |
| Hash failure           | App fails to start with explicit error |
