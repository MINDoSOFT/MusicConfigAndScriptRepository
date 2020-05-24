local info = debug.getinfo(1,'S');
reaper.ShowConsoleMsg("\nRunning: " .. info.source);

local project = 0; -- Active project

local trackCount = reaper.CountTracks(project);

--reaper.ShowConsoleMsg(trackCount);

local step = 1;
local voicesLoaded = 0;

for trackIndex = 0, trackCount - 1, step 
do
  local mediaTrack = reaper.GetTrack(project, trackIndex);
  --reaper.ShowConsoleMsg("\n" .. trackIndex);
  local trackName;
  retVal, trackName = reaper.GetTrackName(mediaTrack);
  --reaper.ShowConsoleMsg("\n" .. trackName);
  
  local fxCount = reaper.TrackFX_GetCount(mediaTrack);
  for fxIndex = 0, fxCount - 1, step
  do
    fxGUID = reaper.TrackFX_GetFXGUID(mediaTrack, fxIndex);
    --reaper.ShowConsoleMsg("\n" .. fxGUID);
    local fxName = "";
    retval, fxName = reaper.TrackFX_GetFXName(mediaTrack, fxIndex, fxName);
    --reaper.ShowConsoleMsg("\n" .. fxName);

    if string.match(fxName, "ReaControlMIDI") then
      local paramCount = reaper.TrackFX_GetNumParams(mediaTrack, fxIndex)
      for paramIndex = 0, paramCount - 1, step
      do
        local paramName = "";
        retval, paramName = reaper.TrackFX_GetParamName(mediaTrack, fxIndex, paramIndex, paramName);
        --reaper.ShowConsoleMsg("\n" .. paramName);
        if (paramName == "Bank/Program En") then
          intFalse = 0;
          intTrue = 1;
          -- Loads the program changes on the MIDI device
          reaper.TrackFX_SetParam(mediaTrack, fxIndex, paramIndex, intFalse);
          reaper.TrackFX_SetParam(mediaTrack, fxIndex, paramIndex, intTrue);

          voicesLoaded = voicesLoaded + 1;
          --reaper.TrackFX_SetParam(mediaTrack, fxIndex, paramIndex, value)
          --local retval, minval, maxval = reaper.TrackFX_GetParam(mediaTrack, fxIndex, paramIndex);
          --reaper.ShowConsoleMsg("\n" .. retVal .. "min" .. minval .. "max" .. maxval);
          --reaper.ShowConsoleMsg("\nretVal: " .. (retVal and 'true' or 'false'));
        end
      end
    end
  end
end

reaper.ShowConsoleMsg("\nLoaded " .. voicesLoaded .. " voices.");