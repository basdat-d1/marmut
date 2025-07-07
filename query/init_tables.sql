-- ===================================
-- MARMUT DATABASE INITIALIZATION
-- ===================================
-- This file contains all table creation queries for the Marmut music streaming platform
-- Run this file in your PostgreSQL database to create all required tables

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS AKUN_PLAY_SONG CASCADE;
DROP TABLE IF EXISTS AKUN_PLAY_USER_PLAYLIST CASCADE;
DROP TABLE IF EXISTS PLAYLIST_SONG CASCADE;
DROP TABLE IF EXISTS ROYALTI CASCADE;
DROP TABLE IF EXISTS DOWNLOADED_SONG CASCADE;
DROP TABLE IF EXISTS SONGWRITER_WRITE_SONG CASCADE;
DROP TABLE IF EXISTS SONG CASCADE;
DROP TABLE IF EXISTS EPISODE CASCADE;
DROP TABLE IF EXISTS PODCAST CASCADE;
DROP TABLE IF EXISTS ARTIST CASCADE;
DROP TABLE IF EXISTS SONGWRITER CASCADE;
DROP TABLE IF EXISTS ALBUM CASCADE;
DROP TABLE IF EXISTS USER_PLAYLIST CASCADE;
DROP TABLE IF EXISTS CHART CASCADE;
DROP TABLE IF EXISTS PLAYLIST CASCADE;
DROP TABLE IF EXISTS LABEL CASCADE;
DROP TABLE IF EXISTS PEMILIK_HAK_CIPTA CASCADE;
DROP TABLE IF EXISTS PODCASTER CASCADE;
DROP TABLE IF EXISTS GENRE CASCADE;
DROP TABLE IF EXISTS KONTEN CASCADE;
DROP TABLE IF EXISTS TRANSACTION CASCADE;
DROP TABLE IF EXISTS PREMIUM CASCADE;
DROP TABLE IF EXISTS NONPREMIUM CASCADE;
DROP TABLE IF EXISTS PAKET CASCADE;
DROP TABLE IF EXISTS AKUN CASCADE;

-- ===================================
-- MAIN TABLES
-- ===================================

-- 1. AKUN (Account) - Base table for all users
CREATE TABLE AKUN (
    email VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    nama VARCHAR(100) NOT NULL,
    gender INT NOT NULL CHECK (gender IN (0, 1)), -- 0 = perempuan, 1 = laki-laki
    tempat_lahir VARCHAR(50) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    kota_asal VARCHAR(50) NOT NULL
);

-- 2. PAKET - Subscription packages
CREATE TABLE PAKET (
    jenis VARCHAR(50) PRIMARY KEY,
    harga INT NOT NULL
);

-- 3. TRANSACTIONS - Subscription transactions
CREATE TABLE TRANSACTION (
    id UUID DEFAULT gen_random_uuid(),
    jenis_paket VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    timestamp_dimulai TIMESTAMP NOT NULL,
    timestamp_berakhir TIMESTAMP NOT NULL,
    metode_bayar VARCHAR(50) NOT NULL,
    nominal INT NOT NULL,
    PRIMARY KEY (id, jenis_paket, email),
    FOREIGN KEY (jenis_paket) REFERENCES PAKET(jenis) ON DELETE CASCADE,
    FOREIGN KEY (email) REFERENCES AKUN(email) ON DELETE CASCADE
);

-- 4. PREMIUM - Premium users
CREATE TABLE PREMIUM (
    email VARCHAR(50) PRIMARY KEY REFERENCES AKUN(email) ON DELETE CASCADE
);

-- 5. NONPREMIUM - Non-premium users
CREATE TABLE NONPREMIUM (
    email VARCHAR(50) PRIMARY KEY REFERENCES AKUN(email) ON DELETE CASCADE
);

-- 6. KONTEN - Base content table
CREATE TABLE KONTEN (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    judul VARCHAR(100) NOT NULL,
    tanggal_rilis DATE NOT NULL,
    tahun INT NOT NULL,
    durasi INT NOT NULL -- in minutes
);

-- 7. GENRE - Content genres (many-to-many)
CREATE TABLE GENRE (
    id_konten UUID REFERENCES KONTEN(id) ON DELETE CASCADE,
    genre VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_konten, genre)
);

-- 8. PODCASTER - Podcast creators
CREATE TABLE PODCASTER (
    email VARCHAR(50) PRIMARY KEY REFERENCES AKUN(email) ON DELETE CASCADE
);

-- 9. PODCAST - Podcasts
CREATE TABLE PODCAST (
    id_konten UUID PRIMARY KEY REFERENCES KONTEN(id) ON DELETE CASCADE,
    email_podcaster VARCHAR(50) REFERENCES PODCASTER(email) ON DELETE CASCADE
);

-- 10. EPISODE - Podcast episodes
CREATE TABLE EPISODE (
    id_episode UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_konten_podcast UUID REFERENCES PODCAST(id_konten) ON DELETE CASCADE,
    judul VARCHAR(100) NOT NULL,
    deskripsi VARCHAR(500) NOT NULL,
    durasi INT NOT NULL,
    tanggal_rilis DATE NOT NULL
);

-- 11. PEMILIK_HAK_CIPTA - Copyright owners
CREATE TABLE PEMILIK_HAK_CIPTA (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rate_royalti INT NOT NULL
);

-- 12. ARTIST - Music artists
CREATE TABLE ARTIST (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_akun VARCHAR(50) REFERENCES AKUN(email) ON DELETE CASCADE,
    id_pemilik_hak_cipta UUID REFERENCES PEMILIK_HAK_CIPTA(id) ON DELETE CASCADE
);

-- 13. SONGWRITER - Song writers
CREATE TABLE SONGWRITER (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_akun VARCHAR(50) REFERENCES AKUN(email) ON DELETE CASCADE,
    id_pemilik_hak_cipta UUID REFERENCES PEMILIK_HAK_CIPTA(id) ON DELETE CASCADE
);

-- 14. LABEL - Music record labels
CREATE TABLE LABEL (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    kontak VARCHAR(50) NOT NULL,
    id_pemilik_hak_cipta UUID REFERENCES PEMILIK_HAK_CIPTA(id) ON DELETE CASCADE
);

-- 15. ALBUM - Music albums
CREATE TABLE ALBUM (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    judul VARCHAR(100) NOT NULL,
    jumlah_lagu INT NOT NULL DEFAULT 0,
    id_label UUID REFERENCES LABEL(id) ON DELETE CASCADE,
    total_durasi INT NOT NULL DEFAULT 0
);

-- 16. SONG - Songs
CREATE TABLE SONG (
    id_konten UUID PRIMARY KEY REFERENCES KONTEN(id) ON DELETE CASCADE,
    id_artist UUID REFERENCES ARTIST(id) ON DELETE CASCADE,
    id_album UUID REFERENCES ALBUM(id) ON DELETE CASCADE,
    total_play INT NOT NULL DEFAULT 0,
    total_download INT NOT NULL DEFAULT 0
);

-- 17. SONGWRITER_WRITE_SONG - Songwriters writing songs
CREATE TABLE SONGWRITER_WRITE_SONG (
    id_songwriter UUID REFERENCES SONGWRITER(id) ON DELETE CASCADE,
    id_song UUID REFERENCES SONG(id_konten) ON DELETE CASCADE,
    PRIMARY KEY (id_songwriter, id_song)
);

-- 18. DOWNLOADED_SONG - Downloaded songs by premium users
CREATE TABLE DOWNLOADED_SONG (
    id_song UUID REFERENCES SONG(id_konten) ON DELETE CASCADE,
    email_downloader VARCHAR(50) REFERENCES PREMIUM(email) ON DELETE CASCADE,
    PRIMARY KEY (id_song, email_downloader)
);

-- 19. PLAYLIST - Base playlist table
CREATE TABLE PLAYLIST (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);

-- 20. CHART - Music charts
CREATE TABLE CHART (
    tipe VARCHAR(50) PRIMARY KEY,
    id_playlist UUID REFERENCES PLAYLIST(id) ON DELETE CASCADE
);

-- 21. USER_PLAYLIST - User-created playlists
CREATE TABLE USER_PLAYLIST (
    email_pembuat VARCHAR(50) REFERENCES AKUN(email) ON DELETE CASCADE,
    id_user_playlist UUID NOT NULL,
    judul VARCHAR(100) NOT NULL,
    deskripsi VARCHAR(500) NOT NULL,
    jumlah_lagu INT NOT NULL,
    tanggal_dibuat DATE NOT NULL,
    id_playlist UUID REFERENCES PLAYLIST(id) ON DELETE CASCADE,
    total_durasi INT NOT NULL DEFAULT 0,
    PRIMARY KEY (email_pembuat, id_user_playlist)
);

-- 22. ROYALTI - Royalty information
CREATE TABLE ROYALTI (
    id_pemilik_hak_cipta UUID REFERENCES PEMILIK_HAK_CIPTA(id) ON DELETE CASCADE,
    id_song UUID REFERENCES SONG(id_konten) ON DELETE CASCADE,
    jumlah INT NOT NULL,
    PRIMARY KEY (id_pemilik_hak_cipta, id_song)
);

-- 23. AKUN_PLAY_USER_PLAYLIST - User playlist play history
CREATE TABLE AKUN_PLAY_USER_PLAYLIST (
    email_pemain VARCHAR(50) REFERENCES AKUN(email) ON DELETE CASCADE,
    id_user_playlist UUID NOT NULL,
    email_pembuat VARCHAR(50) NOT NULL,
    waktu TIMESTAMP NOT NULL,
    PRIMARY KEY (email_pemain, id_user_playlist, email_pembuat, waktu),
    FOREIGN KEY (id_user_playlist, email_pembuat) REFERENCES USER_PLAYLIST(id_user_playlist, email_pembuat) ON DELETE CASCADE
);

-- 24. AKUN_PLAY_SONG - Song play history
CREATE TABLE AKUN_PLAY_SONG (
    email_pemain VARCHAR(50) REFERENCES AKUN(email) ON DELETE CASCADE,
    id_song UUID REFERENCES SONG(id_konten) ON DELETE CASCADE,
    waktu TIMESTAMP NOT NULL,
    PRIMARY KEY (email_pemain, id_song, waktu)
);

-- 25. PLAYLIST_SONG - Songs in playlists
CREATE TABLE PLAYLIST_SONG (
    id_playlist UUID REFERENCES PLAYLIST(id) ON DELETE CASCADE,
    id_song UUID REFERENCES SONG(id_konten) ON DELETE CASCADE,
    PRIMARY KEY (id_playlist, id_song)
);