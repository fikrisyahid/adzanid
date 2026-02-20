"""Application-wide constants and configuration."""

APP_NAME = "Adzanid"
APP_TITLE = "Jadwal Sholat Indonesia"
APP_VERSION = "1.2.0"
SETTINGS_ORG = "Adzanid"
SETTINGS_APP = "Adzanid"

GITHUB_URL = "https://github.com/fikrisyahid/"
AUTHOR = "Fikri Syahid"
COPYRIGHT_YEAR = 2026

# Default adhan audio file path
DEFAULT_ADHAN_PATH = "assets/adzan.mp3"

# Icon file paths
ICON_PATH = "assets/icon.png"

# Mapping from UI prayer names to Aladhan API keys
PRAYER_NAME_MAP = {
    "Subuh": "Fajr",
    "Dzuhur": "Dhuhr",
    "Ashar": "Asr",
    "Maghrib": "Maghrib",
    "Isya": "Isha",
}

PRAYER_NAMES = list(PRAYER_NAME_MAP.keys())

# City coordinates mapping: city name → (latitude, longitude)
# Used for accurate prayer time lookups via Aladhan coordinates API.
CITY_COORDINATES: dict[str, tuple[float, float]] = {
    # -- Aceh --
    "Banda Aceh": (5.5483, 95.3238),
    "Lhokseumawe": (5.1801, 97.1507),
    # -- Sumatera Utara --
    "Medan": (3.5952, 98.6722),
    "Binjai": (3.6001, 98.4854),
    "Pematangsiantar": (2.9498, 99.0486),
    "Sibolga": (1.7427, 98.7792),
    "Tanjungbalai": (2.9664, 99.7946),
    "Tebing Tinggi": (3.3254, 99.1626),
    "Simalungun": (2.9397, 99.0547),
    # -- Sumatera Barat --
    "Padang": (-0.9493, 100.3543),
    "Bukittinggi": (-0.3056, 100.3692),
    "Padang Panjang": (-0.4728, 100.3958),
    "Padangpariaman": (-0.6284, 100.1223),
    "Pariaman": (-0.6263, 100.1179),
    "Solok": (-0.7901, 100.6543),
    # -- Riau --
    "Pekanbaru": (0.5070, 101.4478),
    "Dumai": (1.6667, 101.4500),
    # -- Kepulauan Riau --
    "Batam": (1.1301, 104.0529),
    "Tanjung Pinang": (0.9186, 104.4463),
    # -- Jambi --
    "Jambi": (-1.6101, 103.6131),
    "Sungai Penuh": (-2.0600, 101.3928),
    # -- Sumatera Selatan --
    "Palembang": (-2.9761, 104.7754),
    "Lubuklinggau": (-3.2968, 102.8617),
    "Prabumulih": (-3.4333, 104.2333),
    "Baturaja": (-4.1290, 104.1667),
    "Lahat": (-3.7839, 103.5300),
    "Panjang": (-5.4700, 105.3200),
    "Sakatiga": (-3.0333, 104.7333),
    # -- Bengkulu --
    "Bengkulu": (-3.8004, 102.2655),
    # -- Lampung --
    "Bandar Lampung": (-5.3971, 105.2668),
    "Metro": (-5.1138, 105.3067),
    # -- Bangka Belitung --
    "Pangkal Pinang": (-2.1275, 106.1139),
    "Tanjungpandan": (-2.7500, 107.6500),
    # -- Banten --
    "Serang": (-6.1104, 106.1640),
    "Cilegon": (-6.0025, 106.0161),
    "Tangerang": (-6.1783, 106.6319),
    "Tangerang Selatan": (-6.2943, 106.7143),
    "Rangkasbitung": (-6.3540, 106.2510),
    "Pandeglang": (-6.3129, 106.1050),
    # -- DKI Jakarta --
    "Jakarta": (-6.2088, 106.8456),
    # -- Jawa Barat --
    "Bandung": (-6.9175, 107.6191),
    "Bekasi": (-6.2383, 107.0000),
    "Bogor": (-6.5971, 106.8060),
    "Cianjur": (-6.7351, 107.1395),
    "Cikarang": (-6.2833, 107.1500),
    "Cimahi": (-6.8722, 107.5408),
    "Cirebon": (-6.7063, 108.5570),
    "Depok": (-6.4025, 106.7942),
    "Garut": (-7.2167, 107.9064),
    "Karawang": (-6.3210, 107.3381),
    "Purwakarta": (-6.5561, 107.4371),
    "Subang": (-6.5714, 107.7529),
    "Sukabumi": (-6.9210, 106.9300),
    "Tasikmalaya": (-7.3274, 108.2207),
    # -- Jawa Tengah --
    "Boyolali": (-7.5337, 110.5962),
    "Cilacap": (-7.7325, 109.0157),
    "Demak": (-6.8936, 110.6385),
    "Kebumen": (-7.6680, 109.6508),
    "Kendal": (-6.9184, 110.2024),
    "Klaten": (-7.7059, 110.6058),
    "Kudus": (-6.8048, 110.8405),
    "Magelang": (-7.4797, 110.2177),
    "Pati": (-6.7463, 111.0401),
    "Pekalongan": (-6.8885, 109.6753),
    "Purwokerto": (-7.4243, 109.2355),
    "Purworejo": (-7.7208, 110.0005),
    "Salatiga": (-7.3319, 110.5062),
    "Semarang": (-6.9932, 110.4203),
    "Surakarta": (-7.5755, 110.8243),
    "Tegal": (-6.8797, 109.1256),
    "Wonosari": (-7.9656, 110.5987),
    "Wonosobo": (-7.3584, 109.9021),
    # -- DI Yogyakarta --
    "Yogyakarta": (-7.7971, 110.3688),
    # -- Jawa Timur --
    "Bangkalan": (-7.0458, 112.7351),
    "Banyuwangi": (-8.2192, 114.3691),
    "Batu": (-7.8672, 112.5239),
    "Blitar": (-8.0957, 112.1609),
    "Gresik": (-7.1625, 112.6514),
    "Jember": (-8.1724, 113.6884),
    "Jombang": (-7.5457, 112.2318),
    "Kediri": (-7.8165, 112.0115),
    "Lamongan": (-7.1193, 112.4213),
    "Madiun": (-7.6298, 111.5238),
    "Malang": (-7.9797, 112.6304),
    "Mojokerto": (-7.4703, 112.4344),
    "Nganjuk": (-7.6050, 111.9051),
    "Pamekasan": (-7.1571, 113.4741),
    "Pasuruan": (-7.6453, 112.9075),
    "Ponorogo": (-7.8669, 111.4649),
    "Probolinggo": (-7.7543, 113.2159),
    "Sidoarjo": (-7.4478, 112.7183),
    "Situbondo": (-7.7068, 114.0046),
    "Surabaya": (-7.2575, 112.7521),
    "Tuban": (-6.8990, 112.0508),
    "Tulungagung": (-8.0656, 111.9047),
    # -- Bali --
    "Denpasar": (-8.6705, 115.2126),
    "Singaraja": (-8.1120, 115.0883),
    "Tabanan": (-8.5412, 115.1253),
    "Ubud": (-8.5069, 115.2625),
    # -- NTB --
    "Mataram": (-8.5833, 116.1167),
    # -- NTT --
    "Kupang": (-10.1718, 123.6074),
    "Maumere": (-8.6200, 122.2100),
    "Ruteng": (-8.6100, 120.4700),
    "Waingapu": (-9.6564, 120.2640),
    # -- Kalimantan Barat --
    "Ketapang": (-1.8500, 109.9833),
    "Pontianak": (-0.0263, 109.3425),
    "Sambas": (1.3500, 109.3000),
    "Singkawang": (0.9053, 108.9619),
    # -- Kalimantan Tengah --
    "Palangkaraya": (-2.2136, 113.9108),
    # -- Kalimantan Selatan --
    "Banjarbaru": (-3.4417, 114.8333),
    "Banjarmasin": (-3.3186, 114.5944),
    # -- Kalimantan Timur --
    "Balikpapan": (-1.2379, 116.8529),
    "Bontang": (0.1333, 117.5000),
    "Samarinda": (-0.5022, 117.1536),
    # -- Kalimantan Utara --
    "Nunukan": (4.1383, 117.6656),
    "Tanjung Selor": (2.8477, 117.3640),
    "Tarakan": (3.3000, 117.6333),
    # -- Sulawesi Utara --
    "Bitung": (1.4404, 125.1217),
    "Kotamobagu": (0.7240, 124.3215),
    "Manado": (1.4748, 124.8421),
    "Tomohon": (1.3193, 124.8316),
    # -- Gorontalo --
    "Gorontalo": (0.5435, 123.0593),
    # -- Sulawesi Tengah --
    "Luwuk": (-0.9500, 122.7833),
    "Palu": (-0.8917, 119.8707),
    # -- Sulawesi Selatan --
    "Makassar": (-5.1477, 119.4327),
    "Palopo": (-2.9933, 120.1978),
    "Parepare": (-4.0135, 119.6255),
    # -- Sulawesi Barat --
    "Mamuju": (-2.6809, 118.8875),
    # -- Sulawesi Tenggara --
    "Baubau": (-5.4710, 122.6040),
    "Kendari": (-3.9985, 122.5127),
    "Kolaka": (-4.0752, 121.5873),
    # -- Maluku --
    "Ambon": (-3.6954, 128.1814),
    "Tual": (-5.6333, 132.7500),
    # -- Maluku Utara --
    "Sofifi": (0.7333, 127.5667),
    "Ternate": (0.7833, 127.3667),
    "Tidore": (0.6833, 127.4000),
    # -- Papua / Papua Barat --
    "Biak": (-1.1800, 136.0800),
    "Fakfak": (-2.9200, 132.2900),
    "Jayapura": (-2.5337, 140.7181),
    "Manokwari": (-0.8614, 134.0820),
    "Merauke": (-8.4932, 140.4018),
    "Sorong": (-0.8762, 131.2560),
    "Tanahmerah": (-6.1000, 140.3000),
    "Timika": (-4.5500, 136.8833),
    "Wamena": (-4.0955, 138.9522),
    # -- Kota Bharu (Kalimantan) --
    "Kota Bharu": (-3.2943, 116.1700),
}

# Sorted city list derived from coordinates
CITIES = sorted(CITY_COORDINATES.keys())
