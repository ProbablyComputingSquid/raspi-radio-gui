# raspi "radio"
[![Athena Award Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Faward.athena.hackclub.com%2Fapi%2Fbadge)](https://award.athena.hackclub.com?utm_source=readme)

This is a simple GUI made with PyQT to play music on a Raspberry Pi, almost like a radio. I couldn't quite get the interfaces with PiFMRds to quite work, because it required some weird loopback crap to be going on, so i decided to make it more of a music player than a radio. In the near future when I have more time I'll try to add a section where you can easily broadcast on fm frequencies, but for now I decided to just make an intergration with yt-dlp so you can rip music and playlists from youtube, soundcloud, bandcamp and [so much more](assets/supported_sites.txt)!

## Features
- Simple GUI made with PyQT
- Play music from local files
- Download and play music from youtube, soundcloud, bandcamp and more using yt-dlp
- Simple playlist management which saves music to a .playlist file
- metadata extraction n stuff to display music title, album cover, and artist.


requirements: 
- python3
- pip
- pyqt (5 or 6 should work)
- all these should be downloadable from the requirements.txt just run `pip install -r requirements.txt`

## installation and troubleshooting
if your the executable is not working make sure to download all the requisite modules with pip first!! there can be some errors regarding that 

    What your project is/does (and what it's called)
    Why you made your project
    How you made your project
    What you struggled with and what you learned

