# raspberry "radio" 
[![Athena Award Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Faward.athena.hackclub.com%2Fapi%2Fbadge)](https://award.athena.hackclub.com?utm_source=readme)

This is a simple music player made with PyQT to play music on a Raspberry Pi, almost like a radio. **This works perfectly on your computer too!** I couldn't quite get the interfaces with PiFMRds to quite work, because it required some weird loopback crap to be going on, so i decided to make it more of a music player than a radio. In the near future when I have more time I'll try to add a section where you can easily broadcast on fm frequencies, but for now I decided to just make an intergration with yt-dlp so you can rip music and playlists from youtube, soundcloud, bandcamp and [so much more](assets/supported_sites.txt)!

## Features
- Simple GUI made with PyQT
- Play music from local files
- Download and play music from youtube, soundcloud, bandcamp and more using yt-dlp
- Simple playlist management which saves music to a .playlist file
- metadata extraction n stuff to display music title, album cover, and artist.

## installation:
head over to the releases tab and check out the latest release, download the executable and run it! it should work on most OSes, but i've only tested it on my arch install. 


requirements: 
- python3
- pip
- pyqt (5 or 6 should work)
- all these should be downloadable from the requirements.txt just run `pip install -r requirements.txt`


I originally made this project because I want a better interface for playing music on my raspberry pi home radio station rather than manually writing out bash scripts to play folders of music. Along the way, I decided that it would be a great idea to allow people to download their favorite songs and playlists off other music streaming websites

This project was written in pure python using the PyQT framework for the GUI. i used pygame (honestly a bad idea, i might rewrite to lessen code bloat) for audio playback which was a BAD idea in retrospect but its un poco too late to change it. Perchance i will change it later along the line. 

I struggled a lot with the PyQT framework, as I had never used it before. I also had a lot of problem working with yt-dlp because i was originanlly using a deprecated old branch of yt-dlp, youtube-dl but yt-dlp made it easier. Then i had to learn some basic threading stuff so downloads wouldn't block the executor and make it look like the program crashed. 

## installation and troubleshooting
if your the executable is not working make sure to download all the requisite modules with pip first!! there can be some errors regarding that 

    What your project is/does (and what it's called)
    Why you made your project
    How you made your project
    What you struggled with and what you learned

