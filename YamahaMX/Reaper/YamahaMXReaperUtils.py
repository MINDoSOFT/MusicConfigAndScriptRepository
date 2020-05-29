import reapy

def set_reacontrol_midi_for_track(track, voiceDict):
    print(track.name)
    #print(voiceDict)
    valueRange = 127

    #print(track.fxs)
    for fx in track.fxs:
        #print(fx.name)
        if 'ReaControlMIDI' in fx.name:
            normaliseMSB = float(voiceDict['msb']) / valueRange
            normaliseLSB = float(voiceDict['lsb']) / valueRange
            normaliseProgram = float(voiceDict['programNumber']) / valueRange

            fx.params['Bank/Program En'] = True # Otherwise the parameters are read only
            fx.params['Bank MSB'] = normaliseMSB
            fx.params['Bank LSB'] = normaliseLSB
            fx.params['Program'] = normaliseProgram

            #for param in fx.params:
            #    print(param.name)

            print('Loaded voice ' + fx.params['Program'].formatted)
            renameTrack = False
            if track.name != '' and track.name != get_default_track_name(track):
                text = "Overwrite track '" + track.name + "' name ?"
                title = "YamahaMXReaperUtils"
                type = "yes-no-cancel"
                messageBoxResult = reapy.show_message_box(text, title, type)
                if messageBoxResult == "yes":
                    renameTrack = True
            else:
                renameTrack = True

            if renameTrack:
                track.name = fx.params['Program'].formatted

    pass

def get_default_track_name(track):
    return 'Track ' + str(track.index + 1)