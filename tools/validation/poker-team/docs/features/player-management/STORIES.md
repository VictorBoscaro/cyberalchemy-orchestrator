---
id: player-management-stories
feature: player-management
title: Player Management User Stories
summary: Capability-scoped user stories for player creation, listing, overview projections, progression checks, and coach assignment model.
status: implemented
pillar: operations
domain: player-management
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
includes: []
---

# Player Management — User Stories

> Source of storytelling truth for [player-management](SPEC.md).

## US-01 Admin Operations Journey: Register A New Player

**Classic format**
As an **operations admin**, I want **to register a new player with identity and financial defaults**, so that **the player exists in the system for settlement, makeup, and stats tracking**.

**BDD scenario**
Given I am authenticated with `player-management.write.createPlayer` permission
When I submit a valid player registration with name, email, current limit, and optional initial bankroll
Then the player is persisted in `OBSERVATION` status with a canonical email key and default bankroll of 0

**Acceptance checks**

- [ ] Player creation follows [CreatePlayer](operations.md#createplayer) rules R0–R6 and calculations C1–C2.
- [ ] Name, email, and currentLimit are required; initialBankroll defaults to 0 when omitted.
- [ ] Email uniqueness is enforced via canonical key (`lowercase(removeSpecialChars(trim(email)))`).
- [ ] currentLimit must be in the allowed set `{NL20, NL40, NL60, NL80, NL100}`.
- [ ] New player state is `OBSERVATION` per [PlayerStatus](domain.md#playerstatus).
- [ ] API contract follows [POST /players](interfaces.md#post-players) with 201 success response.
- [ ] Authorization check follows [AuthorizeRequest](../auth-access-control/operations.md#authorizerequest).

**Capability link**: [SPEC — Create Player](SPEC.md#create-player)

**Concept and aspect links**

- player-management.CreatePlayer: [CreatePlayer](operations.md#createplayer)
- player-management.Player: [Player](domain.md#player)
- player-management.PlayerStatus: [PlayerStatus](domain.md#playerstatus)
- player-management.CreatePlayerRequestToEntity: [CreatePlayerRequestToEntity](mappings.md#createplayerrequesttoentity)
- player-management.PlayerAPI: [POST /players](interfaces.md#post-players)

---

## US-02 Public Journey: View Player List And Portfolio Overview

**Classic format**
As an **operations user or dashboard consumer**, I want **to view all players and their 30-day portfolio projections**, so that **I can monitor team performance and financial health at a glance**.

**BDD scenario**
Given I am authenticated with read permissions
When I request the full player list or the players overview endpoint
Then I receive all players with their current status, or enriched overview projections with lifetime profit, average hands, and winrate

**Acceptance checks**

- [ ] List follows [GetAllPlayers](queries.md#getallplayers) returning all player records.
- [ ] Overview follows [GetPlayersOverview](queries.md#getplayersoverview) joining Player with [PlayerStatsSnapshot](../player-stats/domain.md#playerstatssnapshot).
- [ ] Overview DTO includes computed lifetimeProfit, avgHands, and winrate via [PlayerToOverviewDto](mappings.md#playertooverviewdto).
- [ ] Both endpoints require appropriate read permissions per [PlayerAPI](interfaces.md#external-playerapi-rest).
- [ ] Default period for overview is 30 days.

**Capability link**: [SPEC — List All Players](SPEC.md#list-all-players), [SPEC — Players Overview](SPEC.md#players-overview)

**Concept and aspect links**

- player-management.GetAllPlayers: [GetAllPlayers](queries.md#getallplayers)
- player-management.GetPlayersOverview: [GetPlayersOverview](queries.md#getplayersoverview)
- player-management.PlayerToOverviewDto: [PlayerToOverviewDto](mappings.md#playertooverviewdto)
- player-management.PlayerAPI: [PlayerAPI](interfaces.md#external-playerapi-rest)

---

## US-03 Cross-Feature Integration: Player Data Consumed By Settlement, Makeup, And Progression

**Classic format**
As a **downstream feature consumer** (financial-settlement, player-makeup, player-progression), I want **reliable player identity and financial baseline data**, so that **settlement calculations, makeup adjustments, and progression checks reference authoritative player state**.

**BDD scenario**
Given players exist with current bankroll, makeup, and limit data
When financial-settlement, player-makeup, or player-progression queries player data
Then the consuming feature receives consistent player state through documented query contracts

**Acceptance checks**

- [ ] financial-settlement consumes player context via [GetAllPlayers](queries.md#getallplayers) for settlement calculations.
- [ ] player-makeup consumes player existence and makeup baseline through the same query contract.
- [ ] Players Overview reads [player-stats.GetPlayerStatsWindow](../player-stats/queries.md#getplayerstatswindow) for rolling period metrics.
- [ ] Progression check delegates to [player-progression](../player-progression/SPEC.md) via [GET /players/:id/progression](interfaces.md#get-playersidprogression).
- [ ] Cross-feature dependency contracts are documented in [SPEC — Cross-Feature Dependencies](SPEC.md#cross-feature-dependencies).

**Capability link**: [SPEC — Players Overview](SPEC.md#players-overview), [SPEC — Check Player Progression](SPEC.md#check-player-progression)

**Concept and aspect links**

- player-management.GetAllPlayers: [GetAllPlayers](queries.md#getallplayers)
- player-management.GetPlayersOverview: [GetPlayersOverview](queries.md#getplayersoverview)
- player-stats.GetPlayerStatsWindow: [GetPlayerStatsWindow](../player-stats/queries.md#getplayerstatswindow)

---

## US-04 Error And Edge Case Journey: Reject Invalid Player Registration And Unauthorized Access

**Classic format**
As an **operations admin or API consumer**, I want **invalid, unauthorized, and duplicate registration attempts handled deterministically**, so that **the player roster remains consistent and error feedback is actionable**.

**BDD scenario**
Given a registration request is missing required fields, has a duplicate email, uses an invalid limit, or lacks authorization
When the request is processed
Then the API returns a structured error (400 validation, 409 duplicate, 401/403 auth) and no player is created

**Acceptance checks**

- [ ] Missing name/email/currentLimit returns 400 validation error per [CreatePlayer](operations.md#createplayer) R1–R3.
- [ ] Duplicate canonical email returns 409 `DUPLICATE_EMAIL` per R4.
- [ ] Negative initialBankroll returns 400 per R5.
- [ ] Invalid currentLimit value returns 400 per R6.
- [ ] Missing/invalid/expired JWT returns 401; missing permission returns 403.
- [ ] All error responses follow the standard error payload format per [POST /players responses](interfaces.md#post-players).
- [ ] Read endpoints return 401/403 for unauthorized access.

**Capability link**: [SPEC — Create Player](SPEC.md#create-player)

**Concept and aspect links**

- player-management.CreatePlayer: [CreatePlayer](operations.md#createplayer)
- player-management.PlayerAPI: [PlayerAPI](interfaces.md#external-playerapi-rest)

---

## US-05 Admin Operations Journey: Register A New Coach

**Classic format**
As an **operations admin**, I want **to register a coach with an auth principal binding**, so that **players can be assigned to a coach for visibility-scoped management**.

**BDD scenario**
Given I am authenticated with `player-management.write.createCoach` permission
When I submit a valid coach registration with principalId, name, and email
Then the coach is persisted in `ACTIVE` status with a unique principalId

**Acceptance checks**

- [ ] Coach creation follows [CreateCoach](operations.md#createcoach) rules R0–R4.
- [ ] principalId, name, and email are required.
- [ ] principalId must be unique among active coaches (409 `DUPLICATE_PRINCIPAL` otherwise).
- [ ] New coach state is `ACTIVE` per [CoachStatus](domain.md#coachstatus).
- [ ] API contract follows [POST /coaches](interfaces.md#post-coaches) with 201 success response.
- [ ] Authorization check follows [AuthorizeRequest](../auth-access-control/operations.md#authorizerequest).

**Capability link**: [SPEC — Create Coach](SPEC.md#create-coach)

**Concept and aspect links**

- player-management.CreateCoach: [CreateCoach](operations.md#createcoach)
- player-management.Coach: [Coach](domain.md#coach)
- player-management.CoachStatus: [CoachStatus](domain.md#coachstatus)
- player-management.CreateCoachRequestToEntity: [CreateCoachRequestToEntity](mappings.md#createcoachrequesttoentity)
- player-management.CoachAPI: [POST /coaches](interfaces.md#post-coaches)

---

## US-06 Admin Operations Journey: Assign And Unassign Coach To Player

**Classic format**
As an **operations admin**, I want **to assign a coach to a player and later unassign them**, so that **coach-to-player relationships drive visibility scoping across the platform**.

**BDD scenario — assign**
Given a coach with `ACTIVE` status and a player with no active coach assignment exist
When I submit an assignment request for that coach and player
Then a `CoachAssignment` is created with `assignedAt` set and `unassignedAt` null

**BDD scenario — unassign**
Given an active coach-player assignment exists
When I submit an unassignment request for that coach and player
Then the assignment's `unassignedAt` is set to the current timestamp (soft delete) and the player becomes available for reassignment

**Acceptance checks**

- [ ] Assign follows [AssignCoach](operations.md#assigncoach) rules R0–R4.
- [ ] Coach must exist and be `ACTIVE`; player must exist.
- [ ] Player cannot have an active assignment to another coach (409 `PLAYER_ALREADY_ASSIGNED`).
- [ ] Unassign follows [UnassignCoach](operations.md#unassigncoach) rules R0–R1.
- [ ] Active assignment must exist for the given coach-player pair (404 `ASSIGNMENT_NOT_FOUND`).
- [ ] Unassignment sets `unassignedAt` preserving the historical record.
- [ ] One active coach per player invariant is maintained per [CoachAssignment](domain.md#coachassignment).
- [ ] API contracts follow [POST /coaches/:coachId/players/:playerId](interfaces.md#post-coachescoachidplayersplayerid) and [DELETE /coaches/:coachId/players/:playerId](interfaces.md#delete-coachescoachidplayersplayerid).

**Capability link**: [SPEC — Assign Coach](SPEC.md#assign-coach), [SPEC — Unassign Coach](SPEC.md#unassign-coach)

**Concept and aspect links**

- player-management.AssignCoach: [AssignCoach](operations.md#assigncoach)
- player-management.UnassignCoach: [UnassignCoach](operations.md#unassigncoach)
- player-management.CoachAssignment: [CoachAssignment](domain.md#coachassignment)
- player-management.AssignCoachRequestToInput: [AssignCoachRequestToInput](mappings.md#assigncoachrequesttoinput)
- player-management.UnassignCoachRequestToInput: [UnassignCoachRequestToInput](mappings.md#unassigncoachrequesttoinput)
- player-management.CoachAPI: [CoachAPI](interfaces.md#external-coachapi-rest)

---

## US-07 Public Journey: Coach Views Assigned Players

**Classic format**
As a **coach**, I want **to view the list of players assigned to me**, so that **I can focus on my players' performance, makeup, and stats**.

**BDD scenario**
Given I am authenticated as a coach with `player-management.read.getCoachPlayers` permission
When I request the players for my coach profile
Then I receive only the players actively assigned to me

**BDD scenario — admin override**
Given I am authenticated as an admin with `player-management.read.getCoachPlayers` permission
When I request the players for any coach
Then I receive all players assigned to that coach regardless of my identity

**Acceptance checks**

- [ ] Query follows [GetCoachPlayers](queries.md#getcoachplayers) rules R1–R2.
- [ ] Coach-scope enforcement: coaches see only their own assigned players (R2).
- [ ] Admin/manager scope: all assigned players visible.
- [ ] Coach must exist (404 otherwise).
- [ ] API contract follows [GET /coaches/:coachId/players](interfaces.md#get-coachescoachidplayers).
- [ ] List All Coaches follows [GetAllCoaches](queries.md#getallcoaches) via [GET /coaches](interfaces.md#get-coaches).

**Capability link**: [SPEC — List Coach Players](SPEC.md#list-coach-players), [SPEC — List All Coaches](SPEC.md#list-all-coaches)

**Concept and aspect links**

- player-management.GetCoachPlayers: [GetCoachPlayers](queries.md#getcoachplayers)
- player-management.GetAllCoaches: [GetAllCoaches](queries.md#getallcoaches)
- player-management.CoachAssignment: [CoachAssignment](domain.md#coachassignment)
- player-management.CoachAPI: [CoachAPI](interfaces.md#external-coachapi-rest)

---

## US-08 Cross-Feature Integration: Player Visibility Through Coach Assignment

**Classic format**
As the **platform**, I want **a centralized visibility resolver that uses coach assignments**, so that **makeup, stats, and other features enforce consistent player-scoped access without ad-hoc logic**.

**BDD scenario — admin actor**
Given the actor has admin/manager permissions
When ResolvePlayerVisibility is called
Then it returns ALL player IDs (full visibility)

**BDD scenario — coach actor**
Given the actor is a coach with active player assignments
When ResolvePlayerVisibility is called
Then it returns the IDs of assigned players plus the coach's own player record (if the coach is also a player)

**BDD scenario — player actor**
Given the actor is a player with no coach or admin role
When ResolvePlayerVisibility is called
Then it returns only the actor's own player ID (self-only visibility)

**Acceptance checks**

- [ ] Visibility resolution follows [ResolvePlayerVisibility](queries.md#resolveplayervisibility) priority chain: admin=all, coach=assigned+self, player=self.
- [ ] coach-self visibility: if a coach is also a player, their own player record is included.
- [ ] This service replaces the ad-hoc `enforceReadScope` pattern in [player-makeup routes](../player-makeup/interfaces.md) and will be consumed by [player-stats](../player-stats/SPEC.md).
- [ ] No new REST endpoint — consumed internally by other feature routes.
- [ ] Cross-feature dependency documented in [SPEC — Cross-Feature Dependencies](SPEC.md#cross-feature-dependencies).

**Capability link**: [SPEC — Resolve Player Visibility](SPEC.md#resolve-player-visibility)

**Concept and aspect links**

- player-management.ResolvePlayerVisibility: [ResolvePlayerVisibility](queries.md#resolveplayervisibility)
- player-management.Coach: [Coach](domain.md#coach)
- player-management.CoachAssignment: [CoachAssignment](domain.md#coachassignment)
- player-management.Player: [Player](domain.md#player)

---

## US-09 Error And Edge Case Journey: Coach Operations Failure Modes

**Classic format**
As an **operations admin or API consumer**, I want **invalid coach operations handled deterministically**, so that **coach and assignment data remains consistent and error feedback is actionable**.

**BDD scenario — duplicate principal**
Given a coach with the same principalId already exists in ACTIVE status
When I attempt to create another coach with that principalId
Then the API returns 409 `DUPLICATE_PRINCIPAL` and no coach is created

**BDD scenario — assign to already-assigned player**
Given a player already has an active coach assignment
When I attempt to assign a different coach to that player
Then the API returns 409 `PLAYER_ALREADY_ASSIGNED` and no assignment is created

**BDD scenario — assign inactive coach**
Given a coach exists with `INACTIVE` status
When I attempt to assign that coach to a player
Then the API returns 409 `COACH_INACTIVE` and no assignment is created

**BDD scenario — unassign non-existent assignment**
Given no active assignment exists between the specified coach and player
When I attempt to unassign them
Then the API returns 404 `ASSIGNMENT_NOT_FOUND`

**Acceptance checks**

- [ ] Duplicate principalId returns 409 per [CreateCoach](operations.md#createcoach) R4.
- [ ] Player already assigned returns 409 per [AssignCoach](operations.md#assigncoach) R4.
- [ ] Inactive coach returns 409 per [AssignCoach](operations.md#assigncoach) R2.
- [ ] Missing coach returns 404 per [AssignCoach](operations.md#assigncoach) R1.
- [ ] Missing player returns 404 per [AssignCoach](operations.md#assigncoach) R3.
- [ ] Missing active assignment returns 404 per [UnassignCoach](operations.md#unassigncoach) R1.
- [ ] Missing/invalid/expired JWT returns 401; missing permission returns 403 for all coach endpoints.
- [ ] All error responses follow the standard error payload format per [CoachAPI](interfaces.md#external-coachapi-rest).

**Capability link**: [SPEC — Create Coach](SPEC.md#create-coach), [SPEC — Assign Coach](SPEC.md#assign-coach), [SPEC — Unassign Coach](SPEC.md#unassign-coach)

**Concept and aspect links**

- player-management.CreateCoach: [CreateCoach](operations.md#createcoach)
- player-management.AssignCoach: [AssignCoach](operations.md#assigncoach)
- player-management.UnassignCoach: [UnassignCoach](operations.md#unassigncoach)
- player-management.CoachAPI: [CoachAPI](interfaces.md#external-coachapi-rest)

---

## Story Coverage Matrix

| Story | Mandatory Slice           | Concepts Covered                                                                                                                        | Aspect Anchors                                                                                                                                                                                                                      |
| ----- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| US-01 | Admin operations journey  | player-management.CreatePlayer, player-management.Player, player-management.PlayerStatus, player-management.CreatePlayerRequestToEntity | [CreatePlayer](operations.md#createplayer), [Player](domain.md#player), [PlayerStatus](domain.md#playerstatus), [CreatePlayerRequestToEntity](mappings.md#createplayerrequesttoentity), [POST /players](interfaces.md#post-players) |
| US-02 | Public journey            | player-management.GetAllPlayers, player-management.GetPlayersOverview, player-management.PlayerToOverviewDto                            | [GetAllPlayers](queries.md#getallplayers), [GetPlayersOverview](queries.md#getplayersoverview), [PlayerToOverviewDto](mappings.md#playertooverviewdto), [PlayerAPI](interfaces.md#external-playerapi-rest)                          |
| US-03 | Cross-feature integration | player-management.GetAllPlayers, player-management.GetPlayersOverview, player-stats.GetPlayerStatsWindow                                | [GetAllPlayers](queries.md#getallplayers), [GetPlayersOverview](queries.md#getplayersoverview), [GetPlayerStatsWindow](../player-stats/queries.md#getplayerstatswindow)                                                             |
| US-04 | Error and edge case       | player-management.CreatePlayer, player-management.PlayerAPI                                                                             | [CreatePlayer](operations.md#createplayer), [POST /players](interfaces.md#post-players), [GET /players](interfaces.md#get-players), [GET /players/overview](interfaces.md#get-playersoverview)                                      |
| US-05 | Admin operations journey  | player-management.CreateCoach, player-management.Coach, player-management.CoachStatus, player-management.CreateCoachRequestToEntity     | [CreateCoach](operations.md#createcoach), [Coach](domain.md#coach), [CoachStatus](domain.md#coachstatus), [CreateCoachRequestToEntity](mappings.md#createcoachrequesttoentity), [POST /coaches](interfaces.md#post-coaches)         |
| US-06 | Admin operations journey  | player-management.AssignCoach, player-management.UnassignCoach, player-management.CoachAssignment                                       | [AssignCoach](operations.md#assigncoach), [UnassignCoach](operations.md#unassigncoach), [CoachAssignment](domain.md#coachassignment), [CoachAPI](interfaces.md#external-coachapi-rest)                                              |
| US-07 | Public journey            | player-management.GetCoachPlayers, player-management.GetAllCoaches, player-management.CoachAssignment                                   | [GetCoachPlayers](queries.md#getcoachplayers), [GetAllCoaches](queries.md#getallcoaches), [CoachAPI](interfaces.md#external-coachapi-rest)                                                                                          |
| US-08 | Cross-feature integration | player-management.ResolvePlayerVisibility, player-management.Coach, player-management.CoachAssignment, player-management.Player         | [ResolvePlayerVisibility](queries.md#resolveplayervisibility), [Coach](domain.md#coach), [CoachAssignment](domain.md#coachassignment), [Player](domain.md#player)                                                                   |
| US-09 | Error and edge case       | player-management.CreateCoach, player-management.AssignCoach, player-management.UnassignCoach, player-management.CoachAPI               | [CreateCoach](operations.md#createcoach), [AssignCoach](operations.md#assigncoach), [UnassignCoach](operations.md#unassigncoach), [CoachAPI](interfaces.md#external-coachapi-rest)                                                  |

**Coverage gap check**: All concepts from the player-management concept registry are covered. PlayerRepository and CoachRepository/CoachAssignmentRepository (internal interfaces) are implicitly exercised by all stories through the operation and query paths.
