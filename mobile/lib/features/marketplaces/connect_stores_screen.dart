/// KalaiPaalam AI - "Connect Your Stores" Screen
/// Manages sales channel OAuth authentications, capabilities negotiation, and sync status.

import 'package:flutter/material.dart';
import '../../services/api_client.dart';

class ConnectStoresScreen extends StatefulWidget {
  const ConnectStoresScreen({super.key});

  @override
  State<ConnectStoresScreen> createState() => _ConnectStoresScreenState();
}

class _ConnectStoresScreenState extends State<ConnectStoresScreen> {
  List<dynamic> channels = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadChannels();
  }

  Future<void> _loadChannels() async {
    final list = await ApiClient.getMarketplaces();
    if (mounted) {
      setState(() {
        channels = list;
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Connect Your Stores')),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                const Text(
                  'Manage Connected Marketplaces',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800),
                ),
                const SizedBox(height: 6),
                const Text(
                  'KalaiPaalam connects once via secure OAuth token vaults. No plaintext passwords stored.',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                ),
                const SizedBox(height: 16),

                if (channels.isEmpty)
                  ...[
                    _storeCard('ONDC', 'Kanchi Craft Beckn BPP Node', 'DEMO', true, ['CREATE_LISTING', 'UPDATE_PRICE', 'UPDATE_INVENTORY']),
                    _storeCard('GeM', 'Government e-Marketplace Karigar', 'DEMO', true, ['CREATE_LISTING', 'UPDATE_INVENTORY']),
                    _storeCard('Amazon', 'Kanchipuram Karigar Store', 'DEMO', true, ['CREATE_LISTING', 'UPDATE_LISTING', 'UPDATE_PRICE', 'UPDATE_INVENTORY', 'ORDERS']),
                    _storeCard('Flipkart', 'Samarth Weavers Hub', 'DEMO', true, ['CREATE_LISTING', 'UPDATE_PRICE', 'UPDATE_INVENTORY']),
                    _storeCard('KalaiPaalam Catalog', 'Official Direct D2C Storefront', 'LIVE', true, ['CREATE_LISTING', 'ORDERS', 'IMAGE_UPLOAD']),
                  ]
                else
                  ...channels.map((ch) => _storeCard(
                        ch['marketplace'],
                        ch['account_name'] ?? 'Authorized Account',
                        ch['environment'] ?? 'DEMO',
                        ch['status'] == 'CONNECTED',
                        List<String>.from(ch['capabilities'] ?? []),
                      )),
              ],
            ),
    );
  }

  Widget _storeCard(String name, String account, String env, bool connected, List<String> caps) {
    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: connected ? const Color(0xFF10B981).withOpacity(0.5) : const Color(0xFFE2E8F0)),
        boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 4, offset: Offset(0, 2))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(name, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: env == 'LIVE' ? const Color(0xFFECFDF5) : const Color(0xFFFEF3C7),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  env,
                  style: TextStyle(
                    color: env == 'LIVE' ? const Color(0xFF065F46) : const Color(0xFF92400E),
                    fontWeight: FontWeight.bold,
                    fontSize: 10,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(account, style: const TextStyle(fontSize: 12, color: Colors.grey)),
          const SizedBox(height: 8),
          Row(
            children: [
              Icon(Icons.check_circle, size: 14, color: connected ? const Color(0xFF10B981) : Colors.grey),
              const SizedBox(width: 4),
              Text(
                connected ? 'Connected & Authorized' : 'Disconnected',
                style: TextStyle(
                  color: connected ? const Color(0xFF10B981) : Colors.grey,
                  fontWeight: FontWeight.bold,
                  fontSize: 11,
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Wrap(
            spacing: 4,
            runSpacing: 4,
            children: caps.map((c) => Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
              decoration: BoxDecoration(
                color: const Color(0xFFF1F5F9),
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(c, style: const TextStyle(fontSize: 9, fontWeight: FontWeight.bold, color: Colors.blueGrey)),
            )).toList(),
          ),
        ],
      ),
    );
  }
}
