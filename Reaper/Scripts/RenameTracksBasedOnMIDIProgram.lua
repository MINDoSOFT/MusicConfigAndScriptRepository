-- This script loops through all the tracks, and tries to find the ReaControlMIDI fx.
-- If it does find it, then it picks up the formatted program parameter (e.g. "2 APno: Glasgow"),
-- and renames the track using that parameter.

-- Remember to load a Reabank in the ReaControlMIDI fx Bank/Program Select section to get meaningful
-- names for your hardware device. You can find various Reabank files online.

local info = debug.getinfo(1,'S');
reaper.ShowConsoleMsg("\nRunning: " .. info.source);

local project = 0; -- Active project

local trackCount = reaper.CountTracks(project);

--reaper.ShowConsoleMsg(trackCount);

local step = 1;
local tracksRenamed = 0;
local showReabankMessage = false;

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
        if (paramName == "Program") then
          local formattedParamValue = "";
          local retval, formattedParamValue = reaper.TrackFX_GetFormattedParamValue(mediaTrack, fxIndex, paramIndex, formattedParamValue);
          --reaper.ShowConsoleMsg("\n" .. formattedParamValue);
          if (formattedParamValue ~= "" and formattedParamValue ~= "0") then
            local retval, trackName = reaper.GetSetMediaTrackInfo_String(mediaTrack, "P_NAME", formattedParamValue, true);
            tracksRenamed = tracksRenamed + 1;
          else
            showReabankMessage = true;
          end
        end
      end
    end
  end
end

if (showReabankMessage) then
    reaper.ShowConsoleMsg("\nWarning:");
    reaper.ShowConsoleMsg("\nSome program names were missing.");
    reaper.ShowConsoleMsg("\nHave you properly loaded Reabank in the ReaControlMIDI fx ?");
end

reaper.ShowConsoleMsg("\nRenamed " .. tracksRenamed .. " tracks.");
reaper.ShowConsoleMsg("\nFinished running: " .. info.source);
