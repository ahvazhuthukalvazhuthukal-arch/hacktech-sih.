# Offline-First Architecture & Sync Reconciliation

## 1. The Offline Reality in Rural Artisan Clusters
Artisan clusters in locations like Kanchipuram, Chanderi, or Bastar often face intermittent connectivity. KalaiPaalam AI guarantees that **no artisan work is lost during offline periods**.

---

## 2. Local Persistence (SQLite)
* **Drafts Storage**: Captured craft photos, voice transcripts, and intermediate JSON objects are stored in the mobile SQLite database (`kalaipaalam_offline.db`).
* **State Label**: Items created while offline receive the status `PENDING_SYNC`.
* **Idempotency Keys**: Every offline draft is assigned a unique client UUID (`KP-...`), ensuring that multiple sync attempts never duplicate products on the backend.

---

## 3. Background Sync & Network Transition
1. The app monitors network connectivity changes.
2. Upon network restoration, the client dispatches queued drafts via `POST /api/sync`.
3. The server ingests the drafts, executes the marketplace adapters, and marks the jobs as `SYNCED`.
4. The local SQLite record is updated with server confirmation receipts only after the server acknowledges the transaction.
