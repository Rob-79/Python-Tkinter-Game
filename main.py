import sys
import os
import random
import time
import tkinter
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk

import logging
import logging.handlers as handlers
from datetime import datetime

import subprocess as s

# from test import pid

import pygame

# test_pid = pid

def killProcess(pid):
    s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)


game_over = False

# Setting up Log file name
time = str(datetime.now())


str_file = datetime.now().strftime('mylogfile_%Y-%m-%d_%H-%M')


log_filename = "./Logs/" + str_file + ".log"

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, filename=log_filename, filemode="w",
                            format="%(asctime)s - %(levelname)s - %(message)s")



handler = logging.FileHandler(log_filename)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)



# Creating Player Class for Adventurer
class player:
    def __init__(self, location, health, items, score):
        self.location = location
        self.health = health
        self.items = items
        self.score = 0

hero = player("entry", 100, 0, 0)

class NotificationManager:
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []

    def show_notification(self, title, image_path, text):
        notification = NotificationWindow(self.parent, title, image_path, text, self.destroy_notification)
        self.notifications.append(notification)

    def destroy_notification(self, notification):
        self.notifications.remove(notification)
        notification.destroy_window()

class NotificationWindow:
    def __init__(self, parent, title, image_path, text, destroy_callback, duration=1000):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.title(title)

        image = Image.open(image_path)
        resized_image = image.resize((150, 100), Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(resized_image)

        label = Label(self.window, image=new_image)
        label.image = new_image  # To prevent garbage collection
        label.pack(pady=10)

        notification_label = Label(self.window, text=text)
        notification_label.pack(pady=10)

        # Schedule the destruction of the notification window after the specified duration
        self.window.after(duration, lambda: destroy_callback(self))

        ok_button = Button(self.window, text="OK", command=lambda: destroy_callback(self))
        ok_button.pack(pady=10)

        # Adjust the geometry of the notification window as needed
        self.window.geometry("300x200+350+250")  # Change the size and position

        

    def destroy_window(self):
        self.window.destroy()


class GUI:
    
    # Initialzing main window for GUI
    def __init__(self, window):
        self.window = window

        


        window.title("Adventure Game")

        window.geometry("966x745+0+0")
        window.minsize(width=966, height=850)
        window.maxsize(width=966, height=850)

        # Create a black bar at the top for displaying the score
        self.score_label = tkinter.Label(window, text="SCORE: 0", bg="black", fg="white", font=("Helvetica", 16))
        self.score_label.pack(fill="x")

        frame = Frame(window)
        frame.pack(expand=True, fill="both", anchor=tkinter.CENTER)

        
        print("Medkits", hero.items)


        # Getting and setting up image
        
        self.img = ImageTk.PhotoImage(Image.open("start.png"))

        # Loading Background Image
        self.label = tkinter.Label(frame, image=self.img)
        self.label.pack()

        # Setting Basic buttons and Labels
        self.l1 = tkinter.Label(frame, text="WELCOME TO OUR ADVERNTURE GAME")
        self.l1.pack()

        health_text = "HEALTH = " + str(hero.health)

        self.l2 = tkinter.Label(frame, text=health_text, bg="Black", fg="White")
        self.l2.pack()

        medkit_text = "MEDKITS = " + str(hero.items)

        self.l3 = tkinter.Label(frame, text=medkit_text, bg="Black", fg="White")
        self.l3.pack()

        self.b1 = tkinter.Button(frame, width=15, height=3, text="START", command=self.Entry)
        self.b1.pack()

        self.yes_1 = tkinter.Button(frame, width=15, height=1, text="YES")
  

        self.no_1 = tkinter.Button(frame, width=15, height=1, text="NO")


        self.use_medkit = tkinter.Button(frame, width=15, height=1, text="USE MEDKIT")

        self.notification_manager = NotificationManager(window)

        # Initialize the level indicator
        self.level_indicator = ttk.Progressbar(frame, orient="horizontal", length=600, mode="determinate")
        

        # Add labels at the start and end
        self.start_label = tkinter.Label(frame, text="Start", font=("Helvetica", 10))
        

        self.end_label = tkinter.Label(frame, text="End", font=("Helvetica", 10))
        

        # Set the initial level
        self.current_level = 0
        self.max_level = 14
        self.update_level_indicator()

        # Initialize Pygame mixer for sound
        pygame.mixer.init()

        # Load and play background music in a loop
        pygame.mixer.music.load("SFX\PerituneMaterial_Foreboding(chosic.com).mp3")  # Replace with your music file
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def update_score_label(self):
        # Update the score label with the current score
        self.score_label["text"] = f"SCORE: {hero.score}"

    def update_level_indicator(self):
        # Update the level indicator based on the current level
        self.level_indicator["value"] = self.current_level
        self.level_indicator["maximum"] = 130  # Set the maximum value based on the total number of levels

    def change_level(self, increment):
        # Change the current level based on the increment
        self.current_level += increment
        self.update_level_indicator()



    # Function to make Medkit
    def medkit(self):
        medkit_find = random.choice([True, False])
        if medkit_find is True:

            self.notification_manager.show_notification("Medkit Notification", "Medkit.jpg", "Medkit Found")
            hero.score += 50
            self.update_score_label()

            hero.items += 1
            medkit_text = "MEDKITS = " + str(hero.items)
            self.l3.configure(text=medkit_text)

    # Function to allow use of Medkit
    def using_medkit(self):
        logging.info("Using MedKit")
        if hero.items >= 1:
            hero.health = 100
            health_text = "HEALTH = " + str(hero.health)

            hero.items -= 1

            hero.score += 30
            self.update_score_label()

            medkit_text = "MEDKITS = " + str(hero.items)
            self.l3.configure(text=medkit_text)
            self.l3.pack()

            self.l2.configure(text=health_text)

    # Function to handle Bat Attack
    def bat_attack(self):
        bat_attack = random.choice([True, False])
            
        if bat_attack:
            self.notification_manager.show_notification("Attack Notification", "bat.png", "Bat Attack!!")
            hero.health -= random.randint(1, 50)
            health_text = "HEALTH = " + str(hero.health)
            self.l2.configure(text=health_text)

            hero.score += 30
            self.update_score_label()

            # Killing the Game
            if hero.health <= 0:
                pygame.mixer.music.stop()
                # Load and play background music in a loop
                pygame.mixer.music.load ("SFX\mixkit-horror-lose-2028.wav")  # Replace with your music file
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                
                game_over = True
                print(game_over)
                
                logging.info("YOU DIED")
                tkinter.messagebox.showinfo( "Death", "You Died!!")
                self.window.destroy()

                os._exit(0)


    
    # Function to handle Bat Attack
    def snake_attack(self):
        snake_attack = random.choice([True, False])
            
        if snake_attack:
            self.notification_manager.show_notification("Attack Notification", "Snake.png", "Snake Attack!!")
            hero.health -= random.randint(1, 30)
            health_text = "HEALTH = " + str(hero.health)
            self.l2.configure(text=health_text)

            hero.score += 30
            self.update_score_label()

            # Killing the Game
            if hero.health <= 0:
                pygame.mixer.music.stop()
                # Load and play background music in a loop
                pygame.mixer.music.load ("SFX\mixkit-horror-lose-2028.wav")  # Replace with your music file
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                
                game_over = True
                print(game_over)
                
                logging.info("YOU DIED")
                tkinter.messagebox.showinfo( "Death", "You Died!!")
                self.window.destroy()

                os._exit(0)


    

    # Creating Button function
    def create_btn(self, str, cmd):
        btn = self.tkinter.Button(self.frame, width=15, height=1, text=str, command=cmd)
        return btn


    # Clearin Frame of all widgets
    def clear_frame(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    # Function to change image
    def change_img(self,str):
        self.img2=ImageTk.PhotoImage(Image.open(str))
        self.label.configure(image=self.img2)
        self.label.image=self.img2



    # Starting of Game with 1st Stage
    def Entry(self):
        logging.info("Starting Game")
        self.change_img("Cave2.png")
        self.b1.destroy()
        
        self.yes_1.pack()
        self.no_1.pack()
        
        self.l2.pack()
        self.l1.config(text="You are in a dark cave. The entry has been sealed by fallen rocks. There is no way out. Ahead, you can see a door. Will you continue?")



        self.yes_1.configure(command=self.yes_kick)
        self.yes_1.pack()
        

        self.no_1.configure(command=self.no_kick)
        self.no_1.pack()

        self.use_medkit.configure(command=self.using_medkit)
        self.use_medkit.pack()

        self.level_indicator.pack(pady=10)
        self.start_label.pack(side="left", padx=80)
        self.end_label.pack(side="right", padx=80)

    # Level 2
    # Choosing option YES
    def yes_kick(self):
        logging.info("YES")
        print("Location", hero.location)
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("door.png")
        self.l1.config(text="Door is opened by kick. Contains fast wind. Hero crawls to groung and reach end. Will you crawl?")
        self.yes_1.configure(command=self.Forest)

        self.change_level(10)


        hero.score += 50
        self.update_score_label()

    # Choosing option NO
    def no_kick(self):
        logging.info("NO")
        self.change_img("bat.png")
        self.l1.config(text="A bat flies over your head and you hear screetches in the distance. You sit in total darkness wondering if there's a way out.")

    
    # Level 3
    # Choosing option YES
    def Forest(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("Forest.jpg")
        self.l1.config(text="You Enter a lush green forest. Will you traverse through it?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Forest)
        self.yes_1.configure(command=self.Door)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Forest(self):
        logging.info("NO")
        self.l1.config(text="You wait idly in the forest")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()

    # Level 4
    # Choosing option YES
    def Door(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("Lake2.png")
        self.l1.config(text="It's a long lake and there are two crocodiles in it. Ahead, you can see a rope. Will you swing from rope to get to end point?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Door)
        self.yes_1.configure(command=self.Alarming)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Door(self):
        logging.info("NO")
        self.l1.config(text="You are injured because crocodile hits you. You are thinking any other way except using rope.")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()

    # Level 5
    # Choosing option YES
    def Alarming(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("sand_dune.png")
        self.l1.config(text="Space contains fire with sand dunes. Hero puts off fire with sand. Will you do this?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Alarming)
        self.yes_1.configure(command=self.Desert_city)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Alarming(self):
        logging.info("NO")
        self.l1.config(text="Your one leg and arm has burned because of fire.")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()


    # Level 6
    # Choosing option YES
    def Desert_city(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("Desert_city.png")
        self.l1.config(text="You see ruins of a city. Will you pass through it?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Desert_city)
        self.yes_1.configure(command=self.Cavern)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Desert_city(self):
        logging.info("NO")
        self.l1.config(text="You see a sandstorm approaching and will not be able to survive it")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()


    # Level 7
    # Choosing option YES
    def Cavern(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("Cavern.png")
        self.l1.config(text="You stumble into a dimly lit cavern. You cannot go right or left but the cave continues ahead. Will you go on?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Cavern)
        self.yes_1.configure(command=self.Cave_goblin)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Cavern(self):
        logging.info("NO")
        self.l1.config(text="You sit down and eat some food you brought with you.")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()

    # Level 8
    # Choosing option YES
    def Cave_goblin(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("Cave_goblin.png")
        self.l1.config(text="You see a Goblin, standing by the fire. Will you try to get past silently?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Cave_goblin)
        self.yes_1.configure(command=self.Castle)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Cave_goblin(self):
        logging.info("NO")
        self.l1.config(text="Goblin notices you and trys to attack with his weapon.")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()


    # Level 9
    # Choosing option YES
    def Castle(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("Castle.png")
        self.l1.config(text="Ruins of a great castle emerge from the fog. Would you explore it?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Castle)
        self.yes_1.configure(command=self.Castle_entrance)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Castle(self):
        logging.info("NO")
        self.l1.config(text="You stand idle in the cold and windy landscape")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()


    # Level 10
    # Choosing option YES
    def Castle_entrance(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("Castle_Entrance.png")
        self.l1.config(text="You stumble upon the entrance of the great castle. Would you go in?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Castle_entrance)
        self.yes_1.configure(command=self.Hallway)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Castle_entrance(self):
        logging.info("NO")
        self.l1.config(text="Scary noises can be heard in the distance, while you look at the castle door ahead.")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()

    # Level 11
    # Choosing option YES
    def Hallway(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("hallway.png")
        self.l1.config(text="You are in a wide hallway. It continues on indefinitely. There's no turning back. Will you go on?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Hallway)
        self.yes_1.configure(command=self.Pit)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Hallway(self):
        logging.info("NO")
        self.l1.config(text="You try to call your help but no one is there.")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()

    # Level 12
    # Choosing option YES
    def Pit(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("Pit.png")
        self.l1.config(text="You fall head first into an ominous and languid pit. Luckly, you only landed on your back. You can try to climb out. Will you try?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Pit)
        self.yes_1.configure(command=self.Dungeon)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Pit(self):
        logging.info("NO")
        self.l1.config(text="You sit in utter darkness.")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()

    # Level 13
    # Choosing option YES
    def Dungeon(self):
        logging.info("YES")
        self.medkit()
        self.bat_attack()
        self.snake_attack()

        self.change_img("Dungeon.png")
        self.l1.config(text="You find yourself in a Dungeon, at the end you see a door with shining light beaming through. Will you pry inside?")
        self.l2.pack()
        self.no_1.configure(command=self.no_Dungeon)
        self.yes_1.configure(command=self.Gold)

        hero.score += 50
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def no_Dungeon(self):
        logging.info("NO")
        self.l1.config(text="You stand the dark hallway.")
        self.l2.pack()

        hero.score -= 50
        self.update_score_label()

    # Level 14
    # Choosing option YES
    def Gold(self):
        logging.info("YES")
        self.change_img("Gold.png")
        self.l1.config(text="You reached to your final destination.Finally, you can see gold. You can take the gold. Will you take?")
        self.l2.pack()
        self.no_1.configure(command=self.Lose)
        self.yes_1.configure(command=self.Win)

        hero.score += 100
        self.update_score_label()

        self.change_level(10)

    # Choosing option NO
    def Lose(self):
        logging.info("LOSE")
        self.change_img("Lose.png")
        self.l1.config(text="You did not take the Gold. GAME OVER!")

        pygame.mixer.music.stop()
        # Load and play background music in a loop
        pygame.mixer.music.load("SFX\mixkit-game-over-trombone-1940.wav")  # Replace with your music file
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

        hero.score -= 100
        self.update_score_label()

    # Choosing option YES
    def Win(self):
        logging.info("WON")
        self.change_img("Win.png")
        self.l1.config(text="You took enough gold. GAME OVER!")
        self.l2.pack()

        pygame.mixer.music.stop()
        # Load and play background music in a loop
        pygame.mixer.music.load("SFX\mixkit-medieval-show-fanfare-announcement-226.wav")  # Replace with your music file
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely




class Game:

    def print_slow(self, str, delay=0.1):
        for letter in str:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(delay)
        print("\n")


    def reset_console(self):
        print("\n")
        os.system('cls||clear')


    def fprint(self, str, delay=0):
        print("\n" + str)
        time.sleep(delay)


    def sprint(self, str, delay=0):
        print(str)
        time.sleep(delay)


game_functions = Game()

class World:

    def entry(self):
        hero.location = "entry"
        print(f"\nHealth: {hero.health}")
        game_functions.fprint("You are in a dark cave. The entry has been sealed by fallen rocks. There is no way out.", 2)
        print("Ahead, you can see a door. Will you continue?")
        print("Enter 'yes' or 'no'.")
        self.check_medkit()
        self.handle_goblin()
        while True:
            action = input("\n> ")
            if action == "yes":
                self.door()
            elif action == "no":
                game_functions.fprint("A bat flies over your head and you hear screetches in the distance.")
            elif action == "m":
                self.use_medkit()
            else:
                game_functions.fprint("You sit in total darkness wondering if there's a way out.")

    def door(self):
        hero.location = "door"
        print(f"\nHealth: {hero.health}")
        game_functions.fprint("Door is opened by kick. Contains fast wind.", 2)
        print("Hero crawls to groung and reach end. Will you crawl?")
        print("Enter 'yes' or 'no'.")
        self.check_medkit()
        self.handle_goblin()
        while True:
            action = input("\n> ")
            if action == "yes":
                self.forest()
            elif action == "no":
                game_functions.fprint("You hear loud voices of wind.")
            elif action == "m":
                self.use_medkit()
            else:
                game_functions.fprint("You are scare of voices.")

    def forest(self):
        hero.location = "forest"
        print(f"\nHealth: {hero.health}")
        game_functions.fprint("It is a lush forest.", 2)
        print("Ahead you can see a muddy path. Will you traverse the path?")
        print("Enter 'yes' or 'no'.")
        self.check_medkit()
        self.handle_goblin()
        while True:
            action = input("\n> ")
            if action == "yes":
                self.lake()
            elif action == "no":
                game_functions.fprint("You hear loud voices of wind.")
            elif action == "m":
                self.use_medkit()
            else:
                game_functions.fprint("You are scare of voices.")

    def lake(self):
        hero.location = "lake"
        print(f"\nHealth: {hero.health}")
        game_functions.fprint("It's a long lake and there are two crocodiles in it.", 2)
        print("Ahead, you can see a rope. Will you swing from rope to get to end point?")
        print("Enter 'yes' or 'no'.")
        self.check_medkit()
        self.handle_goblin()
        while True:
            action = input("\n> ")
            if action == "yes":
                self.alarming()
            elif action == "no":
                game_functions.fprint("You are injured because crocodile hits you.")
            elif action == "m":
                self.use_medkit()
            else:
                game_functions.fprint("You are thinking any other way except using rope.")

    def alarming(self):
        hero.location = "alarming"
        print(f"\nHealth: {hero.health}")
        game_functions.fprint("Space contains fire with sand dunes.", 2)
        print("Hero puts off fire with sand. Will you do this?")
        print("Enter 'yes' or 'no'.")
        self.check_medkit()
        while True:
            action = input("\n> ")
            if action == "yes":
                self.cavern()
            elif action == "no":
                game_functions.fprint("Your one leg and arm has burned because of fire.")
            elif action == "m":
                self.use_medkit()
            else:
                game_functions.fprint("You are feeling very hot.")

    def cavern(self):
        hero.location = "cavern"
        print(f"\nHealth: {hero.health}")
        game_functions.fprint("You stumble into a dimly lit cavern.", 2)
        print("You cannot go right or left but the cave continues ahead. Will you go on?")
        print("Enter 'yes' or 'no'.")
        self.check_bat_attack()
        self.handle_goblin()
        while True:
            action = input("\n> ")
            if action == "yes":
                self.hallway()
            elif action == "no":
                game_functions.fprint("You sit down and eat some food you brought with you.")
            elif action == "m":
                self.use_medkit()
            else:
                game_functions.fprint("You shiver from the cold.")

    def hallway(self):
        hero.location = "hallway"
        print(f"\nHealth: {hero.health}")
        game_functions.fprint("You are in a wide hallway. It continues on indefinitely.", 2)
        print("There's no turning back. Will you go on?")
        print("Enter 'yes' or 'no'.")
        self.handle_goblin()
        while True:
            action = input("\n> ")
            if action == "yes":
                self.pit()
            elif action == "no":
                game_functions.fprint("You try to call your help but no one is there.")
            elif action == "m":
                self.use_medkit()
            else:
                game_functions.fprint("You wonder what time it is.")

    def pit(self):
        hero.location = "pit"
        print(f"\nHealth: {hero.health}")
        game_functions.fprint("You fall head first into an ominous and languid pit. Luckly, you only landed on your back", 2)
        print("You can try to climb out. Will you try?")
        print("Enter 'yes' or 'no'.")
        self.handle_goblin()
        while True:
            action = input("\n> ")
            if action == "yes":
                self.gold()
            elif action == "no":
                game_functions.fprint("You sit in utter darkness.")
            elif action == "m":
                self.use_medkit()
            else:
                game_functions.fprint("You feel hopeless.")

    def gold(self):
        hero.location = "gold"
        print(f"\nHealth: {hero.health}")
        game_functions.fprint("You reached to your final destination.", 2)
        game_functions.sprint("Finally, you can see gold.", 2)
        print("You can take the gold. Will you take?")
        print("Enter 'yes' or 'no'.")
        while True:
            action = input("\n> ")
            if action == "yes":
                game_functions.fprint("You take enough gold.", 2)
                print("GAME OVER.")
                sys.exit()
            elif action == "no":
                game_functions.fprint("You don't find the gold, you lose.")
            elif action == "m":
                self.use_medkit()
            else:
                game_functions.fprint("You give up.")




    def use_medkit(self):
        if "medkit" in hero.items:
            hero.items -= 1
            game_functions.fprint("You used your medkit")
            hero.health = 100
            print(f"\nHealth: {hero.health}")
        else:
            game_functions.fprint("You don't have a medkit.")



    def check_medkit(self):
        medkit_find = random.choice([True, False])
        if medkit_find is True:
            hero.items += 1
            game_functions.fprint("You found a medkit!", 2)
            print("Enter 'm' to use it.")


    def check_bat_attack(self):
        bat_attack = random.choice([True, False])
        if bat_attack is True:
            game_functions.fprint("You were attacked by a bat!", 2)
            hero.health -= random.randint(1, 100)
            print(f"\nHealth: {hero.health}")
            if hero.health == 0:
                game_functions.fprint("You are dead!")
                sys.exit()

def test_run():
    root = Tk()
    gui = GUI(root)
    root.mainloop()
    pass

if __name__ == '__main__':
    # Running the main GUI object
    root = Tk()
    gui = GUI(root)
    root.mainloop()
