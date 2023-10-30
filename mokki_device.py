from phew import connect_to_wifi, is_connected_to_wifi

from config import config
from modes import app_mode, setup_mode

def main():
    ssid = config.get("wifi_ssid")
    if config.get("uid") and ssid:
        connect_to_wifi(ssid, config.get("wifi_password"))

    if is_connected_to_wifi():
        app_mode.start()
    else:
        setup_mode.start()

if __name__ == "__main__":
    main()