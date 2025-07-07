# 🚀 Marmut Setup Guide - Supabase & Optimization

**Untuk memverifikasi koneksi:**
```bash
# Jalankan backend
cd marmut
python manage.py runserver 8000

# Jalankan frontend
cd marmut-fe
npm run dev
```

**Cara menjalankan trigger:**

1. **Buka Supabase Dashboard** → SQL Editor
2. **Copy & paste** isi file `setup_database.sql`
3. **Klik Run** untuk mengeksekusi semua trigger
4. **Trigger akan berjalan otomatis** setelah itu

**Trigger yang akan diinstall:**
- ✅ Email validation & uniqueness
- ✅ Auto premium/non-premium user management
- ✅ Playlist duration & song count updates
- ✅ Play count & download count tracking
- ✅ Subscription management
- ✅ Content duration calculations

## 🗄️ Database Setup

### Step 1: Jalankan Trigger & Index
```sql
-- Jalankan di Supabase SQL Editor
-- File: setup_database.sql (sudah dibuat)

-- Contoh trigger penting:
CREATE TRIGGER check_email_exists
BEFORE INSERT ON AKUN
FOR EACH ROW
EXECUTE FUNCTION check_email_exists();

-- Contoh index untuk performance:
CREATE INDEX idx_akun_email ON AKUN(email);
CREATE INDEX idx_song_total_play ON SONG(total_play DESC);
```

### Step 2: Verifikasi Installation
```sql
-- Check triggers
SELECT trigger_name, event_object_table 
FROM information_schema.triggers 
WHERE trigger_schema = 'public';

-- Check indexes
SELECT indexname FROM pg_indexes 
WHERE schemaname = 'public' 
AND indexname LIKE 'idx_%';
```

## ⚡ Performance Optimization

### 📊 Index Categories

#### 1. **Primary Lookup Indexes**
```sql
-- Email-based lookups (most frequent)
CREATE INDEX idx_akun_email ON AKUN(email);
CREATE INDEX idx_premium_email ON PREMIUM(email);
CREATE INDEX idx_user_playlist_email ON USER_PLAYLIST(email_pembuat);
```

#### 2. **Search & Content Indexes**
```sql
-- Full-text search
CREATE INDEX idx_konten_search ON KONTEN USING gin(to_tsvector('english', judul));

-- Content popularity
CREATE INDEX idx_song_total_play ON SONG(total_play DESC);
CREATE INDEX idx_song_total_download ON SONG(total_download DESC);
```

#### 3. **Relationship Indexes**
```sql
-- Foreign key relationships
CREATE INDEX idx_song_id_album ON SONG(id_album);
CREATE INDEX idx_playlist_song_composite ON PLAYLIST_SONG(id_playlist, id_song);
```

#### 4. **Time-based Indexes**
```sql
-- Recent content & transactions
CREATE INDEX idx_konten_tanggal_rilis ON KONTEN(tanggal_rilis);
CREATE INDEX idx_transaction_timestamp ON TRANSACTION(timestamp_dimulai, timestamp_berakhir);
```

## 🔧 Backend Configuration

### Django Settings Verification
```python
# settings.py - Gunakan credentials database kalian
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "...",
        "USER": "...",
        "PASSWORD": "...",
        "HOST": "...",
        "PORT": "...",
    }
}

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```