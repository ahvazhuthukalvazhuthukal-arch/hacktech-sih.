# Marketplace Connectors & Schema Mapping Specification

## 1. Overview
The **Marketplace Connector Layer** decouples KalaiPaalam's internal Canonical Product representation from destination marketplace protocols.

| Marketplace | Protocol / API | Environment | Status | Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **ONDC** | Beckn Protocol v1.2.0 (BPP / BAP) | DEMO / SANDBOX | Connected | `CREATE_LISTING`, `UPDATE_PRICE`, `UPDATE_INVENTORY`, `SYNC` |
| **GeM** | Government e-Marketplace XML/JSON Feed | DEMO / SANDBOX | Connected | `CREATE_LISTING`, `UPDATE_INVENTORY`, `SYNC` |
| **Amazon** | Selling Partner API (SP-API / Flat File) | DEMO / SANDBOX | Connected | `CREATE_LISTING`, `UPDATE_LISTING`, `UPDATE_PRICE`, `UPDATE_INVENTORY`, `ORDERS` |
| **Flipkart** | Samarth Artisan Seller API | DEMO / SANDBOX | Connected | `CREATE_LISTING`, `UPDATE_PRICE`, `UPDATE_INVENTORY`, `SYNC` |
| **KalaiPaalam Catalog** | Direct Native D2C Storefront | LIVE | Connected | `CREATE_LISTING`, `UPDATE_LISTING`, `UPDATE_PRICE`, `UPDATE_INVENTORY`, `ORDERS`, `IMAGE_UPLOAD` |

---

## 2. Field Mapping Matrix

| Canonical Field | ONDC (Beckn) | GeM Feed | Amazon SP-API | Flipkart Samarth |
| :--- | :--- | :--- | :--- | :--- |
| `title` | `descriptor.name` | `catalog_title` | `item_name[0].value` | `attributes.title` |
| `description` | `descriptor.long_desc` | `description` | `description[0].value` | `attributes.description` |
| `price` | `price.value` | `offered_unit_price_inr` | `our_price[0].schedule[0]` | `listing_details.selling_price` |
| `inventory` | `quantity.available.count` | `inventory_available` | `fulfillment_availability.quantity` | `inventory_details.locations[0].stock_count` |
| `hsn_code` | `tags.hsn_code` | `hsn_code` | `hsn_code[0].value` | `listing_details.hsn` |
| `country_of_origin` | `tags.country_of_origin` | `make_in_india_compliance` | `country_of_origin[0].value` | `attributes.country_of_origin` |
| `weight_grams` | `tags.weight` | `weight_in_grams` | `item_package_weight.value` | `shipping_profile.package_weight_kg` |
| `processed_image_url` | `descriptor.images` | `product_image_url` | `main_product_image_locator` | `attributes.primary_image` |

---

## 3. Pre-Publish Validation
Prior to dispatching payloads to any channel, the connector executes `validate_canonical_product()`:
1. If mandatory attributes (`title`, `price`, `hsn_code`) are missing, publishing is **blocked** and returned with actionable error messages.
2. AI assistance is invoked to suggest missing fields (e.g. HSN codes derived from product taxonomy).
3. Secrets and access tokens are never transmitted in cleartext.
