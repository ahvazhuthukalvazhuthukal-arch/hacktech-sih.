# AI Pipeline & Multilingual NLP Specification

## 1. Overview
The KalaiPaalam AI Orchestrator executes a 4-stage pipeline that bridges spoken regional artisan craft knowledge into high-value commercial catalog feeds.

---

## 2. Stage 1: AI Studio Image Processing
* **Objective**: Remove messy artisan workshop backgrounds, normalize uneven incandescent lighting, and create studio catalog mockups without destroying delicate textures.
* **Technology**: OpenCV + rembg (U2-Net / GrabCut fallback).
* **Processing Steps**:
  1. Image validation & compression (max 1024x1024 for low-memory budget Android support).
  2. White-balance correction using Gray-World assumption.
  3. Color and texture enhancement via Contrast Limited Adaptive Histogram Equalization (CLAHE).
  4. Foreground matting preserving delicate zari embroidery, weaves, and metallic luster.
  5. Composition onto neutral studio background (`#F8F9FA`) with soft contact drop-shadow.

---

## 3. Stage 2: Bhashini Vernacular Speech & Translation
* **Objective**: Enable zero-typing listing generation in regional Indian languages (Tamil, Hindi, Telugu, etc.).
* **Pipeline**:
  1. Speech-to-Text (ASR) via Bhashini API specification.
  2. Language Identification.
  3. Neural Machine Translation (NMT) generating parallel English & Hindi catalog copy.

---

## 4. Stage 3: Structured Information Extraction
* **Objective**: Parse free-form spoken narratives into strict canonical attributes.
* **Attributes**: Product Name, Category, Subcategory, Craft Type, Materials, Dimensions, Weight, Labour Hours, Raw Material Cost, HSN Code, Artisan Story.
* **Audit Trail**: Every field carries provenance (`VOICE`, `ARTISAN`, `AI_SUGGESTED`, `AI_GENERATED`) and confidence scores (`HIGH`, `MEDIUM`, `LOW`).

---

## 5. Stage 4: Dynamic Fair-Price Recommender
* **Formula**:
  $$\text{BaseCost} = \text{MaterialCost} + (\text{LabourHours} \times \text{LabourRate}) + \text{Overhead}$$
  $$\text{MarketAdjusted} = \text{BaseCost} \times \text{MarketSignalMultiplier}$$
  $$\text{SuggestedPrice} = \text{clamp}(\text{MarketAdjusted}, \text{low}, \text{high})$$
* **Output**: A transparent suggested range (`recommended_low`, `recommended_mid`, `recommended_high`) accompanied by a plain-language explanation shown directly to the artisan.
