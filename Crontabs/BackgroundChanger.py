import platform
import subprocess
import ctypes
import os
import json


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
        import requests
        response = requests.get(image_path, stream=True)
        if response.status_code == 200:
            with open(tempFile, "wb") as file:
                file.write(response.content)
            image_path = tempFile
        else:
            raise Exception(f"Failed to retrieve image. Status code: {response.status_code}")
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

        command = f"""export DISPLAY=":0"
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"
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
    import random

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

    try:
        set_wallpaper(wallpaper[1])
    except Exception as e:
        print(f"Error setting {wallpaper[0]} as wallpaper.")
        print(e)
