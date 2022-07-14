#!/bin/bash
sudo python3 WordCloudGenerator.py & cd AzureSpeechCC
sleep 10s
sudo python3 write_to_oled.py