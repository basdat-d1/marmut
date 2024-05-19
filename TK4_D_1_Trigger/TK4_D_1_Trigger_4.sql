-- 1
CREATE OR REPLACE FUNCTION update_total_play() RETURNS TRIGGER AS $$
BEGIN
    -- Update total_play in SONG table when a song is added to any playlist
    UPDATE SONG SET total_play = total_play + 1
    WHERE id_konten = NEW.id_song;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_total_play
AFTER INSERT ON PLAYLIST_SONG
FOR EACH ROW
EXECUTE FUNCTION update_total_play();

-- 2
-- Trigger to increment total_download when a song is downloaded
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

-- Trigger to decrement total_download when a download is removed
CREATE OR REPLACE FUNCTION decrement_total_download() RETURNS TRIGGER AS $$
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