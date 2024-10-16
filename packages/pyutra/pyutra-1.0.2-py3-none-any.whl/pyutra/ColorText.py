class ColorText:
  COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[39m'
  }

  BACKGROUNDS = {
    'black': '\033[40m',
    'red': '\033[41m',
    'green': '\033[42m',
    'yellow': '\033[43m',
    'blue': '\033[44m',
    'magenta': '\033[45m',
    'cyan': '\033[46m',
    'white': '\033[47m',
    'reset': '\033[49m'
  }

  STYLES = {
    'bold': '\033[1m',
    'underline': '\033[4m',
    'reversed': '\033[7m',
    'reset': '\033[0m'
  }

  def colorize(self, text: str, color=None, background=None, style=None):
    if style and style in self.STYLES:
      text = self.STYLES[style] + text

    if color and color in self.COLORS:
      text = self.COLORS[color] + text

    if background and background in self.BACKGROUNDS:
      text = self.BACKGROUNDS[background] + text

    return text + self.STYLES['reset']