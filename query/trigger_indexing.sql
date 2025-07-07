-- ===================================
-- MARMUT DATABASE SETUP FOR SUPABASE
-- ===================================
-- This file contains all triggers and indexes needed for the Marmut application
-- Run this file in Supabase SQL Editor after creating all tables

-- ===================================
-- TRIGGERS SETUP
-- ===================================

-- TRIGGER GROUP 1: Account and User Management
-- 1. Check email uniqueness when registering new account
CREATE OR REPLACE FUNCTION check_email_exists()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM AKUN WHERE email = NEW.email) THEN
        RAISE EXCEPTION 'Email sudah pernah didaftarkan.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_email_exists
BEFORE INSERT ON AKUN
FOR EACH ROW
EXECUTE FUNCTION check_email_exists();

-- 2. Auto-create non-premium user when new user registers
CREATE OR REPLACE FUNCTION set_non_premium()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO NONPREMIUM(email) VALUES (NEW.email);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_non_premium
AFTER INSERT ON AKUN
FOR EACH ROW
EXECUTE FUNCTION set_non_premium();

-- 3. Check premium status expiration (Stored Procedure)
CREATE OR REPLACE FUNCTION check_premium_status(user_email VARCHAR(50))
RETURNS VOID AS $$
BEGIN
    -- Check if user has expired premium subscription
    IF EXISTS (
        SELECT 1 FROM TRANSACTION t
        JOIN PREMIUM p ON t.email = p.email
        WHERE t.email = user_email 
        AND t.timestamp_berakhir < CURRENT_TIMESTAMP
    ) THEN
        -- Move from premium to non-premium
        DELETE FROM PREMIUM WHERE email = user_email;
        INSERT INTO NONPREMIUM(email) VALUES (user_email)
        ON CONFLICT (email) DO NOTHING;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER GROUP 2: Playlist Management
-- 1. Update playlist attributes (duration and song count) when songs added/removed
CREATE OR REPLACE FUNCTION update_playlist_attributes()
RETURNS TRIGGER AS $$
DECLARE
    total_duration INT;
    total_songs INT;
    playlist_id UUID;
BEGIN
    -- Get the playlist ID from either USER_PLAYLIST or direct PLAYLIST
    IF TG_TABLE_NAME = 'PLAYLIST_SONG' THEN
        playlist_id := COALESCE(NEW.id_playlist, OLD.id_playlist);
        
        -- Update for USER_PLAYLIST if this playlist belongs to a user
        IF EXISTS (SELECT 1 FROM USER_PLAYLIST WHERE id_playlist = playlist_id) THEN
            SELECT SUM(K.durasi), COUNT(*) INTO total_duration, total_songs
            FROM PLAYLIST_SONG PS
            JOIN SONG S ON PS.id_song = S.id_konten
            JOIN KONTEN K ON S.id_konten = K.id
            WHERE PS.id_playlist = playlist_id;

            UPDATE USER_PLAYLIST 
            SET total_durasi = COALESCE(total_duration, 0), 
                jumlah_lagu = COALESCE(total_songs, 0)
            WHERE id_playlist = playlist_id;
        END IF;
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_playlist_attributes
AFTER INSERT OR DELETE ON PLAYLIST_SONG
FOR EACH ROW
EXECUTE FUNCTION update_playlist_attributes();

-- 2. Check duplicate song in playlist
CREATE OR REPLACE FUNCTION check_duplicate_song_playlist()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM PLAYLIST_SONG
        WHERE id_playlist = NEW.id_playlist AND id_song = NEW.id_song
    ) THEN
        RAISE EXCEPTION 'Lagu sudah ada dalam playlist.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_duplicate_song_playlist
BEFORE INSERT ON PLAYLIST_SONG
FOR EACH ROW
EXECUTE FUNCTION check_duplicate_song_playlist();

-- 3. Check duplicate downloaded song
CREATE OR REPLACE FUNCTION check_duplicate_downloaded_song()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM DOWNLOADED_SONG
        WHERE id_song = NEW.id_song
        AND email_downloader = NEW.email_downloader
    ) THEN
        RAISE EXCEPTION 'Lagu sudah pernah diunduh.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_duplicate_downloaded_song
BEFORE INSERT ON DOWNLOADED_SONG
FOR EACH ROW
EXECUTE FUNCTION check_duplicate_downloaded_song();

-- TRIGGER GROUP 3: Subscription Management
-- 1. Check active subscription package before purchasing new one
CREATE OR REPLACE FUNCTION check_active_package()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if there is any active subscription for this user
    IF EXISTS (
        SELECT 1 FROM TRANSACTION WHERE email = NEW.email
        AND timestamp_dimulai <= CURRENT_TIMESTAMP
        AND timestamp_berakhir >= CURRENT_TIMESTAMP
    ) THEN
        RAISE EXCEPTION 'User % already has an active subscription package.', NEW.email;
    END IF;

    -- Remove from NONPREMIUM and add to PREMIUM
    DELETE FROM NONPREMIUM WHERE email = NEW.email;
    INSERT INTO PREMIUM(email) VALUES (NEW.email)
    ON CONFLICT (email) DO NOTHING;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_active_package
BEFORE INSERT ON TRANSACTION
FOR EACH ROW
EXECUTE FUNCTION check_active_package();

-- 2. Sync playlist songs when playing user playlist
CREATE OR REPLACE FUNCTION sync_playlist_songs()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert records into AKUN_PLAY_SONG for each song in the played playlist
    INSERT INTO AKUN_PLAY_SONG(email_pemain, id_song, waktu)
    SELECT NEW.email_pemain, PS.id_song, NEW.waktu 
    FROM PLAYLIST_SONG PS
    JOIN USER_PLAYLIST UP ON PS.id_playlist = UP.id_playlist
    WHERE UP.id_user_playlist = NEW.id_user_playlist 
    AND UP.email_pembuat = NEW.email_pembuat;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_playlist_songs
AFTER INSERT ON AKUN_PLAY_USER_PLAYLIST
FOR EACH ROW
EXECUTE FUNCTION sync_playlist_songs();

-- TRIGGER GROUP 4: Play and Download Tracking
-- 1. Update total play count when song is added to playlist (not when played)
CREATE OR REPLACE FUNCTION update_total_play_on_playlist_add() 
RETURNS TRIGGER AS $$
BEGIN
    -- Update total_play in SONG table when a song is added to playlist
    UPDATE SONG SET total_play = total_play + 1
    WHERE id_konten = NEW.id_song;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_total_play_on_playlist_add
AFTER INSERT ON PLAYLIST_SONG
FOR EACH ROW
EXECUTE FUNCTION update_total_play_on_playlist_add();

-- 2. Increment total_download when a song is downloaded
CREATE OR REPLACE FUNCTION increment_total_download()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE SONG SET total_download = total_download + 1
    WHERE id_konten = NEW.id_song;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER increment_total_download
AFTER INSERT ON DOWNLOADED_SONG
FOR EACH ROW
EXECUTE FUNCTION increment_total_download();

-- 3. Decrement total_download when a download is removed
CREATE OR REPLACE FUNCTION decrement_total_download() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE SONG SET total_download = total_download - 1
    WHERE id_konten = OLD.id_song;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER decrement_total_download
AFTER DELETE ON DOWNLOADED_SONG
FOR EACH ROW
EXECUTE FUNCTION decrement_total_download();

-- TRIGGER GROUP 5: Content Duration Management
-- 1. Update podcast duration when episode is added
CREATE OR REPLACE FUNCTION update_podcast_duration_add()
RETURNS TRIGGER AS $$
BEGIN
    -- Update the total duration of the podcast in KONTEN table
    UPDATE KONTEN SET durasi = durasi + NEW.durasi
    WHERE id = NEW.id_konten_podcast;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_podcast_duration_add
AFTER INSERT ON EPISODE
FOR EACH ROW
EXECUTE FUNCTION update_podcast_duration_add();

-- 2. Update podcast duration when episode is removed
CREATE OR REPLACE FUNCTION update_podcast_duration_remove()
RETURNS TRIGGER AS $$
BEGIN
    -- Update the total duration of the podcast in KONTEN table
    UPDATE KONTEN SET durasi = durasi - OLD.durasi
    WHERE id = OLD.id_konten_podcast;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_podcast_duration_remove
AFTER DELETE ON EPISODE
FOR EACH ROW
EXECUTE FUNCTION update_podcast_duration_remove();

-- 3. Update album attributes when song is added/removed
CREATE OR REPLACE FUNCTION update_album_attributes()
RETURNS TRIGGER AS $$
DECLARE
    total_duration INT;
    total_songs INT;
    album_id UUID;
BEGIN
    album_id := COALESCE(NEW.id_album, OLD.id_album);
    
    SELECT SUM(K.durasi), COUNT(*) INTO total_duration, total_songs
    FROM SONG S
    JOIN KONTEN K ON S.id_konten = K.id
    WHERE S.id_album = album_id;

    UPDATE ALBUM 
    SET total_durasi = COALESCE(total_duration, 0), 
        jumlah_lagu = COALESCE(total_songs, 0)
    WHERE id = album_id;

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_album_attributes
AFTER INSERT OR DELETE ON SONG
FOR EACH ROW
EXECUTE FUNCTION update_album_attributes();

-- ===================================
-- PERFORMANCE INDEXES
-- ===================================

-- Email-based indexes (most frequent lookups)
CREATE INDEX IF NOT EXISTS idx_akun_email ON AKUN(email);
CREATE INDEX IF NOT EXISTS idx_premium_email ON PREMIUM(email);
CREATE INDEX IF NOT EXISTS idx_nonpremium_email ON NONPREMIUM(email);
CREATE INDEX IF NOT EXISTS idx_label_email ON LABEL(email);

-- Content-based indexes
CREATE INDEX IF NOT EXISTS idx_konten_judul ON KONTEN(judul);
CREATE INDEX IF NOT EXISTS idx_konten_tanggal_rilis ON KONTEN(tanggal_rilis);
CREATE INDEX IF NOT EXISTS idx_song_id_konten ON SONG(id_konten);
CREATE INDEX IF NOT EXISTS idx_song_id_album ON SONG(id_album);
CREATE INDEX IF NOT EXISTS idx_song_id_artist ON SONG(id_artist);
CREATE INDEX IF NOT EXISTS idx_song_total_play ON SONG(total_play DESC);
CREATE INDEX IF NOT EXISTS idx_song_total_download ON SONG(total_download DESC);

-- Playlist indexes
CREATE INDEX IF NOT EXISTS idx_user_playlist_email ON USER_PLAYLIST(email_pembuat);
CREATE INDEX IF NOT EXISTS idx_user_playlist_id ON USER_PLAYLIST(id_user_playlist);
CREATE INDEX IF NOT EXISTS idx_playlist_song_playlist ON PLAYLIST_SONG(id_playlist);
CREATE INDEX IF NOT EXISTS idx_playlist_song_song ON PLAYLIST_SONG(id_song);
CREATE INDEX IF NOT EXISTS idx_playlist_song_composite ON PLAYLIST_SONG(id_playlist, id_song);

-- Album and Artist indexes
CREATE INDEX IF NOT EXISTS idx_album_label ON ALBUM(id_label);
CREATE INDEX IF NOT EXISTS idx_artist_email ON ARTIST(email_akun);
CREATE INDEX IF NOT EXISTS idx_songwriter_email ON SONGWRITER(email_akun);

-- Podcast indexes
CREATE INDEX IF NOT EXISTS idx_podcast_email ON PODCAST(email_podcaster);
CREATE INDEX IF NOT EXISTS idx_episode_podcast ON EPISODE(id_konten_podcast);

-- Genre indexes for search optimization
CREATE INDEX IF NOT EXISTS idx_genre_konten ON GENRE(id_konten);
CREATE INDEX IF NOT EXISTS idx_genre_genre ON GENRE(genre);

-- Play history indexes
CREATE INDEX IF NOT EXISTS idx_akun_play_song_email ON AKUN_PLAY_SONG(email_pemain);
CREATE INDEX IF NOT EXISTS idx_akun_play_song_waktu ON AKUN_PLAY_SONG(waktu DESC);
CREATE INDEX IF NOT EXISTS idx_akun_play_user_playlist_email ON AKUN_PLAY_USER_PLAYLIST(email_pemain);

-- Download indexes
CREATE INDEX IF NOT EXISTS idx_downloaded_song_email ON DOWNLOADED_SONG(email_downloader);
CREATE INDEX IF NOT EXISTS idx_downloaded_song_composite ON DOWNLOADED_SONG(email_downloader, id_song);

-- Transaction indexes
CREATE INDEX IF NOT EXISTS idx_transaction_email ON TRANSACTION(email);
CREATE INDEX IF NOT EXISTS idx_transaction_timestamp ON TRANSACTION(timestamp_dimulai, timestamp_berakhir);
CREATE INDEX IF NOT EXISTS idx_transaction_active ON TRANSACTION(email, timestamp_berakhir);

-- Chart indexes
CREATE INDEX IF NOT EXISTS idx_chart_tipe ON CHART(tipe);

-- Royalty indexes
CREATE INDEX IF NOT EXISTS idx_royalti_song ON ROYALTI(id_song);
CREATE INDEX IF NOT EXISTS idx_royalti_pemilik ON ROYALTI(id_pemilik_hak_cipta);

-- Copyright owner indexes
CREATE INDEX IF NOT EXISTS idx_pemilik_hak_cipta_rate ON PEMILIK_HAK_CIPTA(rate_royalti);

-- ===================================
-- COMPOSITE INDEXES FOR COMPLEX QUERIES
-- ===================================

-- For search functionality
CREATE INDEX IF NOT EXISTS idx_konten_search ON KONTEN USING gin(to_tsvector('english', judul));

-- For user playlist management
CREATE INDEX IF NOT EXISTS idx_user_playlist_composite ON USER_PLAYLIST(email_pembuat, id_user_playlist);

-- For subscription management
CREATE INDEX IF NOT EXISTS idx_paket_composite ON PAKET(jenis, harga);

-- ===================================
-- FULL-TEXT SEARCH INDEXES
-- ===================================

-- Enable full-text search on content titles
CREATE INDEX IF NOT EXISTS idx_konten_fulltext ON KONTEN USING gin(to_tsvector('english', judul));
CREATE INDEX IF NOT EXISTS idx_album_fulltext ON ALBUM USING gin(to_tsvector('english', judul));
CREATE INDEX IF NOT EXISTS idx_user_playlist_fulltext ON USER_PLAYLIST USING gin(to_tsvector('english', judul));

-- ===================================
-- PARTIAL INDEXES FOR SPECIFIC QUERIES
-- ===================================

-- Active premium users only
CREATE INDEX IF NOT EXISTS idx_active_premium ON TRANSACTION(email, timestamp_berakhir);

-- Recent content (last 30 days)
CREATE INDEX IF NOT EXISTS idx_recent_content ON KONTEN(tanggal_rilis);

-- Popular songs (high play count)
CREATE INDEX IF NOT EXISTS idx_popular_songs ON SONG(total_play) 
WHERE total_play > 100;

-- ===================================
-- VACUUM AND ANALYZE
-- ===================================

-- Optimize table statistics for better query planning
ANALYZE AKUN;
ANALYZE KONTEN;
ANALYZE SONG;
ANALYZE ALBUM;
ANALYZE USER_PLAYLIST;
ANALYZE PLAYLIST_SONG;
ANALYZE TRANSACTION;
ANALYZE PREMIUM;
ANALYZE NONPREMIUM;