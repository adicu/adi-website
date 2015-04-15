
class CLIColor(object):
    ENDC = '\033[0m'

    @staticmethod
    def header(message):
        return '\033[95m' + message + CLIColor.ENDC

    @staticmethod
    def ok_blue(message):
        return '\033[94m' + message + CLIColor.ENDC

    @staticmethod
    def ok_green(message):
        return '\033[92m' + message + CLIColor.ENDC

    @staticmethod
    def warning(message):
        return '\033[93m' + message + CLIColor.ENDC

    @staticmethod
    def fail(message):
        return '\033[91m' + message + CLIColor.ENDC

    @staticmethod
    def bold(message):
        return '\033[1m' + message + CLIColor.ENDC

    @staticmethod
    def underline(message):
        return '\033[4m' + message + CLIColor.ENDC
