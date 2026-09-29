# KalaiPaalam AI — 50 Judge & SIH Selector Questions & Answers

### 1. What exactly is the problem?
Artisans possess generational craft expertise but face insurmountable friction in photography, digital cataloging, English descriptions, complex marketplace fields, and multi-channel pricing. KalaiPaalam eliminates this digital burden.

### 2. Why is voice important?
It converts existing spoken craft knowledge into structured digital catalog data in seconds, requiring zero typing from marginalized rural artisans.

### 3. Why not just use an existing e-commerce app?
Standard seller apps assume English literacy, computer skills, professional lighting, and manual form filling across dozens of mandatory attributes. KalaiPaalam is designed around artisan constraints first.

### 4. What is uniquely innovative here?
The unified pipeline: **Photo + Voice → AI Studio & NLP → Canonical Product → Dynamic Fair Price → 1-Click Multi-Marketplace Linkage (ONDC, GeM, Amazon, Flipkart)**.

### 5. What is the role of AI?
AI handles image preparation (background removal, lighting normalization), speech transcription/translation (Bhashini), structured field extraction, and fair-price decision support.

### 6. What is NOT AI?
Relational database storage, OAuth token references, API orchestration, and marketplace protocol adapters are conventional, deterministic software components.

### 7. How does the image model work?
It uses edge-aware foreground matting (OpenCV GrabCut + CLAHE lighting correction) to cleanly segment craft items from cluttered workshop floors while preserving fine threads, zari borders, and brass reflections.

### 8. Why rembg and OpenCV?
rembg offers an accessible U2-Net segmentation model, while OpenCV executes sub-second color correction, resizing, and lighting normalization with zero GPU dependency.

### 9. Why Flutter?
A single, high-performance cross-platform codebase optimized for low-resource Android smartphones prevalent in rural artisan clusters.

### 10. Why FastAPI?
Lightweight, asynchronous Python architecture that seamlessly bridges deep learning computer vision and speech pipelines with high-throughput REST APIs.

### 11. Why PostgreSQL & SQLite?
Relational data integrity is essential for inventory, financial transactions, and audit logs. SQLite powers local offline client caching, while PostgreSQL handles the central backend.

### 12. What if internet is unavailable?
The mobile app operates offline-first: photos and drafts are saved locally in SQLite with status `PENDING_SYNC` and automatically synchronized when connectivity returns.

### 13. How do you prevent AI hallucination?
Strict structured JSON extraction schemas, explicit provenance tracking (`VOICE`, `ARTISAN`, `AI_SUGGESTED`), and touch-to-confirm cards ensure the artisan approves all data before publishing.

### 14. Can the artisan correct AI outputs?
Yes. Every field (title, price, dimensions, material) is editable on touch-to-confirm cards.

### 15. How is the fair price calculated?
$$\text{BaseCost} = \text{MaterialCost} + (\text{LabourHours} \times \text{LabourRate}) + \text{Overhead}$$
$$\text{MarketAdjusted} = \text{BaseCost} \times \text{MarketSignalMultiplier}$$
Transparent ranges are provided with full cost breakdown.

### 16. Is the suggested price guaranteed?
No. It is an explainable decision-support recommendation; the artisan retains complete authority to adjust or override.

### 17. What does ONDC integration mean in this prototype?
Our ONDC adapter translates the canonical product into a compliant Beckn Protocol BPP Item schema, ready for network transmission.

### 18. Why not directly call ONDC or Amazon from Flutter?
Direct calls from mobile devices expose API credentials and create unmaintainable network dependencies. The backend connector layer centralizes authentication, protocol transformations, and retries.

### 19. How do you protect marketplace credentials?
We use server-side OAuth token vaults and secure references (`vault://...`). No plaintext passwords or tokens are ever sent to client devices or LLM prompts.

### 20. How does centralized price sync work?
When an artisan updates the price in KalaiPaalam (e.g., ₹5,500 to ₹5,800), the Connector Engine broadcasts price updates across all connected channels simultaneously.

### 21. How does centralized inventory sync work?
An order on any channel decrements stock centrally, and updated stock availability is immediately propagated across all remaining channels to prevent overselling.

### 22. What is Village / Cluster Mode?
Cluster managers can view aggregated inventory across 40+ artisans and execute bulk multi-channel publishing with a single click.

### 23. What happens if Bhashini is temporarily down?
The system falls back gracefully to a verified local multilingual parser or cached transcript, ensuring the demo or user workflow never crashes.

### 24. How do you support budget Android phones (2GB RAM)?
Images are compressed client-side to a max of 1024x1024, heavy ML processing is handled server-side, and client RAM consumption is capped under 85MB.

### 25. How do you handle dialect variations?
Audio is routed through Bhashini’s Indian-language acoustic models, and touch-to-confirm cards allow instant correction of any uncertain terms.

### 26. Can you add more marketplaces in the future?
Yes. The modular `BaseMarketplaceConnector` abstraction allows adding channels (e.g., Etsy, Myntra, Meesho) simply by implementing one adapter class without modifying the mobile app.

### 27. What is DPDP compliance in this context?
Explicit consent screens, purpose-bound collection, and data minimization. Full statutory compliance is planned for institutional pilot deployment.

### 28. How do buyers trust artisan authenticity?
Each product carries verified artisan identity, geographical cluster indicators (GI tags), and rich craft heritage narratives.

### 29. Can an artisan use this without knowing English?
Yes. The entire workflow is voice-driven and available in Tamil, Hindi, and other regional languages.

### 30. How do you avoid duplicate product uploads during offline sync?
Idempotency keys generated client-side ensure that retried batch uploads update existing records rather than creating duplicates.
