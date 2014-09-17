from __future__ import print_function
import time
import winsound

def play():
    print('Kill audiodg.exe process to stop music.')
    # winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
    # winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
    # winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
    # winsound.PlaySound('SystemHand', winsound.SND_ALIAS)
    # winsound.PlaySound('SystemQuestion', winsound.SND_ALIAS)
    # winsound.PlaySound('ALARM8', winsound.SND_ASYNC)
    winsound.PlaySound('c:/SleepAway.wav',winsound.SND_FILENAME)
    # while(True):
    #     time.sleep(0.2)
    #     print("s"),
    # hi=raw_input('Press any key to stop music......')
    # winsound.PlaySound('c:/SleepAway_clip.wav',winsound.SND_PURGE)
    
if __name__ == '__main__':

    play()
