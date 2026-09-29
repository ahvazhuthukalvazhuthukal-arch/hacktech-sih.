/// KalaiPaalam AI - Camera Capture & Voice Recording Screen

import 'package:flutter/material.dart';
import '../../services/api_client.dart';
import '../ai_review/ai_review_screen.dart';

class CameraCaptureScreen extends StatefulWidget {
  const CameraCaptureScreen({super.key});

  @override
  State<CameraCaptureScreen> createState() => _CameraCaptureScreenState();
}

class _CameraCaptureScreenState extends State<CameraCaptureScreen> {
  String selectedSample = 'saree';
  String spokenLanguage = 'ta';
  bool isProcessing = false;

  void _triggerAI() async {
    setState(() => isProcessing = true);

    try {
      final imgUrl = selectedSample == 'brass'
          ? '/static/images/brass_raw.jpg'
          : '/static/images/saree_raw.jpg';

      final res = await ApiClient.processAI(
        existingImageUrl: imgUrl,
        language: spokenLanguage,
        spokenText: selectedSample == 'brass'
            ? 'यह पारंपरिक ढोकरा पीतल का मयूर दीपक है। तीन दिन लगे, सामग्री लागत 550 रुपये।'
            : 'இது எங்க காஞ்சிபுரம் குழு நெய்த தூய பருத்தி புடவை. செய்ய ரெண்டு நாள் ஆச்சு. மூலப்பொருள் செலவு 800 ரூபாய்.',
      );

      if (mounted) {
        setState(() => isProcessing = false);
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => AIReviewScreen(productData: res['product']),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        setState(() => isProcessing = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Processing completed: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Capture Craft & Voice')),
      body: isProcessing
          ? _loadingView()
          : Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('1. Craft Photo Capture', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
                  const SizedBox(height: 10),
                  Container(
                    height: 220,
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: const Color(0xFFE2E8F0)),
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          selectedSample == 'brass' ? Icons.wb_incandescent_outlined : Icons.checkroom_outlined,
                          size: 60,
                          color: const Color(0xFFC85A32),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          selectedSample == 'brass' ? 'Dhokra Brass Peacock Lamp' : 'Handloom Cotton Saree',
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                        ),
                        const SizedBox(height: 12),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            ChoiceChip(
                              label: const Text('Handloom Saree'),
                              selected: selectedSample == 'saree',
                              onSelected: (_) => setState(() => selectedSample = 'saree'),
                            ),
                            const SizedBox(width: 8),
                            ChoiceChip(
                              label: const Text('Brass Lamp'),
                              selected: selectedSample == 'brass',
                              onSelected: (_) => setState(() => selectedSample = 'brass'),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  const Text('2. Describe Craft by Voice (Bhashini)', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
                  const SizedBox(height: 10),
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: const Color(0xFFE2E8F0)),
                    ),
                    child: Column(
                      children: [
                        const Icon(Icons.mic, size: 48, color: Color(0xFFC85A32)),
                        const SizedBox(height: 8),
                        Text(
                          spokenLanguage == 'ta' ? 'தமிழ் குரல் பதிவு செயலில் உள்ளது' : 'हिन्दी में बोलें',
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                        ),
                        const SizedBox(height: 6),
                        const Text(
                          'Speak material, craft method, days taken, and cost.',
                          style: TextStyle(fontSize: 11, color: Colors.grey),
                        ),
                      ],
                    ),
                  ),
                  const Spacer(),
                  SizedBox(
                    width: double.infinity,
                    height: 52,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFC85A32),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      onPressed: _triggerAI,
                      child: const Text(
                        '✨ Run AI Studio & Listing →',
                        style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                      ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }

  Widget _loadingView() {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircularProgressIndicator(color: Color(0xFFC85A32)),
          SizedBox(height: 20),
          Text('AI Studio: Removing background & lighting...', style: TextStyle(fontWeight: FontWeight.bold)),
          SizedBox(height: 6),
          Text('Bhashini: Converting voice to structured catalog...', style: TextStyle(color: Colors.grey, fontSize: 12)),
        ],
      ),
    );
  }
}
