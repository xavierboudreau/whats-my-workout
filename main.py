
import os
import sched
import time

workout = ['Leg raise clap', 'Reverse Crunch', \
            'Spider man plank', 'Cross body mountain climbers', \
            'Russian Twist', 'In and Out', \
            'Plank with hip twist', 'Plank Jacks', \
            'One hundreds', 'Crunch', \
            'Up and down plank', 'Plank', \
            'Penguins' , 'Bicycles', \
            'Reverse crunch leg extension' , 'Straight leg crunch', \
            'Up and down plank']

LOADTIME = 2
WAITTIME = 10
DEFAULT_PRIORITY = 1
NO_OP = ()
EXERCISE_LENGTH = 30
BREAK_LENGTH = 10

'''
May fail if text contains escape characters or certain non-alphanumeric characters
'''
def say(*text, speaker = 'Samantha'):
    # there is a strange bug where text is a tuple of characters instead of a str
    text = ''.join(text)
    os.system('say -v {} {}'.format(speaker, text))

def announce_break(currTime, warning_length = 15):
    currTime += (EXERCISE_LENGTH-warning_length)
    s.enterabs(currTime, DEFAULT_PRIORITY, say, ('{} seconds left, then a 10 second break'.format(warning_length)))

def announce_exercise(currTime, exercise_name, warning_length = 15):
    currTime += (EXERCISE_LENGTH-warning_length)
    s.enterabs(currTime, DEFAULT_PRIORITY, say, ('{} seconds left, then {}'.format(warning_length, exercise_name)))


if __name__ == '__main__':
    s = sched.scheduler(time.time, time.sleep)
    epoch = time.time() + LOADTIME
    currTime = epoch
    s.enterabs(currTime, DEFAULT_PRIORITY, say, ('workout starts in {} seconds'.format(WAITTIME)))
    currTime += WAITTIME

    for i in range(0, len(workout)-1, 2):
        s.enterabs(currTime, DEFAULT_PRIORITY, say, (workout[i]))
        announce_exercise(currTime, workout[i+1])
        currTime += EXERCISE_LENGTH
        s.enterabs(currTime, DEFAULT_PRIORITY, say, (workout[i+1]))
        announce_break(currTime)
        currTime += EXERCISE_LENGTH
        s.enterabs(currTime, DEFAULT_PRIORITY, say, ('10 second break, get ready for {}'.format(workout[i+2])))
        currTime += BREAK_LENGTH

    # Last exercise is standalone
    s.enterabs(currTime, DEFAULT_PRIORITY, say, ('{}, this is the last exercise'.format(workout[-1])))
    announce_exercise(currTime, 'we are done')
    currTime += EXERCISE_LENGTH
    s.enterabs(currTime, DEFAULT_PRIORITY, say, ('We are done. Great workout'))

    s.run()
