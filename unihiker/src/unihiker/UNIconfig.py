import os
import platform

class UNIConfig:
    def __init__(self):
        pass

    def set_brightness(self, brightness):
        # Determine the operating system
        system = platform.system()

        # Check if the system is Linux; if not, show an error message and return early
        if system != "Linux":
            print("Error: brightness command is not supported on this system. Please connect to UNIHIKER.")
            return

        # Check if brightness is an integer (supports subclass of int)
        if not isinstance(brightness, int):
            print("Error: brightness must be an integer value.")
            return

        # Check if the brightness value is within the valid range (0 to 100)
        if not (0 <= brightness <= 100):
            print("Error: brightness must be between 0 and 100.")
            return
        
        file_path = '/opt/unihiker/Version'

        def is_unihiker_system(file_path):
            return os.path.exists(file_path)
        
        if is_unihiker_system(file_path):
            # Execute the brightness command
            result = os.system(f'brightness {brightness}')
            if result != 0:
                print("Error: failed to set brightness. Please check if the 'brightness' command is available and you have sufficient permissions.")
                return
        else:
            print("Error: brightness command is not supported on this system. Please connect to UNIHIKER.")