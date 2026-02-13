import platform
import subprocess
import ctypes
import os
import json
import random
import requests


def set_wallpaper(image_path: str) -> None:
    """
    Set the wallpaper of the current desktop environment.
    If the image file exists we will say it is a path in the system.
    It should be an absolute path.
    If not we will try to download it.

    We can't use url because there it does a Ddos attack on
    the router. If we fix it, we would use
    gsettings set org.gnome.desktop.background picture-uri "https://example.com/image.jpg"

    Args:
        image_path (str): The path to the image file.
    """
    system = platform.system()

    if not os.path.exists(image_path):
        tempFile = os.path.join(os.path.expanduser("~"), ".tempBackground.png")

        response = requests.get(image_path, stream=True)
        if response.status_code == 200:

            if not response.headers.get("content-type") or response.headers.get(
                "content-type"
            ).startswith("image"):
                # Problem with .webp images because they don't have the content-type
                with open(tempFile, "wb") as file:
                    file.write(response.content)
                image_path = tempFile
            else:
                raise Exception(
                    f"It is not an image. Content type: {response.headers.get("content-type")}"
                )

        else:
            raise Exception(
                f"Failed to retrieve image. Status code: {response.status_code}"
            )

    else:
        image_path = os.path.abspath(image_path)

    if system == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    elif system == "Darwin":  # macOS
        script = f"""
        tell application "Finder"
            set desktop picture to POSIX file "{image_path}"
        end tell
        """
        subprocess.run(["osascript", "-e", script])
    elif system == "Linux":
        """
        The original Linux color was
        #2c001e
        This was obtrined with the command gsettings get org.gnome.desktop.background primary-color
        """
        colors = ["00", "FF", f"{random.randint(0,255):02X}"]
        random.shuffle(colors)

        command = f"""export DISPLAY=":0"
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"
gsettings set org.gnome.desktop.background primary-color '#{''.join(colors)}'
gsettings set org.gnome.desktop.background picture-uri file://{image_path}
gsettings set org.gnome.desktop.background picture-options scaled"""

        subprocess.run(command, shell=True)
    else:
        raise Exception("Unsupported operating system")


def getBookmarks() -> dict:
    """
    Get the bookmarks from the Chrome browser.

    Should work on Windows, macOS, and Linux.

    Returns:
        dict: The bookmarks tree.
    """
    system = platform.system()

    if system == "Windows":
        # Not tested yet
        path = os.path.join(
            os.path.expanduser("~"),
            "AppData",
            "Local",
            "Google",
            "Chrome",
            "User Data",
            "Default",
            "Bookmarks",
        )

    elif system == "Darwin":  # macOS
        # Not tested yet
        path = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Google",
            "Chrome",
            "Default",
            "Bookmarks",
        )

    elif system == "Linux":
        path = os.path.join(
            os.path.expanduser("~"), ".config", "google-chrome", "Default", "Bookmarks"
        )
    else:
        print("Unsupported operating system")

    # Read the bookmarks file
    with open(path, "r") as file:
        data = json.load(file)

    return data


def findBookmarkFolder(bookmarks: dict, folder_name: str) -> dict:
    """
    Find a bookmark folder in the bookmarks tree.

    Args:
        bookmarks (dict): The bookmarks tree.
        folder_name (str): The name of the folder to find.

    Returns:
        dict: The folder found or None if it was not found.
    """
    if "name" in bookmarks.keys() and bookmarks["name"] == folder_name:
        return bookmarks
    if "children" in bookmarks.keys():
        for child in bookmarks["children"]:
            folder = findBookmarkFolder(child, folder_name)
            if folder:
                return folder
    return None


def getBookmarksFromFolder(bookmarks: dict, solution: dict = {}) -> dict:
    """
    Get the bookmarks urls from a folder in the bookmarks tree.
    It is a recursive function.

    Args:
        bookmarks (dict): The bookmarks tree.
        solution (dict): The dictionary where the urls will be stored.

    Returns:
        dict: The dictionary with the urls.
    """
    if "type" in bookmarks.keys() and bookmarks["type"] == "url":
        solution[bookmarks["name"]] = bookmarks["url"]
    if "children" in bookmarks.keys():
        for child in bookmarks["children"]:
            solution.update(getBookmarksFromFolder(child, solution))
    return solution


if __name__ == "__main__":
    # Get the current directory
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    backgroundsFile = os.path.join(currentDirectory, "backgrounds.json")
    failureFile = os.path.join(currentDirectory, "failures.json")

    # Load the background log
    if not os.path.exists(backgroundsFile):
        backgroundsLog = {}
    else:
        with open(backgroundsFile, "r", encoding="utf-8") as file:
            backgroundsLog = json.load(file)

    bookmarks = getBookmarks()["roots"]

    index = 0

    while index < len(bookmarks.keys()):
        temp = findBookmarkFolder(
            bookmarks[list(bookmarks.keys())[index]], "Backgrounds"
        )
        if temp:
            backgroundFolder = temp
            index = len(bookmarks.keys())
        index += 1

    backgrounds = getBookmarksFromFolder(backgroundFolder)
    wallpaper = random.choice(list(backgrounds.items()))

    # Add if it is not in the log
    if not backgroundsLog.get(wallpaper[0]):
        backgroundsLog[wallpaper[0]] = {"failures": 0, "successes": 0}

    # for wallpaper in backgrounds.items(): # Check all wallpapers
    try:
        set_wallpaper(wallpaper[1])
        backgroundsLog[wallpaper[0]]["successes"] += 1
    except Exception as e:
        print(f"Error setting {wallpaper[0]} as wallpaper.")
        print(e)

        try:
            response = requests.get("https://www.google.com")
            if response.status_code == 200:
                # There is no problem with the internet connection
                backgroundsLog[wallpaper[0]]["failures"] += 1
        except Exception as e:
            print("Problem with the internet connection.")

    # Sort by name of the wallpaper
    backgroundsLog = dict(
        sorted(backgroundsLog.items(), key=lambda item: item[0], reverse=False)
    )

    # Save the background log
    with open(backgroundsFile, "w", encoding="utf-8") as file:
        json.dump(backgroundsLog, file, indent=2, ensure_ascii=False)
        file.write("\n")

    # Create a log of the failures
    failures = {}
    for wallpaper in backgroundsLog.keys():
        if backgroundsLog[wallpaper]["failures"] > 0:
            failures[wallpaper] = backgroundsLog[wallpaper]["failures"] / (
                backgroundsLog[wallpaper]["failures"]
                + backgroundsLog[wallpaper]["successes"]
            )

    # Sort by failure rate
    failures = dict(
        sorted(failures.items(), key=lambda item: (item[1], item[0]), reverse=True)
    )

    # Save the failure log
    with open(failureFile, "w", encoding="utf-8") as file:
        json.dump(failures, file, indent=2, ensure_ascii=False)
        file.write("\n")
