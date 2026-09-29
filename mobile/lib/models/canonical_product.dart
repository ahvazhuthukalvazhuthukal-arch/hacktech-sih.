/// KalaiPaalam AI - Canonical Product Model for Flutter Mobile Application
/// Shared schema with FastAPI backend and marketplace connector engine.

import 'dart:convert';

class CanonicalProduct {
  final String productId;
  final String artisanId;
  final String artisanName;
  final String clusterName;
  final String region;
  final String title;
  final String? hindiTitle;
  final String? tamilTitle;
  final String description;
  final String? hindiDescription;
  final String category;
  final String subcategory;
  final String craftType;
  final List<String> material;
  final List<String> colors;
  final Map<String, dynamic> dimensions;
  final double weightGrams;
  final String hsnCode;
  final String countryOfOrigin;
  final double labourHours;
  final double materialCost;
  final double price;
  final Map<String, dynamic> recommendedPriceRange;
  final int inventory;
  final String sku;
  final String? originalImageUrl;
  final String? processedImageUrl;
  final String? voiceTranscript;
  final String detectedLanguage;
  final String? craftStory;
  final Map<String, String> confidenceScores;
  final Map<String, String> provenance;
  final String status;
  final Map<String, dynamic> marketplaceChannels;

  CanonicalProduct({
    required this.productId,
    required this.artisanId,
    required this.artisanName,
    required this.clusterName,
    required this.region,
    required this.title,
    this.hindiTitle,
    this.tamilTitle,
    required this.description,
    this.hindiDescription,
    required this.category,
    required this.subcategory,
    required this.craftType,
    required this.material,
    required this.colors,
    required this.dimensions,
    required this.weightGrams,
    required this.hsnCode,
    this.countryOfOrigin = 'India',
    required this.labourHours,
    required this.materialCost,
    required this.price,
    required this.recommendedPriceRange,
    required this.inventory,
    required this.sku,
    this.originalImageUrl,
    this.processedImageUrl,
    this.voiceTranscript,
    this.detectedLanguage = 'ta',
    this.craftStory,
    required this.confidenceScores,
    required this.provenance,
    required this.status,
    required this.marketplaceChannels,
  });

  factory CanonicalProduct.fromJson(Map<String, dynamic> json) {
    return CanonicalProduct(
      productId: json['product_id'] ?? '',
      artisanId: json['artisan_id'] ?? 'artisan_demo_01',
      artisanName: json['artisan_name'] ?? 'Meenakshi Sundaram',
      clusterName: json['cluster_name'] ?? 'Kanchipuram Heritage Guild',
      region: json['region'] ?? 'Kanchipuram, Tamil Nadu',
      title: json['title'] ?? '',
      hindiTitle: json['hindi_title'],
      tamilTitle: json['tamil_title'],
      description: json['description'] ?? '',
      hindiDescription: json['hindi_description'],
      category: json['category'] ?? 'Textiles & Handloom',
      subcategory: json['subcategory'] ?? 'Saree',
      craftType: json['craft_type'] ?? 'Handloom Weaving',
      material: List<String>.from(json['material'] ?? ['Cotton']),
      colors: List<String>.from(json['colors'] ?? ['Blue']),
      dimensions: Map<String, dynamic>.from(json['dimensions'] ?? {}),
      weightGrams: (json['weight_grams'] ?? 500.0).toDouble(),
      hsnCode: json['hsn_code'] ?? '5208',
      countryOfOrigin: json['country_of_origin'] ?? 'India',
      labourHours: (json['labour_hours'] ?? 16.0).toDouble(),
      materialCost: (json['material_cost'] ?? 500.0).toDouble(),
      price: (json['price'] ?? 0.0).toDouble(),
      recommendedPriceRange: Map<String, dynamic>.from(json['recommended_price_range'] ?? {}),
      inventory: json['inventory'] ?? 10,
      sku: json['sku'] ?? 'SKU-001',
      originalImageUrl: json['original_image_url'],
      processedImageUrl: json['processed_image_url'],
      voiceTranscript: json['voice_transcript'],
      detectedLanguage: json['detected_language'] ?? 'ta',
      craftStory: json['craft_story'],
      confidenceScores: Map<String, String>.from(json['confidence_scores'] ?? {}),
      provenance: Map<String, String>.from(json['provenance'] ?? {}),
      status: json['status'] ?? 'READY',
      marketplaceChannels: Map<String, dynamic>.from(json['marketplace_channels'] ?? {}),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'product_id': productId,
      'artisan_id': artisanId,
      'artisan_name': artisanName,
      'cluster_name': clusterName,
      'region': region,
      'title': title,
      'hindi_title': hindiTitle,
      'tamil_title': tamilTitle,
      'description': description,
      'hindi_description': hindiDescription,
      'category': category,
      'subcategory': subcategory,
      'craft_type': craftType,
      'material': material,
      'colors': colors,
      'dimensions': dimensions,
      'weight_grams': weightGrams,
      'hsn_code': hsnCode,
      'country_of_origin': countryOfOrigin,
      'labour_hours': labourHours,
      'material_cost': materialCost,
      'price': price,
      'recommended_price_range': recommendedPriceRange,
      'inventory': inventory,
      'sku': sku,
      'original_image_url': originalImageUrl,
      'processed_image_url': processedImageUrl,
      'voice_transcript': voiceTranscript,
      'detected_language': detectedLanguage,
      'craft_story': craftStory,
      'confidence_scores': confidenceScores,
      'provenance': provenance,
      'status': status,
      'marketplace_channels': marketplaceChannels,
    };
  }
}
