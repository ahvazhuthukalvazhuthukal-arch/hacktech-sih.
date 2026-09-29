# KalaiPaalam AI — 7-Minute Judge Demo Guide

## Presentation Philosophy
> *"The problem is not that artisans don't have products. The problem is that digital commerce expects them to create professional images, type product descriptions, understand marketplace fields, price products, and manage multiple selling channels. KalaiPaalam removes that digital burden."*

---

## The 3 Big Demo Moments

### Moment 1: One Photo + One Voice → 5 Live Marketplaces (Minute 1:00 – 3:30)
1. Open the **Artisan Mobile App** view.
2. Select **Handloom Cotton Saree** photo and record natural speech in Tamil:
   *"This is a handwoven cotton saree made by our Kanchipuram group with floral temple border. It took 2 days. Material cost was 800 rupees."*
3. Tap **✨ Transform with AI Studio**:
   * Show before & after: Messy workshop plank background removed, neutral catalog background with soft contact shadow applied.
   * Show Touch-to-Confirm cards: Title, material, HSN code 5208 (AI Suggested).
   * Show Explainable Fair-Price recommendation: ₹5,500 with complete cost breakdown.
4. Select all 5 channels: **KalaiPaalam Catalog, ONDC, GeM, Amazon, Flipkart**.
5. Tap **🚀 Publish to All Selected Stores**:
   * Watch live progress checkmarks as each connector receives its mapped protocol payload.

### Moment 2: Centralized 1-Click Price & Stock Sync (Minute 3:30 – 5:00)
1. Switch to the **Multi-Store Sync** tab.
2. Update the saree price from **₹5,500 to ₹5,800** and inventory from **10 to 9 units**.
3. Tap **⚡ Push Updates Across All Connected Stores**.
4. Show how Amazon SP-API, Flipkart Samarth, ONDC Beckn, and D2C Storefront immediately receive the updated price and inventory without editing each platform individually.

### Moment 3: Offline Resilience & Auto-Sync (Minute 5:00 – 6:30)
1. Toggle the **Offline Mode** switch in the top header.
2. Notice the red alert: *"OFFLINE MODE: Drafts saved locally on SQLite"*.
3. Create a new product. Show that it saves locally with status `PENDING_SYNC`.
4. Turn **Offline Mode OFF**.
5. Show how the background sync queue automatically transmits the queued drafts and completes multi-channel publishing once connection returns.

---

## 7-Minute Minute-by-Minute Timeline

| Minute | Screen / Action | What to Say to the Judges |
| :--- | :--- | :--- |
| **0:00–0:45** | Welcome & Problem Statement | *"An artisan may possess master craft expertise but face insurmountable barriers in photography, catalog typing, English descriptions, and pricing. KalaiPaalam starts with what they already have: their craft and their voice."* |
| **0:45–1:45** | Capture & AI Studio | *"A single phone photo is transformed by AI Studio: background removal, lighting normalization, and delicate texture preservation for handlooms and brass."* |
| **1:45–2:45** | Bhashini Voice & NLP | *"The artisan describes the craft in Tamil or Hindi. Bhashini transcribes and translates, while our NLP extracts structured attributes with zero typing."* |
| **2:45–3:45** | Fair-Price Engine | *"Our pricing engine is transparent and explainable: material + skilled labour + overhead + market signal. The artisan stays in control."* |
| **3:45–5:00** | Multi-Channel Publishing | *"One product maps into ONDC Beckn protocol, GeM procurement feed, Amazon SP-API, and Flipkart Samarth. Create once, sell everywhere."* |
| **5:00–6:00** | Price Sync & Offline Demo | *"Demonstrating 1-click price updates across all channels and offline SQLite resilience."* |
| **6:00–7:00** | Admin & Buyer Catalog | *"Cluster managers see collective metrics and full provenance traceability; buyers enjoy an authentic artisan marketplace."* |
