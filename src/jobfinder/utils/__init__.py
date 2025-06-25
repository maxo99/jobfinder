from datetime import datetime


def get_now(underscore: bool = False) -> str:
    if underscore:
        return datetime.now().strftime('%Y%m%d_%H%M%S')
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
