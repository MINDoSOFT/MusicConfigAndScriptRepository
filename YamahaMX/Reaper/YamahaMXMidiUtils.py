import reapy
import mido

def initialise_yamaha_mx():

    inputNames = mido.get_input_names()

    portPrefix = 'Yamaha MX Series-1'

    yamahaMXInputNames = [
        inputName for inputName in inputNames if inputName.startswith(portPrefix)]

    outputNames = mido.get_output_names()

    yamahaMXOutputNames = [
        outputName for outputName in outputNames if outputName.startswith(portPrefix)]

    # reapy.show_console_message(outputNames)

    # reapy.show_console_message(yamahaMXInputNames)

    if len(yamahaMXInputNames) != 1:
        print('More than one ' + portPrefix + ' input ports found. ')
        print(*yamahaMXInputNames, sep='\n')
        return None

    if len(yamahaMXOutputNames) != 1:
        print('More than one ' + portPrefix + ' output ports found. ')
        print(*yamahaMXOutputNames, sep='\n')
        return None

    inport = mido.open_input(yamahaMXInputNames[0])
    outport = mido.open_output(yamahaMXOutputNames[0])

    return [inport, outport]

def close_port(port):
    port.close()

def get_voice(inPort, outPort, voiceIndex):
    parameterRequestPrefix = 'F0 43 31 7F 17 37 '
    parameterRequestSuffix = ' F7'
    msb = '01'
    lsb = '02'
    programNumber = '03'

    sysexLamba = filter(lambda msg: msg.type in 'sysex', inPort)

    print('Getting information for voice ' + str(voiceIndex))
    voiceString = '{:02x}'.format(voiceIndex)
    msbOutMessage = mido.Message.from_hex(
        parameterRequestPrefix + voiceString + msb + parameterRequestSuffix)
    # print(msbOutMessage.hex())
    outPort.send(msbOutMessage)
    for msg in sysexLamba:
        msbInMessage = msg
        break

    # print(msbInMessage.data)
    msbValue = msbInMessage.data[7]
    print(msbValue)

    lsbOutMessage = mido.Message.from_hex(
        parameterRequestPrefix + voiceString + lsb + parameterRequestSuffix)
    # print(lsbOutMessage.hex())
    outPort.send(lsbOutMessage)
    for msg in sysexLamba:
        lsbInMessage = msg
        break

    # print(lsbInMessage.data)
    lsbValue = lsbInMessage.data[7]
    print(lsbValue)

    programNumberOutMessage = mido.Message.from_hex(
        parameterRequestPrefix + voiceString + programNumber + parameterRequestSuffix)
    # print(programNumberOutMessage.hex())
    outPort.send(programNumberOutMessage)
    for msg in sysexLamba:
        programNumberInMessage = msg
        break

    # print(programNumberInMessage.data)
    programNumberValue = programNumberInMessage.data[7]
    print(programNumberValue)

    voiceDict = {}

    voiceDict['msb'] = msbValue
    voiceDict['lsb'] = lsbValue
    voiceDict['programNumber'] = programNumberValue

    return voiceDict
