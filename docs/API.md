# KalaiPaalam AI — REST API Reference Specification

All endpoints are hosted at `http://localhost:8000` (Interactive Swagger docs at `http://localhost:8000/docs`).

---

## 1. Products API (`/api/products`)

### `GET /api/products/`
Returns all canonical craft products with optional filtering.
* **Query Parameters**:
  * `category` (string, optional): e.g., "Textiles & Handloom"
  * `status` (string, optional): "DRAFT", "READY", "PUBLISHED"

### `GET /api/products/{product_id}`
Returns full canonical product object including bilingual titles, descriptions, finance calculations, and connected marketplace statuses.

### `POST /api/products/ai_process`
Executes end-to-end AI Studio transformation.
* **Multipart Form Fields**:
  * `image` (file, optional): Craft photo
  * `voice` (file, optional): Audio recording
  * `spoken_text` (string, optional): Direct transcribed or typed craft description
  * `language` (string, default: "ta"): "ta", "hi", "en"
  * `existing_image_url` (string, optional): Seeded demo image reference
* **Response**: Canonical product object with studio image, bilingual copy, and fair-price range.

### `PUT /api/products/{product_id}`
Updates canonical product attributes following artisan review.

### `POST /api/products/{product_id}/publish`
Publishes one canonical product across selected marketplace adapters.
* **Request Body**:
```json
{
  "channels": ["KalaiPaalam Catalog", "ONDC", "GeM", "Amazon", "Flipkart"]
}
```

### `POST /api/products/{product_id}/sync_price`
Propagates updated price across all active marketplace listings.
* **Request Body**: `{"price": 5800.0}`

### `POST /api/products/{product_id}/sync_inventory`
Propagates stock count adjustments across all active channels.
* **Request Body**: `{"inventory": 9}`

---

## 2. Marketplaces API (`/api/marketplaces`)

### `GET /api/marketplaces/`
Returns all registered sales channels with capabilities, connection state, and environment badges.

### `POST /api/marketplaces/connect`
Simulates OAuth token vault authorization for a channel.
* **Request Body**: `{"marketplace": "Amazon"}`

### `GET /api/marketplaces/{marketplace}/payload/{product_id}`
Returns the exact protocol payload generated for that channel (Beckn BPP Item, GeM procurement feed, Amazon SP-API, Flipkart listing).

---

## 3. Offline Sync API (`/api/sync`)

### `POST /api/sync/`
Batch ingest endpoint for locally cached SQLite drafts upon internet restoration.

### `GET /api/sync/jobs`
Returns recent sync job logs, timestamps, and error messages.

---

## 4. Admin & Traceability API (`/api/admin`)

### `GET /api/admin/dashboard`
Returns high-level statistics for cluster managers (artisans, products, active channels).

### `GET /api/admin/traceability/{product_id}`
Returns complete audit trail from original voice transcript to structured JSON and marketplace payloads.

### `POST /api/admin/bulk_publish`
Cluster-wide bulk publishing for up to 50 items simultaneously.

---

## 5. Buyer Catalog API (`/api/catalog`)

### `GET /api/catalog/`
Public D2C storefront items with search and category filters.

### `POST /api/catalog/order`
Simulates verified buyer purchase and updates central inventory.
