#!/bin/bash
sudo python3 WordCloudGenerator.py & cd AzureSpeechCC && dotnet run & sleep 10s && sudo python write_to_oled.py
