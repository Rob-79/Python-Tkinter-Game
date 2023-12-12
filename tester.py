import unittest
from tkinter import Tk
from main import GUI 
import time
from unittest.mock import patch

import main

import coverage



class TestGameMainCode(unittest.TestCase):

    # hero = player("entry", 100, 0, 0)

    def test_main_code_execution(self):
        try:
            # Attempt to run the main code
            root = Tk()
            gui = GUI(root)
            root.after(1000, root.destroy)  # Schedule the destruction of the root window after 1000 milliseconds
            root.mainloop()

            # If no exceptions are raised, the test passes
            self.assertTrue(True, "Main code execution successful")
        except Exception as e:
            # If an exception occurs, the test fails and prints the exception
            self.fail(f"Main code execution failed with exception: {str(e)}")

    def test_gui_initialization(self):
        # Test if the GUI initializes without errors
        try:
            root = Tk()
            gui = GUI(root)
            self.assertTrue(gui is not None, "GUI initialized successfully")
            root.destroy()  # Close the root window after the test
        except Exception as e:
            self.fail(f"GUI initialization failed with exception: {str(e)}")


    def test_minimum_levels(self):
        root = Tk()
        gui = GUI(root)
        levels = gui.max_level
        root.destroy()
        assert levels >= 8, "Game initializes with minimum required levels"


    def test_decision_points_integration(self):
        root = Tk()
        gui = GUI(root)

        
        # Buttons that are part of the GUI
        yes_button_exists = gui.yes_1.winfo_exists()
        no_button_exists = gui.no_1.winfo_exists()
        
        root.destroy()
        
        assert yes_button_exists and no_button_exists, "Decision points are integrated into the game storyline with YES and NO buttons present"

    def test_UI_accessbility(self):
        root = Tk()
        gui = GUI(root)

        
        # Buttons that are part of the GUI
        yes_button_exists = gui.yes_1.winfo_exists()
        no_button_exists = gui.no_1.winfo_exists()
        medkit_button = gui.use_medkit.winfo_exists()
        level_indicator_bar = gui.level_indicator.winfo_exists()
        root.destroy()
        
        assert yes_button_exists and no_button_exists and medkit_button and level_indicator_bar, "All UI accessbility buttons are available"

    @patch('random.choice', return_value=True)  # Mocking random.choice to always return True
    def test_multiple_attacks(self, mock_random_choice):
        root = Tk()
        gui = GUI(root)
        
        # hero = player("entry", 100, 0, 0)
        
        gui.bat_attack()
        gui.snake_attack()

        root.destroy()

        print("Player Health after attacks: ", main.hero.health)
        self.assertTrue(main.hero.health <= 100, "Health should be less than 100")


    @patch('random.choice', return_value=True)  # Mocking random.randint to always return a specific value
    def test_scoring_after_successful_attack(self, mock_random_randint):
        root = Tk()
        gui = GUI(root)
                
        gui.bat_attack()
        gui.snake_attack()

        root.destroy()

        print("Player Score: ", main.hero.score)
        self.assertTrue(main.hero.score > 0, "Health should be less than 100")


    def test_show_notification(self):
        root = Tk()
        gui = GUI(root)


        gui.notification_manager.show_notification("Test Notification", "Medkit.jpg", "This is a test notification")

        # Checking if the notifications has been added to the Notification list
        self.assertEqual(len(gui.notification_manager.notifications), 1)




        


if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()

    unittest.main()

    cov.stop()

    # Save coverage information to an XML file
    cov.save()
    temp = cov.get_data()
    print(temp)
    cov.xml_report(outfile='coverage.xml')