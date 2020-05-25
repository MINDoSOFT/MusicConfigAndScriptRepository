import mido
import json

inputNames = mido.get_input_names()

portPrefix = 'Yamaha MX Series-1'

yamahaMXInputNames = [inputName for inputName in inputNames if inputName.startswith(portPrefix)]

outputNames = mido.get_output_names()

yamahaMXOutputNames = [outputName for outputName in outputNames if outputName.startswith(portPrefix)]

# print(outputNames)

# print(yamahaMXInputNames)

if len(yamahaMXInputNames) != 1:
    print('More than one ' + portPrefix + ' input ports found. ')
    print(*yamahaMXInputNames, sep='\n')
    quit()

if len(yamahaMXOutputNames) != 1:
    print('More than one ' + portPrefix + ' output ports found. ')
    print(*yamahaMXOutputNames, sep='\n')
    quit()

inport = mido.open_input(yamahaMXInputNames[0])
outport = mido.open_output(yamahaMXOutputNames[0])

voices = 16
voiceIndexes = range(0, voices);

performances = 128
performanceIndexes = range(0, performances);

#print(*voiceIndexes)

#testMsg = mido.Message('sysex', data=bytearray(b'\x43317F17370203')) # Parameter request
#testMsg = mido.Message.from_hex('F0 43 31 7F 17 37 02 03 F7') # Parameter request WORKS
#Will receive sysex data=(67,17,127,23,55,2,3,124) time=0

#testMsg = mido.Message('sysex', data=bytearray(b'43217F17370100'))  # Request Bulk

#testMsg = mido.Message('note_on', note=100, velocity=127, time=6.2) # Works

#with mido.open_input(yamahaMXInputNames[0]) as inport:
#    for message in inport:
#        print(message)

#print(testMsg.hex())

#msg = inport.receive()
#outport.send(testMsg)

#msg = inport.receive()
#print(msg.type)
#print(msg)

parameterRequestPrefix = 'F0 43 31 7F 17 37 '
parameterRequestSuffix = ' F7'
msb = '01'
lsb = '02'
programNumber = '03'

sysexLamba = filter(lambda msg: msg.type in 'sysex', inport)

msbInMessage = ""
lsbInMessage = ""
programNumberInMessage = ""

performanceChannel = 0
performanceMSBCC = 0
performanceMSBValue = 63
performanceLSBCC = 32
performanceLSBValue = 80

performancesKey = 'performances'
performanceIndexKey = 'performanceIndex'
performanceVoicesKey = 'performanceVoices'
performanceVoicesDict = { performancesKey : [] }

for performanceIndex in performanceIndexes:
    print('Getting information for performance ' + str(performanceIndex))
    msbCC = mido.Message('control_change', channel=performanceChannel, control=performanceMSBCC, value=performanceMSBValue)
    #print(msbCC.hex())
    outport.send(msbCC)
    lsbCC = mido.Message('control_change', channel=performanceChannel, control=performanceLSBCC, value=performanceLSBValue)
    #print(lsbCC.hex())
    outport.send(lsbCC)
    programChange = mido.Message('program_change', channel=performanceChannel, program=performanceIndex)
    #print(programChange.hex())
    outport.send(programChange)
    #control_change
    #0: B0 00 3F [CC0 Bank Select MSB] chan 1 val 63
    #1: B0 20 50 [CC32 Bank Select LSB] chan 1 val 80
    #program_change
    #2: C0 01 00 [Program Change] chan 1 val 1

    # Give the device some time to change ?

    for voiceIndex in voiceIndexes:
        print('Getting information for voice ' + str(voiceIndex))
        voiceString = '{:02x}'.format(voiceIndex)
        msbOutMessage = mido.Message.from_hex(parameterRequestPrefix + voiceString + msb + parameterRequestSuffix)
        #print(msbOutMessage.hex())
        outport.send(msbOutMessage)
        for msg in sysexLamba:
            msbInMessage = msg
            break

        #print(msbInMessage.data)
        msbValue = msbInMessage.data[7]
        print(msbValue)

        lsbOutMessage = mido.Message.from_hex(parameterRequestPrefix + voiceString + lsb + parameterRequestSuffix)
        #print(lsbOutMessage.hex())
        outport.send(lsbOutMessage)
        for msg in sysexLamba:
            lsbInMessage = msg
            break

        #print(lsbInMessage.data)
        lsbValue = lsbInMessage.data[7]
        print(lsbValue)

        programNumberOutMessage = mido.Message.from_hex(parameterRequestPrefix + voiceString + programNumber + parameterRequestSuffix)
        #print(programNumberOutMessage.hex())
        outport.send(programNumberOutMessage)
        for msg in sysexLamba:
            programNumberInMessage = msg
            break

        #print(programNumberInMessage.data)
        programNumberValue = programNumberInMessage.data[7]
        print(programNumberValue)
        
        voiceDict = {}

        voiceDict['msb'] = msbValue
        voiceDict['lsb'] = lsbValue
        voiceDict['programNumber'] = programNumberValue

        if (len(performanceVoicesDict[performancesKey]) <= performanceIndex):
            initPerformanceDict = {performanceIndexKey : performanceIndex, performanceVoicesKey : []}
            performanceVoicesDict[performancesKey].append(initPerformanceDict)
        performanceDict = performanceVoicesDict[performancesKey][performanceIndex][performanceVoicesKey]

        performanceDict.append(voiceDict)

print(performanceVoicesDict)

with open("yamaha_mx_all_performance_voices.json", "w") as write_file:
    json.dump(performanceVoicesDict, write_file)

inport.close()
outport.close()