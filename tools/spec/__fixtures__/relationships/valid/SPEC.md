# Relationship Fixture - valid

## Concept Registry

| Concept | Type |
| --- | --- |
| MaxAmountRule | Rule |
| ProcessPayment | Operation |
| PaymentCompleted | Event |
| PaymentTransaction | Entity |
| WireTransferWorkflow | Workflow |
| ReserveFunds | Operation |
| Library | Entity |
| Copy | Entity |
| Title | Entity |

## Feature Concept Graph

| From | Edge | To |
| --- | --- | --- |
| MaxAmountRule | enforces | ProcessPayment |
| ProcessPayment | produces | PaymentCompleted |
| PaymentTransaction | emits | PaymentCompleted |
| WireTransferWorkflow | orchestrates | ReserveFunds |
| Library | owns | Copy |
| Copy | belongs-to | Title |
