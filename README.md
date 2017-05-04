# Music Mood Measure v1.0
## Allows a user to provide continuous arousal and valence ratings, corresponding to a piece of music

* This application is intended primarily for use in experimental research, investigating music and emotion. The purpose is to collect continuous ratings of either perceived or felt emotion, whilst a piece of music is played simultaneously.
* Launch `RUN.py` to run the application. When prompted, enter a participant ID - this can contain any alphanumeric characters. **NOTE:** Entering 0 will cause the application not to log data.
* A dialog box will open, allowing a sound file to be selected (supported formats: WAV, MP3, OGG). For convenience, demo music (non-copyrighted) is included in the 'Resources' directory
* Once a sound file is chosen, the main interface will now open. The user can drag and drop the ball to any position in arousal-valence space, in order to register their current emotional response.
* Once done, simply close the window, and the data will be saved automatically. Data are stored in a CSV file in the 'Data' directory. By default, arousal and valence ratings are saved 10 times per second.
* To take a continuous mood rating without playing any sound, use 'RUN_NO_SOUND.py' instead. To take a single 'snapshot' measure of mood (also without sound), use 'RUN_SNAPSHOT.py'.
* Example instructions ('PARTICIPANT_INSTRUCTIONS.docx') are included, featuring a screenshot of the application. Obviously, these might need to be adapted depending on what the particular experiment involves.
* Further instructions for experimenters are also included ('EXPERIMENTER_INSTRUCTIONS.pdf').

# DEPENDENCIES

* Python 2.7
* pygame 1.9
