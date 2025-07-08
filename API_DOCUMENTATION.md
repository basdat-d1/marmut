# MARMUT REST API DOCUMENTATION

## Overview
This document describes the REST API endpoints for the Marmut music and podcast streaming platform. All endpoints use JSON for request and response bodies.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
Most endpoints require authentication. Users must be logged in to access protected routes.

---

## 1. NAVBAR FUNCTIONALITY
The navbar displays different options based on user authentication status and roles:

### Guest (Not Logged In)
- Login
- Registration

### Authenticated Users
- Dashboard
- [If User/Artist/Songwriter/Podcaster] Chart
- [If User/Artist/Songwriter/Podcaster] Search Bar
- [If User/Artist/Songwriter/Podcaster] Kelola Playlist
- [If User/Artist/Songwriter/Podcaster] Langganan Paket
- [If Premium] Kelola Downloaded Songs
- [If Podcaster] Kelola Podcast
- [If Artist/Songwriter] Kelola Album & Songs
- [If Label] Kelola Album
- [If Artist/Songwriter/Label] Cek Royalti
- Logout

---

## 2. AUTHENTICATION ENDPOINTS (Features 2-3)

### Get CSRF Token
```http
GET /get-csrf-token/
```
**Response:**
```json
{
  "csrfToken": "token_value"
}
```

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (User):**
```json
{
  "message": "Login berhasil",
  "user": {
    "email": "user@example.com",
    "name": "User Name",
    "type": "user",
    "roles": ["user", "artist"],
    "is_premium": false,
    "is_verified": true,
    "kota_asal": "Jakarta",
    "gender": 1,
    "tempat_lahir": "Jakarta",
    "tanggal_lahir": "1990-01-01"
  }
}
```

**Response (Label):**
```json
{
  "message": "Login berhasil",
  "user": {
    "email": "label@example.com",
    "name": "Label Name",
    "type": "label",
    "contact": "+62123456789"
  }
}
```

### Logout
```http
POST /api/auth/logout/
```

### Get Current User
```http
GET /api/auth/me/
```

### Register User
```http
POST /api/auth/register/user/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "nama": "User Name",
  "gender": 1,
  "tempat_lahir": "Jakarta",
  "tanggal_lahir": "1990-01-01",
  "kota_asal": "Jakarta",
  "roles": ["artist", "songwriter"]
}
```

### Register Label
```http
POST /api/auth/register/label/
Content-Type: application/json

{
  "email": "label@example.com",
  "password": "password123",
  "nama": "Label Name",
  "kontak": "+62123456789"
}
```

---

## 3. DASHBOARD ENDPOINTS (Feature 4)

### Get Dashboard
```http
GET /api/dashboard/
```

**Response (User):**
```json
{
  "user": {
    "email": "user@example.com",
    "nama": "User Name",
    "is_verified": true,
    "kota_asal": "Jakarta",
    "gender": "Laki-laki",
    "tempat_lahir": "Jakarta",
    "tanggal_lahir": "1990-01-01",
    "roles": ["user", "artist"],
    "is_premium": false,
    "subscription": null
  },
  "playlists": [...],
  "songs": [...],
  "podcasts": [...]
}
```

### Get User Statistics
```http
GET /api/dashboard/stats/
```

---

## 4. USER PLAYLIST MANAGEMENT (Feature 5)

### List User Playlists
```http
GET /api/user-playlist/
```

### Create Playlist
```http
POST /api/user-playlist/
Content-Type: application/json

{
  "judul": "My Playlist",
  "deskripsi": "My favorite songs"
}
```

### Get Playlist Detail
```http
GET /api/user-playlist/{playlist_id}/
```

### Update Playlist
```http
PUT /api/user-playlist/{playlist_id}/
Content-Type: application/json

{
  "judul": "Updated Playlist",
  "deskripsi": "Updated description"
}
```

### Delete Playlist
```http
DELETE /api/user-playlist/{playlist_id}/
```

### Add Song to Playlist
```http
POST /api/user-playlist/{playlist_id}/add-song/
Content-Type: application/json

{
  "song_id": "song_uuid"
}
```

### Remove Song from Playlist
```http
DELETE /api/user-playlist/{playlist_id}/remove-song/{song_id}/
```

### Get Available Songs
```http
GET /api/user-playlist/available-songs/
```

---

## 5. SUBSCRIPTION MANAGEMENT (Feature 6)

### Get Subscription Packages
```http
GET /api/subscription/packages/
```

### Subscribe to Package
```http
POST /api/subscription/subscribe/
Content-Type: application/json

{
  "jenis_paket": "1 Bulan",
  "metode_bayar": "E-Wallet"
}
```

### Get Transaction History
```http
GET /api/subscription/history/
```

### Get Current Subscription
```http
GET /api/subscription/current/
```

### Cancel Subscription
```http
POST /api/subscription/cancel/
```

### Get Payment Methods
```http
GET /api/subscription/payment-methods/
```

---

## 6. SEARCH FUNCTIONALITY (Feature 7)

### Universal Search
```http
GET /api/search/?q=query_string
```

**Response:**
```json
{
  "message": "Ditemukan 5 hasil untuk \"love\"",
  "query": "love",
  "results": {
    "songs": [...],
    "podcasts": [...],
    "playlists": [...],
    "all": [...],
    "total": 5
  }
}
```

### Search Songs Only
```http
GET /api/search/songs/?q=query_string
```

### Search Podcasts Only
```http
GET /api/search/podcasts/?q=query_string
```

### Search Playlists Only
```http
GET /api/search/playlists/?q=query_string
```

---

## 7. PLAY SONG ENDPOINTS (Feature 8)

### Get Song Details
```http
GET /api/play-song/{song_id}/
```

### Play Song (Track Progress)
```http
POST /api/play-song/{song_id}/play/
Content-Type: application/json

{
  "progress": 75
}
```

### Add Song to Playlist
```http
POST /api/play-song/{song_id}/add-to-playlist/
Content-Type: application/json

{
  "playlist_id": "playlist_uuid"
}
```

### Download Song (Premium Only)
```http
POST /api/play-song/{song_id}/download/
```

---

## 8. DOWNLOADED SONGS (Feature 9)

### Get Downloaded Songs
```http
GET /api/downloads/
```

### Remove Downloaded Song
```http
DELETE /api/downloads/{song_id}/
```

---

## 9. PLAY PODCAST (Feature 10)

### Get Podcast Details
```http
GET /api/play-podcast/{podcast_id}/
```

---

## 10. PLAY USER PLAYLIST (Feature 11)

### Get Playlist Details
```http
GET /api/play-user-playlist/{playlist_id}/
```

### Shuffle Play Playlist
```http
POST /api/play-user-playlist/{playlist_id}/shuffle-play/
```

### Play Single Song from Playlist
```http
POST /api/play-user-playlist/{playlist_id}/play-song/{song_id}/
```

---

## 11. CHARTS (Feature 12)

### Get Chart Types
```http
GET /api/chart/
```

### Get Chart Details
```http
GET /api/chart/{chart_type}/
```

**Available Chart Types:**
- Daily Top 20
- Weekly Top 20
- Monthly Top 20
- Global Top 50
- Trending Songs
- Top Downloads

---

## 12. ALBUM & SONG MANAGEMENT (Feature 13)

### Create Album with First Song
```http
POST /api/album-song/albums/
Content-Type: application/json

{
  "judul_album": "Album Title",
  "id_label": "label_uuid",
  "judul_lagu": "Song Title",
  "artist_id": "artist_uuid",
  "songwriter_ids": ["songwriter_uuid"],
  "genre_ids": ["genre1", "genre2"],
  "durasi": 180
}
```

### Get User Albums
```http
GET /api/album-song/albums/
```

### Add Song to Album
```http
POST /api/album-song/albums/{album_id}/songs/
Content-Type: application/json

{
  "judul": "Song Title",
  "artist_id": "artist_uuid",
  "songwriter_ids": ["songwriter_uuid"],
  "genre_ids": ["genre1"],
  "durasi": 200
}
```

### Get Album Songs
```http
GET /api/album-song/albums/{album_id}/songs/
```

### Delete Song
```http
DELETE /api/album-song/songs/{song_id}/
```

### Delete Album
```http
DELETE /api/album-song/albums/{album_id}/
```

### Get Available Data for Forms
```http
GET /api/album-song/labels/
GET /api/album-song/artists/
GET /api/album-song/songwriters/
GET /api/album-song/genres/
```

---

## 13. ROYALTY CHECK (Feature 14)

### Get Royalty Information
```http
GET /api/royalty/
```

**Response:**
```json
{
  "royalties": [
    {
      "judul_lagu": "Song Title",
      "judul_album": "Album Title",
      "total_play": 1000,
      "total_download": 50,
      "total_royalti": 150000
    }
  ],
  "total_royalti": 150000
}
```

---

## 14. PODCAST MANAGEMENT (Feature 15)

### Create Podcast
```http
POST /api/podcast/
Content-Type: application/json

{
  "judul": "Podcast Title",
  "genre_ids": ["genre1", "genre2"]
}
```

### Get User Podcasts
```http
GET /api/podcast/
```

### Add Episode to Podcast
```http
POST /api/podcast/{podcast_id}/episodes/
Content-Type: application/json

{
  "judul": "Episode Title",
  "deskripsi": "Episode description",
  "durasi": 3600
}
```

### Get Podcast Episodes
```http
GET /api/podcast/{podcast_id}/episodes/
```

### Delete Episode
```http
DELETE /api/podcast/episodes/{episode_id}/
```

### Delete Podcast
```http
DELETE /api/podcast/{podcast_id}/
```

---

## 15. LABEL ALBUM MANAGEMENT (Feature 16)

### Get Label Albums
```http
GET /api/label/albums/
```

### Get Album Details
```http
GET /api/label/albums/{album_id}/
```

### Delete Album
```http
DELETE /api/label/albums/{album_id}/
```

### Delete Song from Album
```http
DELETE /api/label/albums/{album_id}/songs/{song_id}/
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

---

## Database Schema Notes

The API uses the following main tables:
- `AKUN` - User accounts
- `LABEL` - Record labels
- `PREMIUM`/`NONPREMIUM` - User subscription status
- `PAKET` - Subscription packages
- `TRANSACTION` - Subscription transactions
- `KONTEN` - Base content (songs, podcasts)
- `SONG` - Songs
- `PODCAST` - Podcasts
- `EPISODE` - Podcast episodes
- `ALBUM` - Music albums
- `ARTIST` - Music artists
- `SONGWRITER` - Song writers
- `PODCASTER` - Podcast creators
- `USER_PLAYLIST` - User-created playlists
- `PLAYLIST_SONG` - Songs in playlists
- `DOWNLOADED_SONG` - Downloaded songs
- `AKUN_PLAY_SONG` - Song play history
- `AKUN_PLAY_USER_PLAYLIST` - Playlist play history
- `ROYALTI` - Royalty information

All UUID fields use PostgreSQL's `gen_random_uuid()` function for generation. 