# Description

This script allows you to load the first voice on the Yamaha MX
midi program information, into a ReaControlMIDI effect
in Reaper's selected track. It also renames the track
and if you have a Reabank loaded i.e. https://stash.reaper.fm/v/32408/Yamaha_MX49.reabank
you get a meaningful name. 

Please use the reaper project template provided, with midi routing already set.


# Installation

To run this script you first need to install Python.

It has been tested with Python 3.7.4

Then launch a terminal and run "pip install -r requirements.txt"

You also need to enable reapy distant api, see this page for details 
https://python-reapy.readthedocs.io/en/latest/install_guide.html#get-configuration-infos

Reaper version that I tested this is v6.11

Please go ahead and install also the Reaper Yamaha MX keymap from
https://panos.dukes.gr/cms/reaper-and-mx/
it will make your life easier and your workflow faster. 
You will be able to click DAW Remote and control Reaper from the Yamaha MX.


# Running

This script can only be run from an external terminal. Not from inside Reaper.
I faced an issue with RtMidi library being reimported, and I switched 
to using the script from outside Reaper.

1. Find the voice you like on the Yamaha MX.
2. Select the track in Reaper that you want to load the voice midi program information.
3. Launch a terminal and go to the location that you downloaded the scripts.
4. Run "python YamahaMXReaperLoadFirstVoiceOnTrack.py"

Note: Avoid selecting the first track, because the first voice is used as a buffer,
in order for you to be able to preview the sound when selecting a voice.

Note: Remember to disable the Local Control from Utility->Midi menu on the Yamaha MX.


# Credits

Hope you enjoy this script.

Created by MINDoSOFT on 29/05/2020
