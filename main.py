import subprocess
import sys
import os

"""
This is to activate the crontab manager
with all the python files that need to be run
"""

if __name__ == "__main__":
    currentFile = os.path.abspath(__file__)
    currentDirectory = os.path.dirname(currentFile)

    # Run the environment setup bash script
    environmentScript = os.path.join(currentDirectory, "environment.sh")
    subprocess.run(["bash", environmentScript], check=True)

    # Path to your venv site-packages
    venvPath = os.path.join(
        currentDirectory, ".venv", "lib", "python3.12", "site-packages"
    )
    sys.path.insert(0, str(venvPath))

    # Import the modules
    from pythocron.CrontabManager import CrontabManager

    environmentPath = os.path.join(currentDirectory, ".venv", "bin", "activate")

    pythonFiles = [
        {
            "file": os.path.join(currentDirectory, "BackgroundChanger.py"),
            "logFile": os.path.join(currentDirectory, "output.log"),
            "oncePerDay": False,
        },
    ]

    CrontabManager().setup(
        environmentPath=environmentPath,
        pythonFiles=pythonFiles,
        howOften=1,
    )
