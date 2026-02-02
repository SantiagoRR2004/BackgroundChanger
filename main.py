from pythocron.CrontabManager import CrontabManager
import subprocess
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
