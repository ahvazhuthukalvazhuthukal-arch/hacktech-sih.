/// KalaiPaalam AI - Select Marketplace & 1-Click Publishing Screen

import 'package:flutter/material.dart';
import '../../services/api_client.dart';

class SelectMarketplaceScreen extends StatefulWidget {
  final Map<String, dynamic> productData;

  const SelectMarketplaceScreen({super.key, required this.productData});

  @override
  State<SelectMarketplaceScreen> createState() => _SelectMarketplaceScreenState();
}

class _SelectMarketplaceScreenState extends State<SelectMarketplaceScreen> {
  final List<String> selectedChannels = [
    'KalaiPaalam Catalog',
    'ONDC',
    'GeM',
    'Amazon',
    'Flipkart',
  ];
  bool isPublishing = false;
  bool isPublished = false;

  void _publish() async {
    setState(() => isPublishing = true);

    try {
      final pid = widget.productData['product_id'] ?? 'KP-001';
      await ApiClient.publishToStores(pid, selectedChannels);
      if (mounted) {
        setState(() {
          isPublishing = false;
          isPublished = true;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => isPublishing = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Where Do You Want to Sell?')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Select Marketplaces',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 6),
            const Text(
              'One product automatically transforms into each platform’s required schema.',
              style: TextStyle(fontSize: 12, color: Colors.grey),
            ),
            const SizedBox(height: 16),

            _channelTile('KalaiPaalam D2C Catalog', 'Direct buyer storefront • Live orders', 'KalaiPaalam Catalog'),
            _channelTile('ONDC (Beckn Protocol)', 'Open Network discovery • BPP Item', 'ONDC'),
            _channelTile('GeM (Government e-Marketplace)', 'Public Procurement Feed • SHG Portal', 'GeM'),
            _channelTile('Amazon Karigar', 'SP-API formatted catalog listing', 'Amazon'),
            _channelTile('Flipkart Samarth', 'Samarth Weavers listing feed', 'Flipkart'),

            const Spacer(),

            if (isPublished)
              Container(
                padding: const EdgeInsets.all(14),
                margin: const EdgeInsets.only(bottom: 14),
                decoration: BoxDecoration(
                  color: const Color(0xFFECFDF5),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: const Color(0xFF10B981)),
                ),
                child: const Row(
                  children: [
                    Icon(Icons.check_circle, color: Color(0xFF065F46)),
                    SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Published! 1 craft product is now active across all 5 sales channels.',
                        style: TextStyle(color: Color(0xFF065F46), fontWeight: FontWeight.bold, fontSize: 12),
                      ),
                    ),
                  ],
                ),
              ),

            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFC85A32),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                onPressed: isPublishing || isPublished
                    ? () => Navigator.popUntil(context, ModalRoute.withName('/home'))
                    : _publish,
                child: isPublishing
                    ? const CircularProgressIndicator(color: Colors.white)
                    : Text(
                        isPublished ? 'Return to Home 🏠' : '🚀 Publish to Selected Stores',
                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _channelTile(String title, String subtitle, String channelKey) {
    final isSelected = selectedChannels.contains(channelKey);
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
        color: isSelected ? const Color(0xFFFBF1EC) : Colors.white,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: isSelected ? const Color(0xFFC85A32) : const Color(0xFFE2E8F0)),
      ),
      child: CheckboxListTile(
        activeColor: const Color(0xFFC85A32),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
        subtitle: Text(subtitle, style: const TextStyle(fontSize: 11, color: Colors.grey)),
        value: isSelected,
        onChanged: (val) {
          setState(() {
            if (val == true) {
              selectedChannels.add(channelKey);
            } else {
              selectedChannels.remove(channelKey);
            }
          });
        },
      ),
    );
  }
}
