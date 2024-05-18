-- 1
CREATE OR REPLACE FUNCTION update_playlist_attributes()
RETURNS TRIGGER AS $$
DECLARE
    total_duration INT;
    total_songs INT;
BEGIN
    SELECT SUM(K.durasi) INTO total_duration
    FROM PLAYLIST_SONG PS
    JOIN KONTEN K ON PS.id_song = K.id
    WHERE PS.id_playlist = COALESCE(NEW.id_playlist, OLD.id_playlist);

    SELECT COUNT(*) INTO total_songs
    FROM PLAYLIST_SONG
    WHERE id_playlist = COALESCE(NEW.id_playlist, OLD.id_playlist);

    UPDATE USER_PLAYLIST SET total_durasi = COALESCE(total_duration, 0), jumlah_lagu = COALESCE(total_songs, 0)
    WHERE id_playlist = COALESCE(NEW.id_playlist, OLD.id_playlist);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_playlist_attributes
AFTER INSERT OR DELETE ON PLAYLIST_SONG
FOR EACH ROW
EXECUTE FUNCTION update_playlist_attributes();

-- 2
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

-- 3
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