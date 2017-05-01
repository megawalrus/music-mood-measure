# Music Mood Measure v1.0
## Allows a user to provide continuous arousal and valence ratings, corresponding to a piece of music

* This application is intended primarily for use in experimental research, investigating music and emotion. The purpose is to collect continuous ratings of either perceived or felt emotion, whilst a piece of music is played simultaneously.
* Launch 'RUN.py' to run the application. When prompted, enter a participant ID - this can contain any alphanumeric characters.
* NOTE: Entering 0 will cause the application not to log data.
* The main interface will now open. Drag and drop the ball to any position in arousal-valence space.
* Once done, simply close the window, and the data will be saved automatically. Data are stored in a CSV file in the 'Data' directory.
* To take a continuous mood rating without playing any sound, use 'RUN_NO_SOUND.py' instead. To take a single 'snapshot' measure of mood (also without sound), use 'RUN_SNAPSHOT.py'.

# DEPENDENCIES

* Python 2.7
* pygame 1.9
