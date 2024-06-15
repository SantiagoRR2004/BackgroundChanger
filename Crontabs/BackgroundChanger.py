import platform
import subprocess
import ctypes
import os

def set_wallpaper(image_path: str) -> None:
    """
    Set the wallpaper of the current desktop environment.
    If the image file exists we will say it is a path in the system.
    It should be an absolute path.
    If not we will suppose it is a URL and use it directly.
    
    Args:
        image_path (str): The path to the image file.
    """
    system = platform.system()
    
    if system == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    elif system == "Darwin":  # macOS
        script = f'''
        tell application "Finder"
            set desktop picture to POSIX file "{image_path}"
        end tell
        '''
        subprocess.run(["osascript", "-e", script])
    elif system == "Linux":
        desktop_env = subprocess.run(["echo $XDG_CURRENT_DESKTOP"], shell=True, capture_output=True, text=True).stdout.strip()
        if "GNOME" in desktop_env or "Unity" in desktop_env:
            if os.path.exists(image_path):
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{image_path}"])
            else:
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"{image_path}"])
        else:
            print(f"Unsupported Linux desktop environment {desktop_env}")
    else:
        print("Unsupported operating system")


if __name__ == "__main__":
    import time
    backgrounds = [
        "https://www.woodus.com/den/gallery/graphics/dq9ds/wallpaper/monsters.jpg",
        "https://www.spriters-resource.com/resources/sheets/45/47529.png?updated=1460959095",
        "https://darksouls.wiki.fextralife.com/file/Dark-Souls/Dark-Souls_Wallpaper7_1920_1200.jpg",
        "https://steamuserimages-a.akamaihd.net/ugc/2058741034012526512/379E6434B473E7BE31C50525EB946D4212A8C8B3/",
        "https://www.capcom-games.com/ghosttrick/assets/images/video/video_img1_en.jpg",
        "https://images7.alphacoders.com/749/749807.png",
        "https://ubuntu.com/wp-content/uploads/c919/noble1.png"
    ]

    for background in backgrounds:
        set_wallpaper(background)
        time.sleep(2)
