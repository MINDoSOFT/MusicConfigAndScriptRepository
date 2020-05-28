import reapy
import YamahaMXMidiUtils
import YamahaMXReaperUtils

#reapy.show_console_message('Test')
#reapy.show_console_message(reapy.get_reaper_version())

inOutPorts = YamahaMXMidiUtils.initialise_yamaha_mx()

if inOutPorts == None:
    reapy.show_console_message('Could not open the YamahaMX ports.')
    quit()

inPort = inOutPorts[0]
outPort = inOutPorts[1]

voiceIndex = 0
voiceDict = YamahaMXMidiUtils.get_voice(inPort, outPort, voiceIndex)

if voiceDict == None or voiceDict == {}:
    reapy.show_console_message('Could not retrieve voice from YamahaMX.')
    quit()

project = reapy.Project()
# print(project)

if (project.n_selected_tracks != 1):
    reapy.show_console_message('Only one track must be selected to load voice from YamahaMX.')
    quit()

YamahaMXReaperUtils.set_reacontrol_midi_for_track(project.selected_tracks[0], voiceDict)

YamahaMXMidiUtils.close_port(inPort)
YamahaMXMidiUtils.close_port(outPort)
