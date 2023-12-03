import pyautogui as gui, time
# import main
import sys
import os

# game_over = 'False'

pid = os.getpid()

print('PID: ',pid)
def game_check():
    from main import game_over
    # print(game_over)   
    if game_over == 'True':
        print('OVERRR')
        time.sleep(1)
        sys.exit(0)

# main.test_run()

screenWidth, screenHeight = gui.size()

def test_gui():
    print(pid)
    # Scene 1
    gui.moveTo(482,722)
    gui.click(482,722)

    time.sleep(1)
    gui.press('enter')
    gui.press('enter')
    game_check()

def identifyloc():
    while True:
        currentMouseX, currentMouseY = gui.position()
        print(currentMouseX,currentMouseY)
        time.sleep(3)


# identifyloc()

if __name__ == '__main__':
    gui.moveTo(488,722)
    gui.click(488,722)

    time.sleep(1)



    # Scene 2
    test_gui()

    # Scene 3
    test_gui()

    # Scene 4
    test_gui()

    # Scene 5
    test_gui()

    # Scene 6
    test_gui()

    # Scene 7
    test_gui()

    # Scene 8
    test_gui()

    # Scene 9
    test_gui()




