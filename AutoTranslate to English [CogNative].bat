rem echo "%~1" gives original file
rem echo "%~d1%~p1%~n1Translated%~x1" gives file with "Translated" appended to name in same location
python -m CogNative.main -sampleAudio "%~1" -synType audio -dialogueAudio "%~1" -out "%~d1%~p1%~n1_English.wav" -useExistingEmbed y -destLang english