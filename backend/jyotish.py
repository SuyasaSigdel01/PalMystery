import swisseph as swe

RASHIS_NE = [
    "मेष", "वृष", "मिथुन", "कर्कट", "सिंह", "कन्या",
    "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन",
]

RASHIS_EN = [
    "Mesh", "Vrish", "Mithun", "Karkat", "Simha", "Kanya",
    "Tula", "Vrishchik", "Dhanu", "Makar", "Kumbha", "Meen",
]

NEPAL_TZ_OFFSET = 5.75

swe.set_sid_mode(swe.SIDM_LAHIRI)


def moon_rashi(year, month, day, hour, minute, tz_offset=NEPAL_TZ_OFFSET):
    ut_hour = hour + minute / 60.0 - tz_offset
    jd = swe.julday(year, month, day, ut_hour)

    flags = swe.FLG_MOSEPH | swe.FLG_SIDEREAL
    position, _ = swe.calc_ut(jd, swe.MOON, flags)

    longitude = position[0]
    index = int(longitude // 30)

    return {
        "index": index,
        "nepali": RASHIS_NE[index],
        "english": RASHIS_EN[index],
        "moon_longitude": round(longitude, 4),
    }