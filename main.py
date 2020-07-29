import pyfirmata
import time
from pynput.keyboard import Key, Controller
keyboard = Controller()

# Morse code table
MORSE_CODE_DICT = {
    '.-': 'A',   '-...': 'B',   '-.-.': 'C',
    '-..': 'D',      '.': 'E',   '..-.': 'F',
    '-.': 'G',   '....': 'H',     '..': 'I',  
    '.---': 'J',    '-.-': 'K',   '.-..': 'L',
    '--': 'M',     '-.': 'N',    '---': 'O', 
    '.--.': 'P',   '--.-': 'Q',    '.-.': 'R',
    '...': 'S',      '-': 'T',    '..-': 'U', 
    '...-': 'V',    '.--': 'W',   '-..-': 'X',
    '-.--': 'Y',   '--..': 'Z',  '-----': '0', 
    '.----': '1',  '..---': '2',  '...--': '3',
    '....-': '4',  '.....': '5',  '-....': '6', 
    '--...': '7',  '---..': '8',  '----.': '9'
}

board = pyfirmata.Arduino('/dev/tty.usbmodem14101')

it = pyfirmata.util.Iterator(board)
it.start()

board.digital[2].mode = pyfirmata.INPUT

buttonUp            = False
startedMorseBuffer  = False
lastButtonDelay     = 0
timeButtonDownFor   = 0
timeButtonUpFor     = 0

morseBuffer = ''

print('Started loop')
interval = 1/20
while True:
    lastButtonDelay += interval
    if not buttonUp:
        timeButtonDownFor += interval
    else:
        timeButtonUpFor += interval

    isButtonPushed = not board.digital[2].read()
    if (timeButtonUpFor > 1 and startedMorseBuffer):
        codeValid = False
        for testCode in MORSE_CODE_DICT.keys():
            if morseBuffer == testCode:
                codeValid = True
                break

        if codeValid:
            c = MORSE_CODE_DICT[morseBuffer]
            print(f'Buffer {morseBuffer} | character {c}')
            keyboard.press(c)
            keyboard.release(c)
        else:
            print(f'{morseBuffer} invalid code')

        startedMorseBuffer = False
        morseBuffer = ''
        lastButtonDelay = 0
        timeButtonDownFor = 0

    if not isButtonPushed:
        if not buttonUp:
            if not startedMorseBuffer:
                startedMorseBuffer = True
                lastButtonDelay = 0
            else:
                morseBuffer += '-' if lastButtonDelay >= 0.4 else '.'

                print(f'Pushed button! Button delay {morseBuffer}')
                lastButtonDelay = 0
                canButtonBePushed = False
                timeButtonDownFor = 0
            timeButtonUpFor = 0
        buttonUp = True
    else:
        buttonUp = False
        

    time.sleep(interval)