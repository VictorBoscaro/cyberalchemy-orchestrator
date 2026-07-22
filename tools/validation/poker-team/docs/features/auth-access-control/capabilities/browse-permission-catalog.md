# Browse Permission Catalog

> ← Back to [Module Index](../SPEC.md#capabilities) · Stories: [US-09](../STORIES.md#us-09-admin-lists-available-permissions)

List available permission keys for admin tooling.

## Aspect Map

| Aspect | Concept | Summary |
| ------ | ------- | ------- |
| Query | [GetPermissionCatalog](../queries.md#getpermissioncatalog) | Lists permission keys, descriptions, and active/deprecated status |
| Interface | Internal or admin endpoint | Namespace filter, optional deprecated inclusion |

## Filters

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| namespace | string | (all) | Filter by service namespace |
| includeDeprecated | boolean | false | Include deprecated permission keys |

## Output Shape

| Field | Type | Description |
| ----- | ---- | ----------- |
| permissions[].key | string | Canonical permission key (`service.scope.action`) |
| permissions[].description | string | Human-readable meaning |
| permissions[].status | string | `active` or `deprecated` |

## Required Catalog Entries

These canonical keys must always be present in active entries:

- `auth-access-control.read.introspectToken`
- `auth-access-control.admin.logoutAnySession`

## Domain Concepts Used

- [PermissionGrant](../domain.md#permissiongrant) — source of permission keys
- [PermissionKey](../domain.md#permissionkey) — canonical key format
