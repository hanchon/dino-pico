import random
import time

from machine import Pin, PWM
from lcd import BL, LCD_1inch14
from sprite import Dino, Tree, render, check_collision
from controller import button_pressed

max_score = 0

def run_game():
    global max_score

    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(8192) #max 65535

    LCD = LCD_1inch14()
    LCD.fill(LCD.white)
    LCD.show()

    now = time.ticks_ms()
    dino = Dino(25)
    dino.do_update(now)

    i = 0
    obstacles = []
    end = 250
    while i <  6:
        cactus = Tree(end, now)
        obstacles.append(cactus)
        end = int(end + 75 + 20 * random.random())
        i = i + 1


    score = 0
    playing = True

    while playing:
        now = time.ticks_ms()

        jump = button_pressed()
        if jump:
            if dino.can_jump():
                dino.jump()

        LCD.fill(LCD.white)
        if max_score < score * 100:
            max_score = score * 100

        LCD.text("Max score: "+str(max_score), 10, 10, LCD.blue)
        LCD.text("Score: "+str(score*100), 10, 20, LCD.green)

        offset = None
        i = 0
        for element in obstacles:
            # If tree behing the dino, send it to the back and score++
            if element.sprite.x < 10:
                if offset is None:
                    offset = obstacles[i-1].sprite.x
                offset = int(offset + 100 + 30 * random.random())
                element.sprite.x = offset
                score = score + 1

            i = i + 1
            element.do_update(now)
            # Render the tree
            render(LCD, element)

        # Render the dino
        dino.do_update(now)
        render(LCD, dino)

        # Check for gameover
        if check_collision(dino, obstacles):
            LCD.text("GAMEOVER. SCORE: "+str(score*100), 20, 60, LCD.red)
            LCD.text("PRESS ANY KEY TO RESTART", 20, 68, LCD.red)
            playing = False

        LCD.show()
    time.sleep(1)

if __name__=='__main__':
    while 1:
        waiting = True
        while waiting:
            jump = button_pressed()
            if jump:
                waiting = False
                break
        run_game()


