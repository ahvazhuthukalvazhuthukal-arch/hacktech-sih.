/// KalaiPaalam AI - HTTP Client Service
/// Connects Flutter mobile client to the central FastAPI backend.

import 'dart:convert';
import 'dart:typed_int';
import 'package:http/http.dart' as http;
import '../models/canonical_product.dart';

class ApiClient {
  static const String baseUrl = 'http://10.0.2.2:8040'; // Standard Android emulator host or localhost:8040

  static Future<List<CanonicalProduct>> getProducts() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/products/'));
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => CanonicalProduct.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  static Future<Map<String, dynamic>> processAI({
    String? spokenText,
    String language = 'ta',
    String? existingImageUrl,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/products/ai_process'),
      body: {
        if (spokenText != null) 'spoken_text': spokenText,
        'language': language,
        if (existingImageUrl != null) 'existing_image_url': existingImageUrl,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to process craft with AI Studio');
    }
  }

  static Future<Map<String, dynamic>> publishToStores(String productId, List<String> channels) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/products/$productId/publish'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'channels': channels}),
    );
    return jsonDecode(response.body);
  }

  static Future<Map<String, dynamic>> syncPrice(String productId, double newPrice) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/products/$productId/sync_price'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'price': newPrice}),
    );
    return jsonDecode(response.body);
  }

  static Future<List<dynamic>> getMarketplaces() async {
    final response = await http.get(Uri.parse('$baseUrl/api/marketplaces/'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return [];
  }
}
