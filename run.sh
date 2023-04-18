#!/bin/bash
arecord --list-devices & sudo python3 WordCloudGenerator.py & cd AzureSpeechCC && /home/wordcloud/.dotnet/dotnet run & sleep 10s && sudo python write_to_oled.py
