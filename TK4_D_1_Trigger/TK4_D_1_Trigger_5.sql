-- 1
-- Trigger to update duration when an episode is added
CREATE OR REPLACE FUNCTION update_podcast_duration_add()
RETURNS TRIGGER AS $$
BEGIN
    -- Update the total duration of the podcast in KONTEN table
    UPDATE KONTEN SET durasi = durasi + NEW.durasi
    WHERE id = (
        SELECT id_konten FROM PODCAST
        WHERE id_konten = NEW.id_konten_podcast
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_podcast_duration_add
AFTER INSERT ON EPISODE
FOR EACH ROW
EXECUTE FUNCTION update_podcast_duration_add();

-- Trigger to update duration when an episode is removed
CREATE OR REPLACE FUNCTION update_podcast_duration_remove()
RETURNS TRIGGER AS $$
BEGIN
    -- Update the total duration of the podcast in KONTEN table
    UPDATE KONTEN SET durasi = durasi - OLD.durasi
    WHERE id = (
        SELECT id_konten FROM PODCAST
        WHERE id_konten = OLD.id_konten_podcast
    );

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_podcast_duration_remove
AFTER DELETE ON EPISODE
FOR EACH ROW
EXECUTE FUNCTION update_podcast_duration_remove();

-- 2
-- Trigger to update album duration and song count when a song is added
CREATE OR REPLACE FUNCTION update_album_attributes()
RETURNS TRIGGER AS $$
DECLARE
    total_duration INT;
    total_songs INT;
BEGIN
    SELECT SUM(K.durasi) INTO total_duration
    FROM SONG S
    JOIN KONTEN K ON S.id_konten = K.id
    WHERE S.id_album = COALESCE(NEW.id_album, OLD.id_album);

    SELECT COUNT(*) INTO total_songs
    FROM SONG S
    WHERE id_album = COALESCE(NEW.id_album, OLD.id_album);

    UPDATE ALBUM SET total_durasi = COALESCE(total_duration, 0), jumlah_lagu = COALESCE(total_songs, 0)
    WHERE id = COALESCE(NEW.id_album, OLD.id_album);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_album_attributes
AFTER INSERT OR DELETE ON SONG
FOR EACH ROW
EXECUTE FUNCTION update_album_attributes();