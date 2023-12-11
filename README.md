# mokki-pico

Micropython project files for Raspberry Pico Pi W (Micropython RP2040)

## Installation

### Required packages

- micropython-umqtt.simple
- micropython_qr
- micropython_ssd1306

OpenSSL certificate ca.crt for MQTT needs to be placed inside the certs folder.
TPM generated secret needs to be placed inside the secrets folder. Script for generating the secret [here](https://github.com/teemueer/mokki-flask/blob/master/management/tpm.sh).

- Uses DHT22 (on pin 26) and KY018 (on pin 27) sensors.
- SSD1306 OLED monitor on SCL 15 and SDA 14.
- Change to bluetooth mode is set on button on pin 9.
