from epics import caput, caget
from time import sleep

def playalarm():
  caput('norum:asyn.AOUT', '@MAIN:INP=SERVER')
  sleep(1.5)
  caput('norum:asyn.AOUT', '@SERVER:PLAYBACKINFO=?')
  sleep(0.3)
  response = caget('norum:asyn.AINP')
  if response != '@SERVER:PLAYBACKINFO=Stop':
    caput('norum:asyn.AOUT', '@SERVER:PLAYBACK=Stop')
  sleep(0.3)
  caput('norum:asyn.AOUT', '@SERVER:LISTCURSOR=Return to Home')
  sleep(0.3)
  caput('norum:asyn.AOUT', '@SERVER:LISTCURSOR=Down')
  sleep(0.3)
  playing = 0
  while playing==0:
    caput('norum:asyn.AOUT', '@SERVER:LISTCURSOR=Sel')
    sleep(0.3)
    response = caget('norum:asyn.AINP')
    print response
    if response=='@SERVER:PLAYBACKINFO=Play':
      playing=1

  sleep(10)
  caput('norum:asyn.AOUT', '@SERVER:PLAYBACK=Stop')
  caput('norum:asyn.AOUT', '@MAIN:INP=HDMI1')
  

playalarm()
