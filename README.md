

# WordCloud
A device that is always listening to it's surrounding and plays back this data via a word cloud on an E-Ink Display.


## Turning On
1. Plug in the microphone.
2. Plug in the power. You know that it is on when you can look in the SD card slot and see a red and green LED blinking
3. The wifi LED should turn green - this means the device is connected to the internet. 
4. The E-Ink screen should flash and change content - this means the hardware script is running fine
5. The OLED screen should eventually show the last word it has heard on the screen. 
6. If all this is happening then everything is working fine! If not see below....

## Troubleshooting
- No blinking LEDS on start up - No power. Check the cable is ok.
- Only see a blinking or solid red LED on startup - This means there is likely either no SD card or it has become corrupted. Either replace the SD card with a new one with the WordCloud image on or connect to a screen to investigate further
- Not Green wifi LED - No internet connection, please see the 'Add New Credentials' Section below.
- The OLED screen doesn't do anything after 5 mins of waiting - some or all of the scripts are not running. Access the device remotely using Dataplicity or SSH and run the following scripts:
   ```
   cd home/wordcloud/WordCloud/
   bash run.sh
   ```
- You should now waitto see the words 'connecting to pipe' then 'pipe connected' then 'Ready Speak' - If this is the case then the OLED should now be working.
- If these words don't all appear then we need to run one more line of code:
   ```
   sudo python3 write_to_oled.py
   ```


  ******************************************************************************
  ******************************************************************************
## HOW TO CLONE FROM GITHUB

**1. delete the folder WordCloud on your device**

**2. Make sure that you've got an ssh key on your device**

if not, do following:
The first step involves creating a set of RSA keys for use in authentication.
This should be done on the client.
To create your public and private SSH keys on the command-line:
```
$ mkdir ~/.ssh
$ chmod 700 ~/.ssh
$ ssh-keygen
```
You will be prompted for a location to save the keys, and a passphrase for the keys. This passphrase will protect your private key while it's stored on the hard drive:

Generating public/private rsa key pair.
Enter file in which to save the key (/home/b/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/b/.ssh/id_rsa.
Your public key has been saved in /home/b/.ssh/id_rsa.pub.

display your ssh key with following line and copy it
```
$ cat ~/.ssh/id_rsa.pub
```
insert your new ssh key into your git account - setting ssh keys

**3. clone the git repository with ssh:**
```
$ git clone <link> 'WordCloud'
```



  ******************************************************************************
## ADD NEW WIFI CREDENTIALS

To add a wifi network to the WordCloud/Uberblick follow the instructions on [this link] (https://linuxconfig.org/ubuntu-20-04-connect-to-wifi-from-command-line)

But first you need to connect the device to a temporary network. To do this use the hotspot feature on your phone. Change the name of your phone to the SSID and the hotspot password to the netword password. All WordCLouds and Ubewrblicks should remember the following network

SSID: Uniform Go 5

Password: InUniform

**1. First step is to identify the name of your wireless network interface. To do so execute:**

```
$ ls /sys/class/net
enp0s25  lo  wlp3s0
```

Depending on your Ubuntu 20.04 system the wireless network interface name would be something like: wlan0 or like in this case it is wlp3s0.

**2. Next, navigate to the /etc/netplan directory and locate the appropriate Netplan configuration files.**

The configuration file might have a name such as 01-network-manager-all.yaml or 50-cloud-init.yaml.
   
```
$ ls /etc/netplan/

3. Edit the Netplan configuration file:
   
$ sudoedit /etc/netplan/50-cloud-init.yaml
```

and insert the following configuration stanza while replacing the SSID-NAME-HERE and PASSWORD-HERE with your SSID network name and password. Make sure that the wifis block is aligned with the above ethernets or version block if present. The entire configuration file may look similar to the one below:

```
network:
    ethernets:
        eth0:
            dhcp4: true
            optional: true
    version: 2
    wifis:
        wlp3s0:
            optional: true
            access-points:
                "SSID-NAME-HERE":
                    password: "PASSWORD-HERE"
            dhcp4: true
```

**3. Once ready, apply the changes and connect to your wireless interface by executing the bellow command:**

```
$ sudo netplan apply
```

 ******************************************************************************
## LANGUAGE CHANGE

All languages supported are here: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=stt-tts

For Wordclouds you only need to change the language in the Program.cs file. For Uberblicks you also need to change the language in the config file.

**In dataplicity type:**
```
su wordcloud
(enter password - wordcloud)
sudo nano /home/wordcloud/WordCloud/AzureSpeechCC/Program.cs
```

**Now comment/uncomment the language you want using // and delete the // infront of the languages you do not want. Other languages can be added in here easily - see the full list here.**

```
var speechConfig = SpeechConfig.FromSubscription(YourSubscriptionKey, YourServiceRegion);
        // Swiss German
        //speechConfig.SpeechRecognitionLanguage = "de-CH";
        // German
        //speechConfig.SpeechRecognitionLanguage = "de-DE";
        // English
        speechConfig.SpeechRecognitionLanguage = "en-US";

```

**After editing the dotnet file (Program.cs) it first needs to complie, to do this type the following into terminal**
```
dotnet clean
dotnet build
dotnet run
```


 ******************************************************************************
 ## AUTO RUN ON STARTUP
 
 This is done using systemd
There are two start-up files:
```
wordcloud.service
```
```
Startup.service
```

 To edit this file go:
 ```
 sudo nano etc/systemd/system/wordcloud.service
 ```

 Once saved run the following:
 ```
 sudo systemctl daemon-reload
 sudo systemctl start wordcloud.service		This runs the run.sh file
 sudo systemctl enable wordcloud.service	This enables the service file to run on startup
```

To debug it’s useful to look at:
```
 sudo systemctl status wordcloud.service
```
		
 
 ## TO TURN OF AUTO RUN
 ```
 sudo systemctl stop wordcloud.service		This stops the service file running in terminal
 sudo systemctl disable wordcloud.service	This stops the service file running on startup
 ```

 ******************************************************************************
## GENERAL PROCESS

| Script | Description |
| --- | --- |
| run.sh | This file executes everything |
| WordCloudGenerator.py | This reads the contents.txt file, generates a wordcloud, dithers the image to make it E-Ink compatible and finally publishes it to the display.|
| AzureSpeechCC (C# | This file executes everything |
| write_to_oled.py | This launches the speech to text service. The recognized phrases are published to the contents.txt file. The individiual words are send to the PiOLED via a pipe |
| reset_button.py | This opens the pipe with AzureSpeechCC and prints the words to the display |
| WifiStatusLED.py | This runs a script to light an LED when connected to the internet |
| main.py | This runs all the ChatGPT stuff |



******************************************************************************
## BUGS

**initrims Issue fix:**

```
fsck -y /dev/______
exit
```

 ******************************************************************************
## USEFUL COMMANDS FOR DEBUGGING

**Show all python scripts running**
```
ps -fA | grep python3 - 		
```
**Show all programs running**
```
Top
```
**Print speech/text and process stuff in terminal**
```					
journalctl -f -u wordcloud.service	
```

To escape the wordcloud generator in terminal use 
<kbd>Ctrl</kbd> + <kbd>Z</kbd>

To escape the other scripts in terminal press 
<kbd>Ctrl</kbd> + <kbd>C</kbd>

  ******************************************************************************
## RESET "WORDCLOUD powered by VA-PEPR" IMAGE
 
In dataplicity type:
```
su wordcloud
(enter password - wordcloud)
cd home/wordcloud/WordCloud
sudo python3 dither-image-what.py --colour "red" --image "LoadScreen.png"
```
 
 CLEAR CONTENTS WITH:
```
truncate -s 0 content.txt
```

 ******************************************************************************

## WORDCLOUD CHARACTERISTICS CHANGES

In dataplicity type:
```
su wordcloud
(enter password - wordcloud)
sudo nano /home/wordcloud/WordCloud/WordCloudGenerator.py
```

Find the following section in the code to alter Wordcloud refresh rate, word length and word density.
```
    print("Generating wordcloud...")
    # create wordcloud using data
    wordcloud = WordCloud(
        background_color="white", height=300, width=400,
        include_numbers = True, min_word_length=5, # minimum length of word
        max_words = 15, margin = 4 # margin between words
    ).generate(data)
```
    
To alter the E-Ink refresh rate edit:
```
        time.sleep(1800)
```

Now press the following keys to save and exit the editor   
```
Control + o
Enter
Control + x
```

