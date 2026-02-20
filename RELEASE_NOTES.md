# Release Notes — Adzanid v1.2.0

**Release Date:** February 20, 2026

---

## New Features

### Adhan Volume & Mute Control
- Users can now adjust the adhan volume using a slider in the Settings tab.
- A **Mute** option is available to silence the adhan completely.
- Volume and mute preferences are saved automatically and restored on next launch.

### Do Not Disturb (Focus Assist) Integration
- The adhan **will not play** when **Do Not Disturb / Focus Assist** mode is active on Windows, macOS, or Linux.
- Prayer time notifications will still appear even when DND is active (without audio).

### New Cities Added
The following cities are now available in the city selector:
- Tangerang Selatan, Banyuwangi, Jember, Cimahi, Karawang, Cikarang, Cianjur
- Cilacap, Tegal, Klaten, Demak, Kendal, Kebumen, Wonosobo, Wonosari
- Boyolali, Tulungagung, Ponorogo, Lamongan, Tuban, Pamekasan, Bangkalan
- Baubau, Kolaka, Pandeglang, Purwakarta

### Coordinate-Based Prayer Time Accuracy
- Prayer times are now fetched using **GPS coordinates** instead of city names.
- This fixes inaccurate results for cities not recognized by the Aladhan API (e.g. Tangerang Selatan).

---

## Bug Fixes

### Prayer Schedule Not Updating After Midnight
- **Before:** The prayer schedule would remain stuck on the previous day's data if the app was left running past midnight.
- **After:** The app now automatically detects a day change and re-fetches the latest schedule from the API.

---

## Other Changes
- Application version bumped to **v1.2.0**.

---

## Upgrading from v1.1.0
Users still on v1.1.0 will see an automatic update notification in the Schedule tab when they open the app.
