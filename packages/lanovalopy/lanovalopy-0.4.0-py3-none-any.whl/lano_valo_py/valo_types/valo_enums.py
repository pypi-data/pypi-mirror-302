from enum import Enum


class Episodes(str, Enum):
    e1a1 = "e1a1"
    e1a2 = "e1a2"
    e1a3 = "e1a3"
    e2a1 = "e2a1"
    e2a2 = "e2a2"
    e2a3 = "e2a3"
    e3a1 = "e3a1"
    e3a2 = "e3a2"
    e3a3 = "e3a3"
    e4a1 = "e4a1"
    e4a2 = "e4a2"
    e4a3 = "e4a3"
    e5a1 = "e5a1"
    e5a2 = "e5a2"
    e5a3 = "e5a3"


class LeaderboardEpisodes(str, Enum):
    e2a1 = "e2a1"
    e2a2 = "e2a2"
    e2a3 = "e2a3"
    e3a1 = "e3a1"
    e3a2 = "e3a2"
    e3a3 = "e3a3"
    e4a1 = "e4a1"
    e4a2 = "e4a2"
    e4a3 = "e4a3"
    e5a1 = "e5a1"
    e5a2 = "e5a2"
    e5a3 = "e5a3"


class Modes(str, Enum):
    escalation = "escalation"
    spikerush = "spikerush"
    deathmatch = "deathmatch"
    competitive = "competitive"
    unrated = "unrated"
    replication = "replication"
    custom = "custom"
    newmap = "newmap"
    snowball = "snowball"


class Maps(str, Enum):
    ascent = "ascent"
    split = "split"
    fracture = "fracture"
    bind = "bind"
    breeze = "breeze"
    icebox = "icebox"
    haven = "haven"
    pearl = "pearl"


class CCRegions(str, Enum):
    en_gb = "en-gb"
    en_us = "en-us"
    es_es = "es-es"
    es_mx = "es-mx"
    fr_fr = "fr-fr"
    it_it = "it-it"
    ja_jp = "ja-jp"
    ko_kr = "ko-kr"
    pt_br = "pt-br"
    ru_ru = "ru-ru"
    tr_tr = "tr-tr"
    vi_vn = "vi-vn"


class Locales(str, Enum):
    ar_AE = "ar-AE"
    de_DE = "de-DE"
    en_GB = "en-GB"
    en_US = "en-US"
    es_ES = "es-ES"
    es_MX = "es-MX"
    fr_FR = "fr-FR"
    id_ID = "id-ID"
    it_IT = "it-IT"
    ja_JP = "ja-JP"
    ko_KR = "ko-KR"
    pl_PL = "pl-PL"
    pt_BR = "pt-BR"
    ru_RU = "ru-RU"
    th_TH = "th-TH"
    tr_TR = "tr-TR"
    vi_VN = "vi-VN"
    zn_CN = "zn-CN"
    zn_TW = "zn-TW"


class RawTypes(str, Enum):
    competitiveupdates = "competitiveupdates"
    mmr = "mmr"
    matchdetails = "matchdetails"
    matchhistory = "matchhistory"


class MMRVersions(str, Enum):
    v1 = "v1"
    v2 = "v2"


class FeaturedItemsVersion(str, Enum):
    v1 = "v1"
    v2 = "v2"


class LeaderboardVersions(str, Enum):
    v1 = "v1"
    v2 = "v2"
    v3 = "v3"


class Regions(str, Enum):
    eu = "eu"
    na = "na"
    kr = "kr"
    ap = "ap"
    latam = "latam"
    br = "br"


class EsportsRegions(str, Enum):
    international = "international"
    north_america = "north_america"
    emea = "emea"
    brazil = "brazil"
    japan = "japan"
    korea = "korea"
    latin_america = "latin_america"
    latin_america_south = "latin_america_south"
    latin_america_north = "latin_america_north"
    southeast_asia = "southeast_asia"
    vietnam = "vietnam"
    oceania = "oceania"


class EsportsLeagues(str, Enum):
    VCT_AMERICAS = "vct_americas"
    CHALLENGERS_NA = "challengers_na"
    GAME_CHANGERS_NA = "game_changers_na"
    VCT_EMEA = "vct_emea"
    VCT_PACIFIC = "vct_pacific"
    CHALLENGERS_BR = "challengers_br"
    CHALLENGERS_JPN = "challengers_jpn"
    CHALLENGERS_KR = "challengers_kr"
    CHALLENGERS_LATAM = "challengers_latam"
    CHALLENGERS_LATAM_N = "challengers_latam_n"
    CHALLENGERS_LATAM_S = "challengers_latam_s"
    CHALLENGERS_APAC = "challengers_apac"
    CHALLENGERS_SEA_ID = "challengers_sea_id"
    CHALLENGERS_SEA_PH = "challengers_sea_ph"
    CHALLENGERS_SEA_SG_AND_MY = "challengers_sea_sg_and_my"
    CHALLENGERS_SEA_TH = "challengers_sea_th"
    CHALLENGERS_SEA_HK_AND_TW = "challengers_sea_hk_and_tw"
    CHALLENGERS_SEA_VN = "challengers_sea_vn"
    VALORANT_OCEANIA_TOUR = "valorant_oceania_tour"
    CHALLENGERS_SOUTH_ASIA = "challengers_south_asia"
    GAME_CHANGERS_SEA = "game_changers_sea"
    GAME_CHANGERS_SERIES_BRAZIL = "game_changers_series_brazil"
    GAME_CHANGERS_EAST_ASIA = "game_changers_east_asia"
    GAME_CHANGERS_EMEA = "game_changers_emea"
    GAME_CHANGERS_JPN = "game_changers_jpn"
    GAME_CHANGERS_KR = "game_changers_kr"
    GAME_CHANGERS_LATAM = "game_changers_latam"
    GAME_CHANGERS_CHAMPIONSHIP = "game_changers_championship"
    MASTERS = "masters"
    LAST_CHANCE_QUALIFIER_APAC = "last_chance_qualifier_apac"
    LAST_CHANCE_QUALIFIER_EAST_ASIA = "last_chance_qualifier_east_asia"
    LAST_CHANCE_QUALIFIER_EMEA = "last_chance_qualifier_emea"
    LAST_CHANCE_QUALIFIER_NA = "last_chance_qualifier_na"
    LAST_CHANCE_QUALIFIER_BR_AND_LATAM = "last_chance_qualifier_br_and_latam"
    VCT_LOCK_IN = "vct_lock_in"
    CHAMPIONS = "champions"
    VRL_SPAIN = "vrl_spain"
    VRL_NORTHERN_EUROPE = "vrl_northern_europe"
    VRL_DACH = "vrl_dach"
    VRL_FRANCE = "vrl_france"
    VRL_EAST = "vrl_east"
    VRL_TURKEY = "vrl_turkey"
    VRL_CIS = "vrl_cis"
    MENA_RESILIENCE = "mena_resilence"
    CHA = "cha"
