/// KalaiPaalam AI - Flutter Mobile Application
/// SIH26090: AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans
/// Theme: Heritage & Culture

import 'package:flutter/material.dart';
import 'features/home/home_screen.dart';
import 'features/camera/camera_screen.dart';
import 'features/marketplaces/connect_stores_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const KalaiPaalamApp());
}

class KalaiPaalamApp extends StatelessWidget {
  const KalaiPaalamApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'KalaiPaalam AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFC85A32), // Terracotta
          primary: const Color(0xFFC85A32),
          secondary: const Color(0xFFD4AF37), // Gold
          surface: const Color(0xFFFAFAFA),
        ),
        scaffoldBackgroundColor: const Color(0xFFF8FAFC),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.white,
          elevation: 0,
          scrolledUnderElevation: 1,
          iconTheme: IconThemeData(color: Color(0xFF0F172A)),
          titleTextStyle: TextStyle(
            color: Color(0xFF0F172A),
            fontSize: 18,
            fontWeight: FontWeight.w800,
          ),
        ),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const SplashScreen(),
        '/consent': (context) => const ConsentScreen(),
        '/home': (context) => const HomeScreen(),
        '/capture': (context) => const CameraCaptureScreen(),
        '/connect_stores': (context) => const ConnectStoresScreen(),
      },
    );
  }
}

/// 1. Splash Screen
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        Navigator.pushReplacementNamed(context, '/consent');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFFC85A32), Color(0xFF1A365D)],
          ),
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 90,
                height: 90,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(22),
                  boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 15)],
                ),
                child: const Center(
                  child: Text(
                    'க',
                    style: TextStyle(
                      fontSize: 48,
                      fontWeight: FontWeight.w900,
                      color: Color(0xFFC85A32),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                'KalaiPaalam AI',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.w900,
                  color: Colors.white,
                  letterSpacing: 1,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'Your Craft • One Catalog • Multiple Markets',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                  color: Colors.white70,
                ),
              ),
              const SizedBox(height: 20),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                decoration: BoxDecoration(
                  color: const Color(0xFFD4AF37).withOpacity(0.3),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: const Color(0xFFD4AF37)),
                ),
                child: const Text(
                  'SIH26090 • Heritage & Culture',
                  style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/// 2. Privacy & Vernacular Language Consent Screen
class ConsentScreen extends StatefulWidget {
  const ConsentScreen({super.key});

  @override
  State<ConsentScreen> createState() => _ConsentScreenState();
}

class _ConsentScreenState extends State<ConsentScreen> {
  String selectedLanguage = 'ta';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Language & Privacy')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Select Your Language',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                _langOption('தமிழ் (Tamil)', 'ta'),
                const SizedBox(width: 8),
                _langOption('हिन्दी (Hindi)', 'hi'),
                const SizedBox(width: 8),
                _langOption('English', 'en'),
              ],
            ),
            const SizedBox(height: 28),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFFBF1EC),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: const Color(0xFFC85A32).withOpacity(0.3)),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.shield_outlined, color: Color(0xFFC85A32)),
                      SizedBox(width: 8),
                      Text(
                        'Privacy-First Architecture',
                        style: TextStyle(fontWeight: FontWeight.w800, color: Color(0xFFC85A32)),
                      ),
                    ],
                  ),
                  SizedBox(height: 10),
                  Text(
                    'KalaiPaalam AI uses your photo and voice solely to generate your craft catalog and marketplace feeds. '
                    'Your data remains under your ownership. Aligned with DPDP principles.',
                    style: TextStyle(fontSize: 13, height: 1.4, color: Color(0xFF475569)),
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
                onPressed: () {
                  Navigator.pushReplacementNamed(context, '/home');
                },
                child: const Text(
                  'Accept & Continue →',
                  style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _langOption(String name, String code) {
    final isSelected = selectedLanguage == code;
    return Expanded(
      child: GestureDetector(
        onTap: () => setState(() => selectedLanguage = code),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFFC85A32) : Colors.white,
            border: Border.all(color: isSelected ? const Color(0xFFC85A32) : const Color(0xFFCBD5E1)),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Center(
            child: Text(
              name,
              style: TextStyle(
                color: isSelected ? Colors.white : const Color(0xFF0F172A),
                fontWeight: FontWeight.bold,
                fontSize: 12,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
