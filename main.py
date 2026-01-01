from pythocron.CrontabManager import CrontabManager
import os

"""
This is to activate the crontab manager
with all the python files that need to be run
"""

if __name__ == "__main__":
    currentFile = os.path.abspath(__file__)
    currentDirectory = os.path.dirname(currentFile)

    environmentPath = os.path.join(currentDirectory, ".venv", "bin", "activate")

    pythonFiles = []

    CrontabManager().setup(
        environmentPath=environmentPath,
        pythonFiles=[{"file": file} for file in pythonFiles],
    )
