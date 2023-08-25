import os
import json

from dotenv import load_dotenv

load_dotenv()


filename = f'{os.getenv("CONFIG_NAME")}.json'
width    = int(os.getenv("WINDOW_WIDTH"))


if not os.path.exists(filename):
    result = {
        "width": width,
        "height": 800,
        "bgMain": "#b7bcc4",
        "bgFrame": "#8d9199",
        "bgFrame1": "#f0f0f0",
        "imagePath": None,
        "enhancement": {
            "brightening": {
                "value": 0,
                "status": False,
            },
            "contrass": {
                "value": 0,
                "status": False,
            },
            "smoothing": {
                "value": 0,
                "status": False,
            },
            "sharpening": {
                "value": 0,
                "status": False,
            }
        }
    }
                    
    with open(filename, "w") as outfile:
        json.dump(result, outfile)
                
    outfile.close()


def read():
    with open(filename, "r") as openfile:
        config = json.load(openfile)

    openfile.close()

    return config

def write(configuration):
    with open(filename, "w") as outfile:
        json.dump(configuration, outfile)
            
    outfile.close()

    return 1