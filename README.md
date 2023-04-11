# rehersal\_export

This is a Python script that I use for exporting rehersal-recordings over to my band's
Nextcloud storage.

  1. It scans an Ardour session/project folder for recordings
  1. For each "take" it finds, it creates a mix where the first two "Audio N" files are
     left- and right-drum channels.
  1. It then overlays/mixes the rest of the files for each
     take on top of the now-stereo drum-track.
  1. Exports the mixed audio to an appropriate folder within Nextcloud as mp4/m4a.
  1. Encodes and exports ALL the audio-files for the session/project as mp4/m4a to the
     Nextcloud folder.
  1. Profit.

