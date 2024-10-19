def info():
    return {
        "name": "Hamidreza",
        "age": 21,
        "major": "Computer Engineering",
        "site": "https://MrHamidreza.ir",
    }


def time():
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
