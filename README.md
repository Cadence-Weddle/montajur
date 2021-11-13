# montajur
A python/ffmpeg based tool for creating montages/slideshows
Requires ffmpeg to be installed. 


`python montajur.py IMAGE_DIRECTORY -o OUTFILE="o.mp4" -d DURATION -t SPECIAL_PHOTOS -s RATIO=1.5 -a AUDIO_STREAMS -l LOG=FALSE -r RESOLUTION=1920,1080 -v OVERWRITE=TRUE`

IMAGE_DIRECTORY   :The location of the images to be stiched together. They will be put in alphanumeric order (special characters, 0-9, aA-zZ). Images of any size work; they will be rescaled and centered if they don't match the output video resolution (though height/width will be preserved). 

`-o OUTFILE`        :The destination file. The format is inferred from the extension. Defaults to "o.mp4"

`-d DURATION`       :The duration in seconds of the output file. Seconds / Image will be inferred. 

`-t SPECIAL_PHOTOS` :(Optional) a filename containing a '\n' seperated list of characters. Images whose filename contain any of these sets of characters will be shown for an 
extended duration.  

`-s RATIO`          :Ratio of [DUration of Special Photo]/[Duration of Normal Photo] defaults to 1.5.

`-a AUDIO_STREAMS`  :File which contains a list of audio files to added to the slideshow. 

`-r RESOLUTION`     :output resolution in the format WIDTHxHEIGHT. Defaults to 1920x1080. 

`-l`                :show ffmpeg logs

`-v`                :Overwrite OUTFILE if it already exists, otherwise exit. 

