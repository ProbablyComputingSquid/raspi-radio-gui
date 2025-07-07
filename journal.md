# 10:17 am 21/06/25

trying to get things set up on the raspi

10:25 am: imaging the usb drive lol, accidentally deleted it with arch :despair:

10:43 am: setup pi, doing ssh now

# 24/06/25 17:46
looking around for vocaloid stuff, thinking about using coqui tts for the voice. what i was thinking is that you would write in a script for the radio, and then it would "speak" it out using the tts with the user's voice.<br>
so basically it would be like a fake radio host. It would do something like, "the next song playing is [song name] by [artist name]" <br>
i was thinking that it would be cool to have a "radio host" that would talk about the songs and stuff, like a real radio station. <br>
maybe it would be cool to have a daily new summary or something, where it would fetch headline articles from the news or an RSS feed and then talk about them. <br>
I know AI is cringe and bad, but it would be cool to have a radio station where you would train an AI to talk like you and then it would talk about things from your perspective. <br>
honestly thats kinda weird and a waste of resources and time, but it would be cool. just as like a fun thing yk. or you could just be normal and right blurbs for the tts to read <br> 
18:01: okay so apparently the openai's whisper model has a broken release on pypi so have to build it from the github :sob:
gonna try to record the phonemes.txt paragraph now and see if it works
todo: `pip install audioop-lts`
done ^^
okay now its 9:27 pm, went fishing and grandfather got injured so its coding time<br>
researching methods for extracting phonemes from audio, found "montreal forced aligner". it uses a lot of big fancy words that I dont know. 

bahh installing conda for mfa. why does montreal forced alignment have same abbreviation as multifactor authentication...
its 9:31 now, installing mfa...
9:43 installation dependency hell, i cannot install pytorch with conda