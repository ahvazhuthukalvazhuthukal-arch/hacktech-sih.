/// KalaiPaalam AI - Offline-First SQLite Cache & Drafts Manager
/// Preserves products, pending sync operations, and voice metadata when internet is unavailable.

import 'dart:convert';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/canonical_product.dart';

class OfflineDatabase {
  static final OfflineDatabase instance = OfflineDatabase._init();
  static Database? _database;

  OfflineDatabase._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('kalaipaalam_offline.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }

  Future _createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE local_drafts (
        id TEXT PRIMARY KEY,
        title TEXT,
        category TEXT,
        price REAL,
        inventory INTEGER,
        raw_image_path TEXT,
        processed_image_path TEXT,
        voice_transcript TEXT,
        status TEXT,
        canonical_json TEXT,
        created_at TEXT
      )
    ''');

    await db.execute('''
      CREATE TABLE pending_sync_jobs (
        job_id TEXT PRIMARY KEY,
        product_id TEXT,
        target_channels TEXT,
        status TEXT,
        created_at TEXT
      )
    ''');
  }

  Future<void> saveLocalDraft(CanonicalProduct product) async {
    final db = await instance.database;
    await db.insert(
      'local_drafts',
      {
        'id': product.productId,
        'title': product.title,
        'category': product.category,
        'price': product.price,
        'inventory': product.inventory,
        'raw_image_path': product.originalImageUrl,
        'processed_image_path': product.processedImageUrl,
        'voice_transcript': product.voiceTranscript,
        'status': 'PENDING_SYNC',
        'canonical_json': jsonEncode(product.toJson()),
        'created_at': DateTime.now().toIso8601String(),
      },
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<List<CanonicalProduct>> getLocalDrafts() async {
    final db = await instance.database;
    final result = await db.query('local_drafts', orderBy: 'created_at DESC');

    return result.map((row) {
      final jsonMap = jsonDecode(row['canonical_json'] as String);
      return CanonicalProduct.fromJson(jsonMap);
    }).toList();
  }

  Future<void> enqueueSyncJob(String productId, List<String> targetChannels) async {
    final db = await instance.database;
    final jobId = 'job_${DateTime.now().millisecondsSinceEpoch}';
    await db.insert('pending_sync_jobs', {
      'job_id': jobId,
      'product_id': productId,
      'target_channels': jsonEncode(targetChannels),
      'status': 'PENDING',
      'created_at': DateTime.now().toIso8601String(),
    });
  }

  Future<List<Map<String, dynamic>>> getPendingSyncJobs() async {
    final db = await instance.database;
    return await db.query('pending_sync_jobs', where: 'status = ?', whereArgs: ['PENDING']);
  }

  Future<void> markJobSynced(String jobId) async {
    final db = await instance.database;
    await db.update('pending_sync_jobs', {'status': 'SYNCED'}, where: 'job_id = ?', whereArgs: [jobId]);
  }
}
