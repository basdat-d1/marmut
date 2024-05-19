--1
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

    -- Insert the user email into PREMIUM table if not already a premium user
    IF NOT EXISTS (SELECT 1 FROM PREMIUM WHERE email = NEW.email) THEN
        INSERT INTO PREMIUM(email) VALUES (NEW.email);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_active_package
BEFORE INSERT ON TRANSACTION
FOR EACH ROW
EXECUTE FUNCTION check_active_package();

-- 2
CREATE OR REPLACE FUNCTION sync_playlist_songs()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert records into AKUN_PLAY_SONG for each song in the played playlist
    INSERT INTO AKUN_PLAY_SONG(email_pemain, id_song, waktu)
    SELECT NEW.email_pemain, PS.id_song, NEW.waktu FROM PLAYLIST_SONG PS
    WHERE PS.id_playlist = NEW.id_playlist;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_playlist_songs
AFTER INSERT ON AKUN_PLAY_USER_PLAYLIST
FOR EACH ROW
EXECUTE FUNCTION sync_playlist_songs();