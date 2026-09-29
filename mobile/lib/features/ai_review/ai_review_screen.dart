/// KalaiPaalam AI - AI Review & Pricing Screen
/// Displays Before/After image matting, Touch-to-confirm cards, and Fair Price recommendation.

import 'package:flutter/material.dart';
import '../marketplaces/select_marketplace_screen.dart';

class AIReviewScreen extends StatelessWidget {
  final Map<String, dynamic> productData;

  const AIReviewScreen({super.key, required this.productData});

  @override
  Widget build(BuildContext context) {
    final title = productData['title'] ?? 'Handwoven Cotton Saree';
    final price = (productData['price'] ?? 5500.0).toDouble();
    final hsn = productData['hsn_code'] ?? '5208';
    final rec = productData['recommended_price_range'] ?? {};

    return Scaffold(
      appBar: AppBar(title: const Text('Review AI Listing')),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          // Studio Image Box
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: const Color(0xFFE2E8F0)),
            ),
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('AI Studio Enhancement', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        color: const Color(0xFFECFDF5),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: const Text('Edge Matting ✓', style: TextStyle(color: Color(0xFF065F46), fontWeight: FontWeight.bold, fontSize: 10)),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Container(
                  height: 150,
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.auto_awesome, color: Color(0xFFC85A32), size: 36),
                        SizedBox(height: 4),
                        Text('Master Studio Catalog Image Ready', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                        Text('Background removed • Fabric texture preserved', style: TextStyle(color: Colors.grey, fontSize: 10)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Confirmation Cards
          _infoCard('Product Title', title, 'VOICE'),
          _infoCard('Category & Technique', '${productData['category']} • ${productData['craft_type']}', 'AI SUGGESTED'),
          _infoCard('HSN Code (Tax/Export)', '$hsn (Harmonized System)', 'AI SUGGESTED'),
          _infoCard('Craft Story', productData['craft_story'] ?? 'Woven by artisan Meenakshi.', 'VOICE'),

          const SizedBox(height: 16),

          // Fair Price Recommendation Card
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFFFFFBEB),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: const Color(0xFFFDE68A)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Dynamic Fair-Price Recommendation',
                  style: TextStyle(color: Color(0xFF92400E), fontWeight: FontWeight.w800, fontSize: 13),
                ),
                const SizedBox(height: 6),
                Text(
                  '₹${price.toStringAsFixed(0)}',
                  style: const TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: Color(0xFF92400E)),
                ),
                Text(
                  'Suggested Range: ₹${rec['low'] ?? 5200} – ₹${rec['high'] ?? 5900}',
                  style: const TextStyle(color: Color(0xFFB45309), fontSize: 12, fontWeight: FontWeight.bold),
                ),
                const Divider(height: 20, color: Color(0xFFFCD34D)),
                const Text(
                  'Breakdown: Raw material + 40 hrs skilled labour (@ ₹120/hr) + overhead + 1.12x market signal.',
                  style: TextStyle(color: Color(0xFF78350F), fontSize: 11, height: 1.4),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          SizedBox(
            width: double.infinity,
            height: 52,
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFFC85A32),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => SelectMarketplaceScreen(productData: productData),
                  ),
                );
              },
              child: const Text(
                'Continue to Where to Sell? →',
                style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _infoCard(String label, String value, String source) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey, fontWeight: FontWeight.bold)),
                const SizedBox(height: 2),
                Text(value, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold)),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: const Color(0xFFF1F5F9),
              borderRadius: BorderRadius.circular(4),
            ),
            child: Text(source, style: const TextStyle(fontSize: 9, fontWeight: FontWeight.bold, color: Colors.blueGrey)),
          ),
        ],
      ),
    );
  }
}
