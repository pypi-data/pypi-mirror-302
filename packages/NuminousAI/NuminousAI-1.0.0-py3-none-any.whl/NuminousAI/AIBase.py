import os
import sys
import click
import appdirs
import subprocess
from tqdm import tqdm
from selenium import webdriver

class AIBase:
    """
    AIBase class to manage the NuminousAI environment.
    It provides functionality to set up directories, execute system commands, 
    and write/execute Python scripts dynamically.
    
    Args:
        verbose (bool): If True, outputs additional information during initialization.
    """
    class Colors:
        def __init__(self) -> None:
                
            # Regular Colors
            self.black = "\033[0;30m"
            self.red = "\033[0;31m"
            self.green = "\033[0;32m"
            self.yellow = "\033[0;33m"
            self.blue = "\033[0;34m"
            self.magenta = "\033[0;35m"
            self.cyan = "\033[0;36m"
            self.white = "\033[0;37m"

            # Bold Colors (Bright)
            self.bold_black = "\033[1;30m"
            self.bold_red = "\033[1;31m"
            self.bold_green = "\033[1;32m"
            self.bold_yellow = "\033[1;33m"
            self.bold_blue = "\033[1;34m"
            self.bold_magenta = "\033[1;35m"
            self.bold_cyan = "\033[1;36m"
            self.bold_white = "\033[1;37m"

            # Underline Colors
            self.underline_black = "\033[4;30m"
            self.underline_red = "\033[4;31m"
            self.underline_green = "\033[4;32m"
            self.underline_yellow = "\033[4;33m"
            self.underline_blue = "\033[4;34m"
            self.underline_magenta = "\033[4;35m"
            self.underline_cyan = "\033[4;36m"
            self.underline_white = "\033[4;37m"

            # Background Colors
            self.background_black = "\033[40m"
            self.background_red = "\033[41m"
            self.background_green = "\033[42m"
            self.background_yellow = "\033[43m"
            self.background_blue = "\033[44m"
            self.background_magenta = "\033[45m"
            self.background_cyan = "\033[46m"
            self.background_white = "\033[47m"

            # Bright Background Colors
            self.background_bright_black = "\033[100m"
            self.background_bright_red = "\033[101m"
            self.background_bright_green = "\033[102m"
            self.background_bright_yellow = "\033[103m"
            self.background_bright_blue = "\033[104m"
            self.background_bright_magenta = "\033[105m"
            self.background_bright_cyan = "\033[106m"
            self.background_bright_white = "\033[107m"

            # Bold Colors
            self.bold_bright_red = "\033[1;91m"
            self.bold_bright_green = "\033[1;92m"
            self.bold_bright_yellow = "\033[1;93m"
            self.bold_bright_blue = "\033[1;94m"
            self.bold_bright_magenta = "\033[1;95m"
            self.bold_bright_cyan = "\033[1;96m"

            # Reset
            self.reset = "\033[0m"

        def get_colors_example(self) -> None:
            # Regular Colors
            print(f"{self.black}This is testing Regular Color text{self.reset}")
            print(f"{self.red}This is testing Regular Color text{self.reset}")
            print(f"{self.green}This is testing Regular Color text{self.reset}")
            print(f"{self.yellow}This is testing Regular Color text{self.reset}")
            print(f"{self.blue}This is testing Regular Color text{self.reset}")
            print(f"{self.magenta}This is testing Regular Color text{self.reset}")
            print(f"{self.cyan}This is testing Regular Color text{self.reset}")
            print(f"{self.white}This is testing Regular Color text{self.reset}\n")

            # Bold Colors (Bright)
            print(f"{self.bold_black}This is testing Bold Color (Bright) text{self.reset}")
            print(f"{self.bold_red}This is testing Bold Color (Bright) text{self.reset}")
            print(f"{self.bold_green}This is testing Bold Color (Bright) text{self.reset}")
            print(f"{self.bold_yellow}This is testing Bold Color (Bright) text{self.reset}")
            print(f"{self.bold_blue}This is testing Bold Color (Bright) text{self.reset}")
            print(f"{self.bold_magenta}This is testing Bold Color (Bright) text{self.reset}")
            print(f"{self.bold_cyan}This is testing Bold Color (Bright) text{self.reset}")
            print(f"{self.bold_white}This is testing Bold Color (Bright) text{self.reset}\n")

            # Underline Colors
            print(f"{self.underline_black}This is testing Underline Color text{self.reset}")
            print(f"{self.underline_red}This is testing Underline Color text{self.reset}")
            print(f"{self.underline_green}This is testing Underline Color text{self.reset}")
            print(f"{self.underline_yellow}This is testing Underline Color text{self.reset}")
            print(f"{self.underline_blue}This is testing Underline Color text{self.reset}")
            print(f"{self.underline_magenta}This is testing Underline Color text{self.reset}")
            print(f"{self.underline_cyan}This is testing Underline Color text{self.reset}")
            print(f"{self.underline_white}This is testing Underline Color text{self.reset}\n")

            # Background Colors
            print(f"{self.background_black}This is testing Background Color text{self.reset}")
            print(f"{self.background_red}This is testing Background Color text{self.reset}")
            print(f"{self.background_green}This is testing Background Color text{self.reset}")
            print(f"{self.background_yellow}This is testing Background Color text{self.reset}")
            print(f"{self.background_blue}This is testing Background Color text{self.reset}")
            print(f"{self.background_magenta}This is testing Background Color text{self.reset}")
            print(f"{self.background_cyan}This is testing Background Color text{self.reset}")
            print(f"{self.background_white}This is testing Background Color text{self.reset}\n")

            # Bright Background Colors
            print(f"{self.background_bright_black}This is testing Bright Background Color text{self.reset}")
            print(f"{self.background_bright_red}This is testing Bright Background Color text{self.reset}")
            print(f"{self.background_bright_green}This is testing Bright Background Color text{self.reset}")
            print(f"{self.background_bright_yellow}This is testing Bright Background Color text{self.reset}")
            print(f"{self.background_bright_blue}This is testing Bright Background Color text{self.reset}")
            print(f"{self.background_bright_magenta}This is testing Bright Background Color text{self.reset}")
            print(f"{self.background_bright_cyan}This is testing Bright Background Color text{self.reset}")
            print(f"{self.background_bright_white}This is testing Bright Background Color text{self.reset}\n")

            # Bold Colors
            print(f"{self.bold_bright_red}This is testing Bold Color text{self.reset}")
            print(f"{self.bold_bright_green}This is testing Bold Color text{self.reset}")
            print(f"{self.bold_bright_yellow}This is testing Bold Color text{self.reset}")
            print(f"{self.bold_bright_blue}This is testing Bold Color text{self.reset}")
            print(f"{self.bold_bright_magenta}This is testing Bold Color text{self.reset}")
            print(f"{self.bold_bright_cyan}This is testing Bold Color text{self.reset}")

    def __init__(self):
        # Define the Python interpreter to be used (can be extended for multi-interpreter support)
        self.interpreter = "python"
        
        # Set up application directories using appdirs for storing cache
        appdir = appdirs.AppDirs(appname="NuminousAI", appauthor="Sujal Rajpoot")
        self.App_Name = appdir.appname
        self.App_Author = appdir.appauthor
        self.NuminousAI_Base_Directory = appdir.user_config_dir
        self.NuminousAI_AutoExecution_Path = os.path.join(self.NuminousAI_Base_Directory, "NuminousAI_Execution.py")
        self.NuminousAI_Conversation_File_Path = os.path.join(self.NuminousAI_Base_Directory, "Conversation.json")

        # Ensure the base path exists or create it
        if not os.path.exists(self.NuminousAI_Base_Directory):
            os.makedirs(self.NuminousAI_Base_Directory)

        # print("DeepInfraAI initialized")
        # print(f"App Name: {self.App_Name}")
        # print(f"App Author: {self.App_Author}")
        # print(f"NuminousAI Base Directory: {self.NuminousAI_Base_Directory}")
        # print(f"AutoExecution Python File: {self.NuminousAI_AutoExecution_Path}")
        # print(f"Conversation File: {self.NuminousAI_Conversation_File_Path}\n")
    
    def run_system_command(
        self,
        command: str,
        exit_on_error: bool = True,
        stdout_error: bool = True,
        help: str = None
    ):
        """
        Run system commands in the shell.
        
        Args:
            command (str): The shell command to be executed.
            exit_on_error (bool): Exit on error if set to True. Defaults to True.
            stdout_error (bool): Print the error to stdout if set to True. Defaults to True.
            help (str): Optional help message in case of failure.
        
        Returns:
            tuple: (is_successful (bool), result (subprocess.CompletedProcess or Exception))
        """
        try:
            # Run the system command and capture the output
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return (True, result)
        except subprocess.CalledProcessError as e:
            # Handle error when command execution fails
            if stdout_error:
                click.secho(f"Error occurred while running: '{command}'", fg="yellow")
                click.secho(e.stderr, fg="red")
                if help:
                    click.secho(help, fg="cyan")
            if exit_on_error:
                sys.exit(e.returncode)
            return (False, e)

    def auto_execution_script(self, code: str):
        """
        Write and execute a custom Python script in the AutoExecution file.
        
        Args:
            code (str): The Python code to write and execute.
        
        Returns:
            str: Success or error message.
        """
        if not code:
            return "No code provided to execute.\n"

        try:
            # Write the provided Python code to the AutoExecution file
            with open(self.NuminousAI_AutoExecution_Path, "w") as file_handle:
                file_handle.write(code)

            # Execute the script that was just written
            try:
                is_successful, result = self.run_system_command(f'{self.interpreter} "{self.NuminousAI_AutoExecution_Path}"')

                # Return the appropriate message based on the execution result
                if is_successful:
                    return f"Script executed successfully.\nOutput:\n{result.stdout}\n"
                else:
                    return f"Script execution failed.\nError:\n{result.stderr}\n"

            except Exception as execute_error:
                return f"An error occurred during script execution: {execute_error}\n"

        except Exception as write_error:
            return f"An error occurred while writing the script: {write_error}\n"

    def get_total_size(self, folder) -> int:
        """
        - Returns the total size of all files in the given folder and its subfolders.
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total_size += os.path.getsize(fp)
                except PermissionError:
                    # Skip files that we don't have permission to access
                    continue
        return total_size

    def copy_with_progress(self, source_folder, destination_folder) -> None:
        """
        # Copies a folder and all its contents to a destination folder, with a progress bar.

        - param source_folder: The folder to copy from
        - param destination_folder: The folder to copy to
        - return: None
        """

        total_size = self.get_total_size(source_folder)
        copied_size = 0

        # Create destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        # Progress bar setup
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Copying", ncols=100)

        # Walk through the source folder
        for dirpath, dirnames, filenames in os.walk(source_folder):
            # Create corresponding destination directory
            dest_dir = dirpath.replace(source_folder, destination_folder, 1)
            os.makedirs(dest_dir, exist_ok=True)

            for file in filenames:
                source_file = os.path.join(dirpath, file)
                dest_file = os.path.join(dest_dir, file)

                try:
                    # Copy the file in chunks to track progress
                    with open(source_file, 'rb') as sf, open(dest_file, 'wb') as df:
                        while True:
                            buffer = sf.read(1024 * 1024)  # Read in chunks of 1MB
                            if not buffer:
                                break
                            df.write(buffer)
                            copied_size += len(buffer)
                            progress_bar.update(len(buffer))
                except PermissionError:
                    # Skip files that we don't have permission to copy
                    # print(f"Skipping file due to permission error: {source_file}")
                    continue
        progress_bar.close()

    def get_website_cookies(self, website_url:str, verbose:bool = True) -> str:
        """
        - Refreshes the demo API key by using Selenium to open a headless Chrome session and fetch the cookies.
        - Then it uses the cookies to fetch the API key from the /api/auth/session endpoint.
        - The API key is then written to the config file in human-readable format.

        - If the refresh fails, it will retry the process.
        """
        home_dir = os.path.expanduser("~")
        source_folder = os.path.join(home_dir, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
        destination_folder = os.path.join(AIBase().NuminousAI_Base_Directory, "ChromeData")
        if not os.path.exists(destination_folder):
            print("\033[1;91m🚨 ChromeData folder not found in required path. 📁 Automatically copying to required location... 🔄\033[0m")
            print("\033[1;91m🚫 This process may take a few moments. Please do not attempt to interact with the system until it completes.\033[0m\n")
            self.copy_with_progress(source_folder, destination_folder)
        
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={destination_folder}")
        options.add_argument('--profile-directory=Default')
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        print("\n\033[1;96mFetching Required Cookies...\033[0m")
        driver.get(website_url)

        cookies = driver.get_cookies()
        driver.quit()

        if verbose:print(f"All Extracted Cookies: {cookies}\n")

        cookies_dict = {item['name']: item['value'] for item in cookies}
        print("\033[1;92mRequired Cookies Fetched Successfully.\033[0m\n")
        return f"Required Cookies Dictionary: \033[1;95m{cookies_dict}\033[0m\n"

# Example Python code to be executed
python_code = """def greet(name):\n    return f"Hello, {name}!"\nprint(greet("Sujal"))"""

if __name__ == "__main__":
    ai = AIBase()

    # Call the method to write and execute the script
    result_message = ai.auto_execution_script(python_code)

    # Output the result message from the function
    print(result_message)
