# MCP Integration & Tool Safety Guidelines

## 1. Role of Model Context Protocol (MCP) in KalaiPaalam AI
In the KalaiPaalam architecture, MCP servers act as standard gateway connectors between the core catalog engine and external systems.

### Supported Tools:
* `marketplace.get_account`: Inquires account name and connectivity state.
* `marketplace.get_capabilities`: Discovers supported operations for dynamic UI generation.
* `marketplace.create_listing`: Dispatches validated canonical payloads to channel APIs.
* `marketplace.update_price`: Updates single-channel pricing.
* `marketplace.update_inventory`: Updates stock availability.
* `marketplace.sync`: Synchronizes inventory and pricing state.

---

## 2. Safety Boundaries & Human-in-the-Loop Constraints
To prevent accidental inventory corruption, automated account suspensions, or unintended financial commitments:

1. **Explicit Confirmation**: The AI agent is strictly forbidden from autonomously executing destructive actions (`DELETE_LISTING`, `DISCONNECT`, `PRICE_UPDATE`, `BULK_PUBLISH`) without human artisan or cluster manager approval.
2. **Deterministic Execution**: The AI prepares, extracts, and validates schemas, but actual transmission through the connector remains deterministic.
3. **Token Isolation**: Marketplace credentials are kept in server-side environment variables and token references (`vault://...`); tokens are never exposed in prompt contexts or client code.
