-- ===================================
-- MARMUT DUMMY DATA
-- ===================================
-- This file contains all dummy data according to the specifications
-- Run this file after creating tables and triggers

-- ===================================
-- 1. AKUN - 45 records (minimal 30 verified)
-- ===================================

INSERT INTO AKUN (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) VALUES
-- Verified users (30)
('user1@marmut.com', 'pass123', 'Ahmad Rahman', 1, 'Jakarta', '1995-01-15', TRUE, 'Jakarta'),
('user2@marmut.com', 'pass123', 'Siti Nurhaliza', 0, 'Bandung', '1992-03-20', TRUE, 'Bandung'),
('user3@marmut.com', 'pass123', 'Budi Santoso', 1, 'Surabaya', '1988-07-10', TRUE, 'Surabaya'),
('user4@marmut.com', 'pass123', 'Dewi Sartika', 0, 'Yogyakarta', '1990-12-05', TRUE, 'Yogyakarta'),
('user5@marmut.com', 'pass123', 'Eko Prasetyo', 1, 'Medan', '1993-09-18', TRUE, 'Medan'),
('user6@marmut.com', 'pass123', 'Fitri Handayani', 0, 'Makassar', '1991-06-22', TRUE, 'Makassar'),
('user7@marmut.com', 'pass123', 'Gunawan Wijaya', 1, 'Palembang', '1987-11-30', TRUE, 'Palembang'),
('user8@marmut.com', 'pass123', 'Hani Permata', 0, 'Semarang', '1994-04-14', TRUE, 'Semarang'),
('user9@marmut.com', 'pass123', 'Indra Kusuma', 1, 'Denpasar', '1989-08-25', TRUE, 'Denpasar'),
('user10@marmut.com', 'pass123', 'Joko Widodo', 1, 'Solo', '1985-02-17', TRUE, 'Solo'),
('artist1@marmut.com', 'pass123', 'Raisa Andriana', 0, 'Jakarta', '1990-06-06', TRUE, 'Jakarta'),
('artist2@marmut.com', 'pass123', 'Afgan Syahreza', 1, 'Jakarta', '1989-05-27', TRUE, 'Jakarta'),
('artist3@marmut.com', 'pass123', 'Isyana Sarasvati', 0, 'Bandung', '1993-05-02', TRUE, 'Bandung'),
('artist4@marmut.com', 'pass123', 'Glenn Fredly', 1, 'Ambon', '1975-09-30', TRUE, 'Ambon'),
('artist5@marmut.com', 'pass123', 'Tulus Rusydi', 1, 'Bukittinggi', '1987-08-20', TRUE, 'Bukittinggi'),
('songwriter1@marmut.com', 'pass123', 'Yovie Widianto', 1, 'Bandung', '1970-07-29', TRUE, 'Bandung'),
('songwriter2@marmut.com', 'pass123', 'Melly Goeslaw', 0, 'Bandung', '1974-01-07', TRUE, 'Bandung'),
('songwriter3@marmut.com', 'pass123', 'Andi Rianto', 1, 'Jakarta', '1970-10-19', TRUE, 'Jakarta'),
('songwriter4@marmut.com', 'pass123', 'Bebi Romeo', 1, 'Jakarta', '1974-09-06', TRUE, 'Jakarta'),
('songwriter5@marmut.com', 'pass123', 'Yura Yunita', 0, 'Bandung', '1991-06-09', TRUE, 'Bandung'),
('podcaster1@marmut.com', 'pass123', 'Deddy Corbuzier', 1, 'Jakarta', '1976-12-28', TRUE, 'Jakarta'),
('podcaster2@marmut.com', 'pass123', 'Gita Savitri', 0, 'Jakarta', '1990-12-31', TRUE, 'Jakarta'),
('podcaster3@marmut.com', 'pass123', 'Raditya Dika', 1, 'Jakarta', '1984-12-28', TRUE, 'Jakarta'),
('podcaster4@marmut.com', 'pass123', 'Cameo Project', 1, 'Jakarta', '1985-03-15', TRUE, 'Jakarta'),
('podcaster5@marmut.com', 'pass123', 'Arief Muhammad', 1, 'Bandung', '1987-01-22', TRUE, 'Bandung'),
('user12@marmut.com', 'pass123', 'Lukman Hakim', 1, 'Pontianak', '1988-12-12', TRUE, 'Pontianak'),
('user13@marmut.com', 'pass123', 'Maya Indira', 0, 'Manado', '1995-05-05', TRUE, 'Manado'),
('user14@marmut.com', 'pass123', 'Nanda Pratama', 1, 'Pekanbaru', '1991-07-07', TRUE, 'Pekanbaru'),
('user15@marmut.com', 'pass123', 'Olivia Zalianty', 0, 'Banjarmasin', '1990-09-09', TRUE, 'Banjarmasin'),
-- Non-verified users (15)
('temp1@marmut.com', 'pass123', 'Temporary User 1', 1, 'Jakarta', '2000-01-01', FALSE, 'Jakarta'),
('temp2@marmut.com', 'pass123', 'Temporary User 2', 0, 'Bandung', '2000-02-02', FALSE, 'Bandung'),
('temp3@marmut.com', 'pass123', 'Temporary User 3', 1, 'Surabaya', '2000-03-03', FALSE, 'Surabaya'),
('temp4@marmut.com', 'pass123', 'Temporary User 4', 0, 'Medan', '2000-04-04', FALSE, 'Medan'),
('temp5@marmut.com', 'pass123', 'Temporary User 5', 1, 'Makassar', '2000-05-05', FALSE, 'Makassar'),
('temp6@marmut.com', 'pass123', 'Temporary User 6', 0, 'Palembang', '2000-06-06', FALSE, 'Palembang'),
('temp7@marmut.com', 'pass123', 'Temporary User 7', 1, 'Semarang', '2000-07-07', FALSE, 'Semarang'),
('temp8@marmut.com', 'pass123', 'Temporary User 8', 0, 'Denpasar', '2000-08-08', FALSE, 'Denpasar'),
('temp9@marmut.com', 'pass123', 'Temporary User 9', 1, 'Solo', '2000-09-09', FALSE, 'Solo'),
('temp10@marmut.com', 'pass123', 'Temporary User 10', 0, 'Yogyakarta', '2000-10-10', FALSE, 'Yogyakarta'),
('temp11@marmut.com', 'pass123', 'Temporary User 11', 1, 'Malang', '2000-11-11', FALSE, 'Malang'),
('temp12@marmut.com', 'pass123', 'Temporary User 12', 0, 'Bogor', '2000-12-12', FALSE, 'Bogor'),
('temp13@marmut.com', 'pass123', 'Temporary User 13', 1, 'Depok', '2001-01-01', FALSE, 'Depok'),
('temp14@marmut.com', 'pass123', 'Temporary User 14', 0, 'Tangerang', '2001-02-02', FALSE, 'Tangerang'),
('temp15@marmut.com', 'pass123', 'Temporary User 15', 1, 'Bekasi', '2001-03-03', FALSE, 'Bekasi');

-- ===================================
-- 2. PAKET - 4 packages
-- ===================================

INSERT INTO PAKET (jenis, harga) VALUES
('1 Bulan', 25000),
('3 Bulan', 65000),
('6 Bulan', 120000),
('1 Tahun', 200000);

-- ===================================
-- 3. TRANSACTION - 5 records
-- ===================================

INSERT INTO TRANSACTION (jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal) VALUES
('1 Bulan', 'user1@marmut.com', '2024-01-01 10:00:00', '2025-02-01 10:00:00', 'Credit Card', 25000),
('3 Bulan', 'user2@marmut.com', '2024-01-15 14:30:00', '2025-04-15 14:30:00', 'Bank Transfer', 65000),
('6 Bulan', 'artist1@marmut.com', '2024-02-01 09:15:00', '2024-08-01 09:15:00', 'E-Wallet', 120000),
('1 Tahun', 'artist2@marmut.com', '2024-01-10 16:45:00', '2025-01-10 16:45:00', 'Credit Card', 200000),
('1 Bulan', 'user3@marmut.com', '2024-02-15 11:20:00', '2024-03-15 11:20:00', 'Bank Transfer', 25000); 

-- ================================== 
-- 4. PREMIUM - 5 record 
-- ===================================

INSERT INTO PREMIUM (email) VALUES
('user1@marmut.com'),
('user2@marmut.com'),
('artist1@marmut.com'),
('artist2@marmut.com'),
('user3@marmut.com');

-- ===================================
-- 5. NONPREMIUM - 25 records
-- ===================================

INSERT INTO NONPREMIUM (email) VALUES
('user4@marmut.com'), ('user5@marmut.com'), ('user6@marmut.com'), ('user7@marmut.com'), ('user8@marmut.com'),
('user9@marmut.com'), ('user10@marmut.com'), ('artist3@marmut.com'), ('artist4@marmut.com'), ('artist5@marmut.com'),
('songwriter1@marmut.com'), ('songwriter2@marmut.com'), ('songwriter3@marmut.com'), ('songwriter4@marmut.com'), ('songwriter5@marmut.com'),
('podcaster1@marmut.com'), ('podcaster2@marmut.com'), ('podcaster3@marmut.com'), ('podcaster4@marmut.com'), ('podcaster5@marmut.com'),
('user11@marmut.com'), ('user12@marmut.com'), ('user13@marmut.com'), ('user14@marmut.com'), ('user15@marmut.com');

-- ===================================
-- PEMILIK_HAK_CIPTA - 25 records
-- ===================================

INSERT INTO PEMILIK_HAK_CIPTA (rate_royalti) VALUES
(5), (8), (12), (18), (22), (25), (28), (32), (35), (38),
(40), (42), (45), (48), (50), (52), (55), (58), (60), (62),
(65), (68), (70), (72), (75);

-- ===================================
-- LABEL - 5 records
-- ===================================

INSERT INTO LABEL (nama, email, password, kontak, id_pemilik_hak_cipta) VALUES
('Universal Music Indonesia', 'label1@marmut.com', 'pass123', '+62211234567', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 75 LIMIT 1)),
('Sony Music Entertainment', 'label2@marmut.com', 'pass123', '+62211234568', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 70 LIMIT 1)),
('Warner Music Indonesia', 'label3@marmut.com', 'pass123', '+62211234569', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 65 LIMIT 1)),
('Aquarius Musikindo', 'label4@marmut.com', 'pass123', '+62211234570', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 60 LIMIT 1)),
('Trinity Optima Production', 'label5@marmut.com', 'pass123', '+62211234571', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 55 LIMIT 1));

-- ===================================
-- PODCASTER - 10 records
-- ===================================

INSERT INTO PODCASTER (email) VALUES
('podcaster1@marmut.com'), ('podcaster2@marmut.com'), ('podcaster3@marmut.com'), 
('podcaster4@marmut.com'), ('podcaster5@marmut.com'), ('user4@marmut.com'), 
('user5@marmut.com'), ('user6@marmut.com'), ('user7@marmut.com'), ('user8@marmut.com');

-- ===================================
-- ARTIST - 10 records
-- ===================================

INSERT INTO ARTIST (email_akun, id_pemilik_hak_cipta) VALUES
('artist1@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 50 LIMIT 1)),
('artist2@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 48 LIMIT 1)),
('artist3@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 45 LIMIT 1)),
('artist4@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 42 LIMIT 1)),
('artist5@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 40 LIMIT 1)),
('user9@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 38 LIMIT 1)),
('user10@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 35 LIMIT 1)),
('user11@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 32 LIMIT 1)),
('user12@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 28 LIMIT 1)),
('user13@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 25 LIMIT 1));

-- ===================================
-- SONGWRITER - 10 records
-- ===================================

INSERT INTO SONGWRITER (email_akun, id_pemilik_hak_cipta) VALUES
('songwriter1@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 22 LIMIT 1)),
('songwriter2@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 18 LIMIT 1)),
('songwriter3@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 12 LIMIT 1)),
('songwriter4@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 8 LIMIT 1)),
('songwriter5@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 5 LIMIT 1)),
('artist1@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 52 LIMIT 1)),
('artist2@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 58 LIMIT 1)),
('artist3@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 62 LIMIT 1)),
('artist4@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 68 LIMIT 1)),
('artist5@marmut.com', (SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 72 LIMIT 1));

-- ===================================
-- KONTEN - 55 records (45 songs + 10 podcasts)
-- ===================================

INSERT INTO KONTEN (judul, tanggal_rilis, tahun, durasi) VALUES
-- Songs (45 records)
('Kamu & Kenangan', '2020-01-15', 2020, 4),
('Cinta Luar Biasa', '2019-03-20', 2019, 3),
('Jangan Menyerah', '2021-05-10', 2021, 5),
('Bahagia Itu Sederhana', '2020-07-25', 2020, 4),
('Mimpi Yang Sempurna', '2018-12-05', 2018, 6),
('Senja Di Jakarta', '2021-02-14', 2021, 4),
('Rindu Setengah Mati', '2019-08-30', 2019, 5),
('Cinta Sejati', '2020-11-12', 2020, 3),
('Masa Lalu', '2018-09-18', 2018, 4),
('Harapan Baru', '2021-06-22', 2021, 5),
('Pelangi Setelah Hujan', '2020-04-08', 2020, 4),
('Bintang Di Langit', '2019-10-15', 2019, 3),
('Cinta Pertama', '2021-01-20', 2021, 5),
('Kenangan Terindah', '2020-08-14', 2020, 4),
('Satu Hati', '2018-11-25', 2018, 6),
('Impian Tinggi', '2021-03-30', 2021, 4),
('Cahaya Hati', '2019-12-10', 2019, 5),
('Bersama Selamanya', '2020-09-05', 2020, 3),
('Melodi Cinta', '2018-07-18', 2018, 4),
('Harmoni Jiwa', '2021-04-25', 2021, 5),
('Syukur Alhamdulillah', '2020-06-12', 2020, 4),
('Doa Untuk Ibu', '2019-05-28', 2019, 3),
('Semangat Pagi', '2021-07-15', 2021, 5),
('Malam Yang Indah', '2020-10-30', 2020, 4),
('Persahabatan Sejati', '2018-08-22', 2018, 6),
('Kebahagiaan Sederhana', '2021-09-18', 2021, 4),
('Cinta Tanah Air', '2019-02-14', 2019, 5),
('Generasi Emas', '2020-12-25', 2020, 3),
('Anak Negeri', '2018-06-10', 2018, 4),
('Bangga Indonesia', '2021-08-17', 2021, 5),
('Lagu Untuk Mama', '2020-05-20', 2020, 4),
('Papa Tercinta', '2019-06-15', 2019, 3),
('Keluarga Bahagia', '2021-10-12', 2021, 5),
('Rumah Impian', '2020-03-08', 2020, 4),
('Masa Depan Cerah', '2018-10-05', 2018, 6),
('Jejak Langkah', '2021-11-28', 2021, 4),
('Perjalanan Hidup', '2019-09-22', 2019, 5),
('Takdir Cinta', '2020-07-14', 2020, 3),
('Kisah Kita', '2018-12-30', 2018, 4),
('Cerita Hati', '2021-05-25', 2021, 5),
('Lagu Rindu', '2020-02-18', 2020, 4),
('Nostalgia Masa Lalu', '2019-11-08', 2019, 3),
('Memori Indah', '2021-12-15', 2021, 5),
('Waktu Berharga', '2020-01-28', 2020, 4),
('Detik Bersejarah', '2018-05-12', 2018, 6),
-- Podcasts (10 records)
('Ngobrol Santai', '2021-01-01', 2021, 45),
('Cerita Inspiratif', '2021-02-01', 2021, 60),
('Diskusi Hangat', '2021-03-01', 2021, 30),
('Motivasi Pagi', '2021-04-01', 2021, 25),
('Podcast Edukasi', '2021-05-01', 2021, 50),
('Sharing Session', '2021-06-01', 2021, 40),
('Talk Show Malam', '2021-07-01', 2021, 75),
('Obrolan Seru', '2021-08-01', 2021, 35),
('Diskusi Topik Hangat', '2021-09-01', 2021, 55),
('Cerita Sukses', '2021-10-01', 2021, 65);

-- ===================================
-- GENRE - 60 records (linking content to genres)
-- ===================================

INSERT INTO GENRE (id_konten, genre) VALUES
((SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Jangan Menyerah' LIMIT 1), 'Rock'),
((SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1), 'Ballad'),
((SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1), 'Ballad'),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Masa Lalu' LIMIT 1), 'Alternative'),
((SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Pelangi Setelah Hujan' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Bintang Di Langit' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Pertama' LIMIT 1), 'Ballad'),
((SELECT id FROM KONTEN WHERE judul = 'Kenangan Terindah' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Satu Hati' LIMIT 1), 'R&B'),
((SELECT id FROM KONTEN WHERE judul = 'Impian Tinggi' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Cahaya Hati' LIMIT 1), 'Gospel'),
((SELECT id FROM KONTEN WHERE judul = 'Bersama Selamanya' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Melodi Cinta' LIMIT 1), 'Jazz'),
((SELECT id FROM KONTEN WHERE judul = 'Harmoni Jiwa' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Syukur Alhamdulillah' LIMIT 1), 'Nasyid'),
((SELECT id FROM KONTEN WHERE judul = 'Doa Untuk Ibu' LIMIT 1), 'Nasyid'),
((SELECT id FROM KONTEN WHERE judul = 'Semangat Pagi' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Malam Yang Indah' LIMIT 1), 'Ballad'),
((SELECT id FROM KONTEN WHERE judul = 'Persahabatan Sejati' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Kebahagiaan Sederhana' LIMIT 1), 'Acoustic'),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Tanah Air' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Generasi Emas' LIMIT 1), 'Rock'),
((SELECT id FROM KONTEN WHERE judul = 'Anak Negeri' LIMIT 1), 'Folk'),
((SELECT id FROM KONTEN WHERE judul = 'Bangga Indonesia' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Lagu Untuk Mama' LIMIT 1), 'Ballad'),
((SELECT id FROM KONTEN WHERE judul = 'Papa Tercinta' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Keluarga Bahagia' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Rumah Impian' LIMIT 1), 'Country'),
((SELECT id FROM KONTEN WHERE judul = 'Masa Depan Cerah' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Jejak Langkah' LIMIT 1), 'Alternative'),
((SELECT id FROM KONTEN WHERE judul = 'Perjalanan Hidup' LIMIT 1), 'Folk'),
((SELECT id FROM KONTEN WHERE judul = 'Takdir Cinta' LIMIT 1), 'Ballad'),
((SELECT id FROM KONTEN WHERE judul = 'Kisah Kita' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Cerita Hati' LIMIT 1), 'R&B'),
((SELECT id FROM KONTEN WHERE judul = 'Lagu Rindu' LIMIT 1), 'Ballad'),
((SELECT id FROM KONTEN WHERE judul = 'Nostalgia Masa Lalu' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Memori Indah' LIMIT 1), 'Jazz'),
((SELECT id FROM KONTEN WHERE judul = 'Waktu Berharga' LIMIT 1), 'Pop'),
((SELECT id FROM KONTEN WHERE judul = 'Detik Bersejarah' LIMIT 1), 'Rock'),
-- Podcast genres
((SELECT id FROM KONTEN WHERE judul = 'Ngobrol Santai' LIMIT 1), 'Talk Show'),
((SELECT id FROM KONTEN WHERE judul = 'Cerita Inspiratif' LIMIT 1), 'Motivation'),
((SELECT id FROM KONTEN WHERE judul = 'Diskusi Hangat' LIMIT 1), 'Discussion'),
((SELECT id FROM KONTEN WHERE judul = 'Motivasi Pagi' LIMIT 1), 'Motivation'),
((SELECT id FROM KONTEN WHERE judul = 'Podcast Edukasi' LIMIT 1), 'Education'),
((SELECT id FROM KONTEN WHERE judul = 'Sharing Session' LIMIT 1), 'Talk Show'),
((SELECT id FROM KONTEN WHERE judul = 'Talk Show Malam' LIMIT 1), 'Talk Show'),
((SELECT id FROM KONTEN WHERE judul = 'Obrolan Seru' LIMIT 1), 'Entertainment'),
((SELECT id FROM KONTEN WHERE judul = 'Diskusi Topik Hangat' LIMIT 1), 'Discussion'),
((SELECT id FROM KONTEN WHERE judul = 'Cerita Sukses' LIMIT 1), 'Motivation'),
-- Additional genres for variety (10 more)
((SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1), 'Indonesian'),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1), 'Love Song'),
((SELECT id FROM KONTEN WHERE judul = 'Jangan Menyerah' LIMIT 1), 'Motivational'),
((SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1), 'Feel Good'),
((SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1), 'Dream'),
((SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1), 'Urban'),
((SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1), 'Romantic'),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1), 'Love Song'),
((SELECT id FROM KONTEN WHERE judul = 'Masa Lalu' LIMIT 1), 'Nostalgia'),
((SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1), 'Hope');

-- ===================================
-- ALBUM - 5 records
-- ===================================

INSERT INTO ALBUM (judul, jumlah_lagu, id_label, total_durasi) VALUES
('Album Cinta', 10, (SELECT id FROM LABEL WHERE nama = 'Universal Music Indonesia' LIMIT 1), 40),
('Album Bahagia', 10, (SELECT id FROM LABEL WHERE nama = 'Sony Music Entertainment' LIMIT 1), 42),
('Album Kenangan', 10, (SELECT id FROM LABEL WHERE nama = 'Warner Music Indonesia' LIMIT 1), 45),
('Album Inspirasi', 10, (SELECT id FROM LABEL WHERE nama = 'Aquarius Musikindo' LIMIT 1), 47),
('Album Nostalgia', 5, (SELECT id FROM LABEL WHERE nama = 'Trinity Optima Production' LIMIT 1), 22);

-- ===================================
-- PODCAST - 5 records
-- ===================================

INSERT INTO PODCAST (id_konten, email_podcaster) VALUES
((SELECT id FROM KONTEN WHERE judul = 'Ngobrol Santai' LIMIT 1), 'podcaster1@marmut.com'),
((SELECT id FROM KONTEN WHERE judul = 'Cerita Inspiratif' LIMIT 1), 'podcaster2@marmut.com'),
((SELECT id FROM KONTEN WHERE judul = 'Diskusi Hangat' LIMIT 1), 'podcaster3@marmut.com'),
((SELECT id FROM KONTEN WHERE judul = 'Motivasi Pagi' LIMIT 1), 'podcaster4@marmut.com'),
((SELECT id FROM KONTEN WHERE judul = 'Podcast Edukasi' LIMIT 1), 'podcaster5@marmut.com');

-- ===================================
-- EPISODE - 10 records
-- ===================================

INSERT INTO EPISODE (id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis) VALUES
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster1@marmut.com' LIMIT 1), 'Episode 1: Perkenalan', 'Episode pertama podcast ngobrol santai', 30, '2021-01-05'),
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster1@marmut.com' LIMIT 1), 'Episode 2: Hobi Favorit', 'Membahas berbagai hobi menarik', 35, '2021-01-12'),
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster2@marmut.com' LIMIT 1), 'Episode 1: Kisah Sukses', 'Cerita inspiratif dari pengusaha muda', 45, '2021-02-05'),
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster2@marmut.com' LIMIT 1), 'Episode 2: Motivasi Hidup', 'Tips motivasi untuk kehidupan sehari-hari', 40, '2021-02-12'),
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster3@marmut.com' LIMIT 1), 'Episode 1: Isu Terkini', 'Diskusi tentang isu-isu terkini', 25, '2021-03-05'),
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster3@marmut.com' LIMIT 1), 'Episode 2: Teknologi Modern', 'Membahas perkembangan teknologi', 30, '2021-03-12'),
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster4@marmut.com' LIMIT 1), 'Episode 1: Semangat Pagi', 'Motivasi untuk memulai hari', 20, '2021-04-05'),
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster4@marmut.com' LIMIT 1), 'Episode 2: Tips Produktif', 'Cara meningkatkan produktivitas', 25, '2021-04-12'),
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster5@marmut.com' LIMIT 1), 'Episode 1: Belajar Efektif', 'Metode belajar yang efektif', 35, '2021-05-05'),
((SELECT id_konten FROM PODCAST WHERE email_podcaster = 'podcaster5@marmut.com' LIMIT 1), 'Episode 2: Skill Digital', 'Pentingnya skill digital di era modern', 40, '2021-05-12');

-- ===================================
-- SONG - 45 records
-- ===================================

INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download) VALUES
-- Album Cinta (10 songs)
((SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist1@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 1500, 120),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist1@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 1200, 95),
((SELECT id FROM KONTEN WHERE judul = 'Jangan Menyerah' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist2@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 980, 78),
((SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist2@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 2100, 165),
((SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist3@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 1800, 140),
((SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist3@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 1650, 130),
((SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist4@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 2200, 175),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist4@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 1900, 150),
((SELECT id FROM KONTEN WHERE judul = 'Masa Lalu' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist5@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 1100, 88),
((SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist5@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Cinta' LIMIT 1), 1750, 138),

-- Album Bahagia (10 songs)
((SELECT id FROM KONTEN WHERE judul = 'Pelangi Setelah Hujan' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist1@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 1400, 112),
((SELECT id FROM KONTEN WHERE judul = 'Bintang Di Langit' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist1@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 1600, 128),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Pertama' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist2@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 2000, 160),
((SELECT id FROM KONTEN WHERE judul = 'Kenangan Terindah' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist2@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 1850, 148),
((SELECT id FROM KONTEN WHERE judul = 'Satu Hati' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist3@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 1300, 104),
((SELECT id FROM KONTEN WHERE judul = 'Impian Tinggi' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist3@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 1550, 124),
((SELECT id FROM KONTEN WHERE judul = 'Cahaya Hati' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist4@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 1700, 136),
((SELECT id FROM KONTEN WHERE judul = 'Bersama Selamanya' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist4@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 1950, 156),
((SELECT id FROM KONTEN WHERE judul = 'Melodi Cinta' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist5@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 1450, 116),
((SELECT id FROM KONTEN WHERE judul = 'Harmoni Jiwa' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist5@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Bahagia' LIMIT 1), 1800, 144),

-- Album Kenangan (10 songs)
((SELECT id FROM KONTEN WHERE judul = 'Syukur Alhamdulillah' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user9@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 2500, 200),
((SELECT id FROM KONTEN WHERE judul = 'Doa Untuk Ibu' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user9@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 2300, 184),
((SELECT id FROM KONTEN WHERE judul = 'Semangat Pagi' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user10@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 1600, 128),
((SELECT id FROM KONTEN WHERE judul = 'Malam Yang Indah' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user10@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 1750, 140),
((SELECT id FROM KONTEN WHERE judul = 'Persahabatan Sejati' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user11@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 1400, 112),
((SELECT id FROM KONTEN WHERE judul = 'Kebahagiaan Sederhana' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user11@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 1850, 148),
((SELECT id FROM KONTEN WHERE judul = 'Cinta Tanah Air' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user12@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 3000, 240),
((SELECT id FROM KONTEN WHERE judul = 'Generasi Emas' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user12@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 2200, 176),
((SELECT id FROM KONTEN WHERE judul = 'Anak Negeri' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user13@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 1900, 152),
((SELECT id FROM KONTEN WHERE judul = 'Bangga Indonesia' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'user13@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Kenangan' LIMIT 1), 2800, 224),

-- Album Inspirasi (10 songs)
((SELECT id FROM KONTEN WHERE judul = 'Lagu Untuk Mama' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist1@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 2100, 168),
((SELECT id FROM KONTEN WHERE judul = 'Papa Tercinta' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist2@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 1950, 156),
((SELECT id FROM KONTEN WHERE judul = 'Keluarga Bahagia' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist3@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 1800, 144),
((SELECT id FROM KONTEN WHERE judul = 'Rumah Impian' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist4@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 1650, 132),
((SELECT id FROM KONTEN WHERE judul = 'Masa Depan Cerah' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist5@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 2300, 184),
((SELECT id FROM KONTEN WHERE judul = 'Jejak Langkah' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist1@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 1500, 120),
((SELECT id FROM KONTEN WHERE judul = 'Perjalanan Hidup' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist2@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 1750, 140),
((SELECT id FROM KONTEN WHERE judul = 'Takdir Cinta' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist3@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 2000, 160),
((SELECT id FROM KONTEN WHERE judul = 'Kisah Kita' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist4@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 1850, 148),
((SELECT id FROM KONTEN WHERE judul = 'Cerita Hati' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist5@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Inspirasi' LIMIT 1), 1700, 136),

-- Album Nostalgia (5 songs)
((SELECT id FROM KONTEN WHERE judul = 'Lagu Rindu' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist1@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Nostalgia' LIMIT 1), 2400, 192),
((SELECT id FROM KONTEN WHERE judul = 'Nostalgia Masa Lalu' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist2@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Nostalgia' LIMIT 1), 2000, 160),
((SELECT id FROM KONTEN WHERE judul = 'Memori Indah' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist3@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Nostalgia' LIMIT 1), 1600, 128),
((SELECT id FROM KONTEN WHERE judul = 'Waktu Berharga' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist4@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Nostalgia' LIMIT 1), 1900, 152),
((SELECT id FROM KONTEN WHERE judul = 'Detik Bersejarah' LIMIT 1), (SELECT id FROM ARTIST WHERE email_akun = 'artist5@marmut.com' LIMIT 1), (SELECT id FROM ALBUM WHERE judul = 'Album Nostalgia' LIMIT 1), 2200, 176);

-- ===================================
-- SONGWRITER_WRITE_SONG - 60 records
-- ===================================

INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) VALUES
-- Songwriter 1 writes for multiple songs (12 songs)
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Jangan Menyerah' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Masa Lalu' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Pelangi Setelah Hujan' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter1@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bintang Di Langit' LIMIT 1) LIMIT 1)),

-- Songwriter 2 writes for 12 songs
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Pertama' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kenangan Terindah' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Satu Hati' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Impian Tinggi' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cahaya Hati' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bersama Selamanya' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Melodi Cinta' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harmoni Jiwa' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Syukur Alhamdulillah' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Doa Untuk Ibu' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Semangat Pagi' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter2@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Malam Yang Indah' LIMIT 1) LIMIT 1)),

-- Songwriter 3 writes for 12 songs
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Persahabatan Sejati' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kebahagiaan Sederhana' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Tanah Air' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Generasi Emas' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Anak Negeri' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bangga Indonesia' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Lagu Untuk Mama' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Papa Tercinta' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Keluarga Bahagia' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rumah Impian' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter3@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Masa Depan Cerah' LIMIT 1) LIMIT 1)),

-- Songwriter 4 writes for 12 songs
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Jejak Langkah' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Perjalanan Hidup' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Takdir Cinta' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kisah Kita' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cerita Hati' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Lagu Rindu' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Nostalgia Masa Lalu' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Memori Indah' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Waktu Berharga' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Detik Bersejarah' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter4@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1) LIMIT 1)),

-- Songwriter 5 writes for 12 songs
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Jangan Menyerah' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Masa Lalu' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Pelangi Setelah Hujan' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bintang Di Langit' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Pertama' LIMIT 1) LIMIT 1)),
((SELECT id FROM SONGWRITER WHERE email_akun = 'songwriter5@marmut.com' LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kenangan Terindah' LIMIT 1) LIMIT 1));

-- ===================================
-- PLAYLIST - 20 records (Base playlist table with UUID)
-- ===================================

INSERT INTO PLAYLIST (id) VALUES
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid()),
(gen_random_uuid());

-- ===================================
-- PLAYLIST_SONG - 30 records
-- ===================================

-- Playlist 1 - My Favorite Songs (15 songs)
INSERT INTO PLAYLIST_SONG (id_playlist, id_song) VALUES
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Pelangi Setelah Hujan' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bintang Di Langit' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Pertama' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kenangan Terindah' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Impian Tinggi' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cahaya Hati' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bersama Selamanya' LIMIT 1) LIMIT 1)),

-- Playlist 2 - Chill Vibes (15 songs)
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Melodi Cinta' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harmoni Jiwa' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Syukur Alhamdulillah' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Doa Untuk Ibu' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Malam Yang Indah' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Persahabatan Sejati' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kebahagiaan Sederhana' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Lagu Untuk Mama' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Papa Tercinta' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Keluarga Bahagia' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rumah Impian' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Perjalanan Hidup' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Takdir Cinta' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Lagu Rindu' LIMIT 1) LIMIT 1)),
((SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Memori Indah' LIMIT 1) LIMIT 1));

-- ===================================
-- CHART - 4 records
-- ===================================

INSERT INTO CHART (tipe, id_playlist) VALUES
('Daily Top 50', (SELECT id FROM PLAYLIST LIMIT 1)),
('Weekly Top 50', (SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1)),
('Monthly Top 50', (SELECT id FROM PLAYLIST OFFSET 2 LIMIT 1)),
('Yearly Top 50', (SELECT id FROM PLAYLIST OFFSET 3 LIMIT 1));

-- ===================================
-- AKUN_PLAY_SONG - 51 records
-- ===================================

INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu) VALUES
('user1@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1) LIMIT 1), '2024-01-01 10:00:00'),
('user1@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1) LIMIT 1), '2024-01-01 10:04:00'),
('user1@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1) LIMIT 1), '2024-01-01 10:08:00'),
('user2@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1) LIMIT 1), '2024-01-01 11:00:00'),
('user2@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1) LIMIT 1), '2024-01-01 11:06:00'),
('user2@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1) LIMIT 1), '2024-01-01 11:10:00'),
('user3@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1) LIMIT 1), '2024-01-01 12:00:00'),
('user3@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1) LIMIT 1), '2024-01-01 12:03:00'),
('user3@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Pelangi Setelah Hujan' LIMIT 1) LIMIT 1), '2024-01-01 12:08:00'),
('user4@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bintang Di Langit' LIMIT 1) LIMIT 1), '2024-01-01 13:00:00'),
('user4@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Pertama' LIMIT 1) LIMIT 1), '2024-01-01 13:03:00'),
('user4@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kenangan Terindah' LIMIT 1) LIMIT 1), '2024-01-01 13:08:00'),
('user5@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Impian Tinggi' LIMIT 1) LIMIT 1), '2024-01-01 14:00:00'),
('user5@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cahaya Hati' LIMIT 1) LIMIT 1), '2024-01-01 14:04:00'),
('user5@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bersama Selamanya' LIMIT 1) LIMIT 1), '2024-01-01 14:09:00'),
('user6@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Melodi Cinta' LIMIT 1) LIMIT 1), '2024-01-01 15:00:00'),
('user6@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harmoni Jiwa' LIMIT 1) LIMIT 1), '2024-01-01 15:04:00'),
('user6@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Syukur Alhamdulillah' LIMIT 1) LIMIT 1), '2024-01-01 15:09:00'),
('user7@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Doa Untuk Ibu' LIMIT 1) LIMIT 1), '2024-01-01 16:00:00'),
('user7@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Malam Yang Indah' LIMIT 1) LIMIT 1), '2024-01-01 16:03:00'),
('user7@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Persahabatan Sejati' LIMIT 1) LIMIT 1), '2024-01-01 16:07:00'),
('user8@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kebahagiaan Sederhana' LIMIT 1) LIMIT 1), '2024-01-01 17:00:00'),
('user8@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Tanah Air' LIMIT 1) LIMIT 1), '2024-01-01 17:04:00'),
('user8@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Generasi Emas' LIMIT 1) LIMIT 1), '2024-01-01 17:09:00'),
('user9@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Anak Negeri' LIMIT 1) LIMIT 1), '2024-01-01 18:00:00'),
('user9@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bangga Indonesia' LIMIT 1) LIMIT 1), '2024-01-01 18:04:00'),
('user9@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Lagu Untuk Mama' LIMIT 1) LIMIT 1), '2024-01-01 18:09:00'),
('user10@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Papa Tercinta' LIMIT 1) LIMIT 1), '2024-01-01 19:00:00'),
('user10@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Keluarga Bahagia' LIMIT 1) LIMIT 1), '2024-01-01 19:03:00'),
('user10@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rumah Impian' LIMIT 1) LIMIT 1), '2024-01-01 19:08:00'),
('artist1@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Masa Depan Cerah' LIMIT 1) LIMIT 1), '2024-01-01 20:00:00'),
('artist1@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Jejak Langkah' LIMIT 1) LIMIT 1), '2024-01-01 20:06:00'),
('artist1@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Perjalanan Hidup' LIMIT 1) LIMIT 1), '2024-01-01 20:10:00'),
('artist2@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Takdir Cinta' LIMIT 1) LIMIT 1), '2024-01-01 21:00:00'),
('artist2@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kisah Kita' LIMIT 1) LIMIT 1), '2024-01-01 21:03:00'),
('artist2@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cerita Hati' LIMIT 1) LIMIT 1), '2024-01-01 21:08:00'),
('artist3@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Lagu Rindu' LIMIT 1) LIMIT 1), '2024-01-01 22:00:00'),
('artist3@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Nostalgia Masa Lalu' LIMIT 1) LIMIT 1), '2024-01-01 22:03:00'),
('artist3@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Memori Indah' LIMIT 1) LIMIT 1), '2024-01-01 22:08:00'),
('artist4@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Waktu Berharga' LIMIT 1) LIMIT 1), '2024-01-01 23:00:00'),
('artist4@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Detik Bersejarah' LIMIT 1) LIMIT 1), '2024-01-01 23:06:00'),
('artist4@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1) LIMIT 1), '2024-01-01 23:12:00'),
('artist5@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1) LIMIT 1), '2024-01-02 00:00:00'),
('artist5@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1) LIMIT 1), '2024-01-02 00:03:00'),
('artist5@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1) LIMIT 1), '2024-01-02 00:07:00'),
('user11@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1) LIMIT 1), '2024-01-02 01:00:00'),
('user11@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1) LIMIT 1), '2024-01-02 01:04:00'),
('user12@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1) LIMIT 1), '2024-01-02 02:00:00'),
('user12@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1) LIMIT 1), '2024-01-02 02:03:00'),
('user13@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Pelangi Setelah Hujan' LIMIT 1) LIMIT 1), '2024-01-02 03:00:00'),
('user13@marmut.com', (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bintang Di Langit' LIMIT 1) LIMIT 1), '2024-01-02 03:04:00');

-- ===================================
-- USER_PLAYLIST - 20 records  
-- ===================================

INSERT INTO USER_PLAYLIST (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi) VALUES
('user1@marmut.com', gen_random_uuid(), 'My Favorite Songs', 'Koleksi lagu favorit saya', 15, '2024-01-01', (SELECT id FROM PLAYLIST LIMIT 1), 45),
('user2@marmut.com', gen_random_uuid(), 'Chill Vibes', 'Lagu-lagu santai untuk bersantai', 15, '2024-01-02', (SELECT id FROM PLAYLIST OFFSET 1 LIMIT 1), 38),
('user3@marmut.com', gen_random_uuid(), 'Workout Playlist', 'Lagu energik untuk olahraga', 15, '2024-01-03', (SELECT id FROM PLAYLIST OFFSET 2 LIMIT 1), 52),
('user4@marmut.com', gen_random_uuid(), 'Love Songs', 'Kumpulan lagu cinta terbaik', 15, '2024-01-04', (SELECT id FROM PLAYLIST OFFSET 3 LIMIT 1), 41),
('user5@marmut.com', gen_random_uuid(), 'Indonesian Hits', 'Lagu-lagu Indonesia terpopuler', 15, '2024-01-05', (SELECT id FROM PLAYLIST OFFSET 4 LIMIT 1), 47),
('user6@marmut.com', gen_random_uuid(), 'Morning Motivation', 'Lagu motivasi untuk pagi hari', 15, '2024-01-06', (SELECT id FROM PLAYLIST OFFSET 5 LIMIT 1), 35),
('user7@marmut.com', gen_random_uuid(), 'Night Playlist', 'Lagu untuk malam yang tenang', 15, '2024-01-07', (SELECT id FROM PLAYLIST OFFSET 6 LIMIT 1), 43),
('user8@marmut.com', gen_random_uuid(), 'Road Trip Songs', 'Lagu untuk perjalanan jauh', 15, '2024-01-08', (SELECT id FROM PLAYLIST OFFSET 7 LIMIT 1), 56),
('user9@marmut.com', gen_random_uuid(), 'Acoustic Collection', 'Koleksi lagu akustik', 15, '2024-01-09', (SELECT id FROM PLAYLIST OFFSET 8 LIMIT 1), 39),
('user10@marmut.com', gen_random_uuid(), 'Party Mix', 'Lagu untuk pesta', 15, '2024-01-10', (SELECT id FROM PLAYLIST OFFSET 9 LIMIT 1), 48),
('artist1@marmut.com', gen_random_uuid(), 'My Compositions', 'Karya-karya saya', 15, '2024-01-11', (SELECT id FROM PLAYLIST OFFSET 10 LIMIT 1), 42),
('artist2@marmut.com', gen_random_uuid(), 'Inspirational Songs', 'Lagu-lagu inspiratif', 15, '2024-01-12', (SELECT id FROM PLAYLIST OFFSET 11 LIMIT 1), 44),
('artist3@marmut.com', gen_random_uuid(), 'Ballad Collection', 'Koleksi lagu ballad', 15, '2024-01-13', (SELECT id FROM PLAYLIST OFFSET 12 LIMIT 1), 51),
('artist4@marmut.com', gen_random_uuid(), 'Upbeat Tracks', 'Lagu-lagu ceria', 15, '2024-01-14', (SELECT id FROM PLAYLIST OFFSET 13 LIMIT 1), 36),
('artist5@marmut.com', gen_random_uuid(), 'Nostalgic Tunes', 'Lagu-lagu nostalgia', 15, '2024-01-15', (SELECT id FROM PLAYLIST OFFSET 14 LIMIT 1), 49),
('user11@marmut.com', gen_random_uuid(), 'Study Playlist', 'Lagu untuk belajar', 15, '2024-01-16', (SELECT id FROM PLAYLIST OFFSET 15 LIMIT 1), 33),
('user12@marmut.com', gen_random_uuid(), 'Rainy Day Songs', 'Lagu untuk hari hujan', 15, '2024-01-17', (SELECT id FROM PLAYLIST OFFSET 16 LIMIT 1), 40),
('user13@marmut.com', gen_random_uuid(), 'Happy Vibes', 'Lagu-lagu bahagia', 15, '2024-01-18', (SELECT id FROM PLAYLIST OFFSET 17 LIMIT 1), 37),
('user14@marmut.com', gen_random_uuid(), 'Throwback Hits', 'Lagu-lagu lawas', 15, '2024-01-19', (SELECT id FROM PLAYLIST OFFSET 18 LIMIT 1), 54),
('user15@marmut.com', gen_random_uuid(), 'Relaxation Mix', 'Lagu untuk relaksasi', 15, '2024-01-20', (SELECT id FROM PLAYLIST OFFSET 19 LIMIT 1), 46);

-- ===================================
-- AKUN_PLAY_USER_PLAYLIST - 15 records
-- ===================================

INSERT INTO AKUN_PLAY_USER_PLAYLIST (email_pemain, id_user_playlist, email_pembuat, waktu) VALUES
('user1@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user1@marmut.com' LIMIT 1), 'user1@marmut.com', '2024-01-01 10:00:00'),
('user2@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user1@marmut.com' LIMIT 1), 'user1@marmut.com', '2024-01-01 11:00:00'),
('user3@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user2@marmut.com' LIMIT 1), 'user2@marmut.com', '2024-01-01 12:00:00'),
('user4@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user2@marmut.com' LIMIT 1), 'user2@marmut.com', '2024-01-01 13:00:00'),
('user5@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user3@marmut.com' LIMIT 1), 'user3@marmut.com', '2024-01-01 14:00:00'),
('user6@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user3@marmut.com' LIMIT 1), 'user3@marmut.com', '2024-01-01 15:00:00'),
('user7@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user4@marmut.com' LIMIT 1), 'user4@marmut.com', '2024-01-01 16:00:00'),
('user8@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user4@marmut.com' LIMIT 1), 'user4@marmut.com', '2024-01-01 17:00:00'),
('user9@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user5@marmut.com' LIMIT 1), 'user5@marmut.com', '2024-01-01 18:00:00'),
('user10@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user5@marmut.com' LIMIT 1), 'user5@marmut.com', '2024-01-01 19:00:00'),
('artist1@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user6@marmut.com' LIMIT 1), 'user6@marmut.com', '2024-01-01 20:00:00'),
('artist2@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user6@marmut.com' LIMIT 1), 'user6@marmut.com', '2024-01-01 21:00:00'),
('artist3@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user7@marmut.com' LIMIT 1), 'user7@marmut.com', '2024-01-01 22:00:00'),
('artist4@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user7@marmut.com' LIMIT 1), 'user7@marmut.com', '2024-01-01 23:00:00'),
('artist5@marmut.com', (SELECT id_user_playlist FROM USER_PLAYLIST WHERE email_pembuat = 'user8@marmut.com' LIMIT 1), 'user8@marmut.com', '2024-01-02 00:00:00');

-- ===================================
-- DOWNLOADED_SONG - 10 records
-- ===================================

INSERT INTO DOWNLOADED_SONG (id_song, email_downloader) VALUES
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1) LIMIT 1), 'user1@marmut.com'),
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1) LIMIT 1), 'user1@marmut.com'),
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1) LIMIT 1), 'user2@marmut.com'),
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1) LIMIT 1), 'user2@marmut.com'),
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1) LIMIT 1), 'artist1@marmut.com'),
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1) LIMIT 1), 'artist1@marmut.com'),
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1) LIMIT 1), 'artist2@marmut.com'),
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1) LIMIT 1), 'artist2@marmut.com'),
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Pelangi Setelah Hujan' LIMIT 1) LIMIT 1), 'user3@marmut.com'),
((SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bintang Di Langit' LIMIT 1) LIMIT 1), 'user3@marmut.com');

-- ===================================
-- ROYALTI - 20 records
-- ===================================

INSERT INTO ROYALTI (id_pemilik_hak_cipta, id_song, jumlah) VALUES
-- Songs from Album Cinta
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 50 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kamu & Kenangan' LIMIT 1) LIMIT 1), 75000),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 48 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Luar Biasa' LIMIT 1) LIMIT 1), 57600),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 45 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Jangan Menyerah' LIMIT 1) LIMIT 1), 44100),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 42 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bahagia Itu Sederhana' LIMIT 1) LIMIT 1), 88200),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 40 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Mimpi Yang Sempurna' LIMIT 1) LIMIT 1), 72000),
-- Songs from Album Bahagia
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 38 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Senja Di Jakarta' LIMIT 1) LIMIT 1), 62700),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 35 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Rindu Setengah Mati' LIMIT 1) LIMIT 1), 77000),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 32 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Sejati' LIMIT 1) LIMIT 1), 60800),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 28 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Masa Lalu' LIMIT 1) LIMIT 1), 30800),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 25 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harapan Baru' LIMIT 1) LIMIT 1), 43750),
-- Songs from Album Kenangan
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 22 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Pelangi Setelah Hujan' LIMIT 1) LIMIT 1), 30800),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 18 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bintang Di Langit' LIMIT 1) LIMIT 1), 28800),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 12 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cinta Pertama' LIMIT 1) LIMIT 1), 24000),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 8 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Kenangan Terindah' LIMIT 1) LIMIT 1), 14800),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 5 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Satu Hati' LIMIT 1) LIMIT 1), 6500),
-- Songs from Album Inspirasi
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 52 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Impian Tinggi' LIMIT 1) LIMIT 1), 80600),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 58 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Cahaya Hati' LIMIT 1) LIMIT 1), 98600),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 62 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Bersama Selamanya' LIMIT 1) LIMIT 1), 120900),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 68 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Melodi Cinta' LIMIT 1) LIMIT 1), 98600),
((SELECT id FROM PEMILIK_HAK_CIPTA WHERE rate_royalti = 72 LIMIT 1), (SELECT id_konten FROM SONG WHERE id_konten = (SELECT id FROM KONTEN WHERE judul = 'Harmoni Jiwa' LIMIT 1) LIMIT 1), 129600);