"""
İndirildiği anda ki konfigürasyon ayarları
"""
import appdirs

deneyapKart = "deneyap:esp32:dydk_mpv10"
deneyapMini = "deneyap:esp32:dym_mpv10"

AGENT_VERSION = "0.10.2"
DENEYAP_VERSION = "1.3.2"
TEMP_PATH = f"{appdirs.user_data_dir()}\DeneyapKartWeb\Temp"
CONFIG_PATH = f"{appdirs.user_data_dir()}\DeneyapKartWeb"
LOG_PATH = f"{appdirs.user_data_dir()}\DeneyapKartWeb"
LIB_PATH = f"{appdirs.user_data_dir()}/DeneyapKartWeb/packages/deneyap/hardware/esp32/{DENEYAP_VERSION}/libraries"
