MIN_COLOR_DURATION = 250

color_to_dec = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'lime': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'silver': (192, 192, 192),
    'grey': (128, 128, 128),
    'maroon': (128, 0, 0),
    'olive': (128, 128, 0),
    'green': (0, 128, 0),
    'purple': (128, 0, 128),
    'teal': (0, 128, 128),
    'navy': (0, 0, 128),
    'orange': (255, 128, 0)
}

dec_to_color = {
    (0, 0, 0): 'black',
    (255, 255, 255): 'white',
    (255, 0, 0): 'red',
    (0, 255, 0): 'lime',
    (0, 0, 255): 'blue',
    (255, 255, 0): 'yellow',
    (0, 255, 255): 'cyan',
    (255, 0, 255): 'magenta',
    (192, 192, 192): 'silver',
    (128, 128, 128): 'grey',
    (128, 0, 0): 'maroon',
    (128, 128, 0): 'olive',
    (0, 128, 0): 'green',
    (128, 0, 128): 'purple',
    (0, 128, 128): 'teal',
    (0, 0, 128): 'navy',
    (255, 128, 0): 'orange'
}

color_categorical_encoding = {
    'black': 0,
    'white': 1,
    'red': 2,
    'lime': 3,
    'blue': 4,
    'yellow': 5,
    'cyan': 6,
    'magenta': 7,
    'silver': 8,
    'grey': 9,
    'maroon': 10,
    'olive': 11,
    'green': 12,
    'purple': 13,
    'teal': 14,
    'navy': 15,
    'orange': 16
}

valid_pattern = {
    ('black', 'purple', 'silver', 'lime'): 1,
    ('white', 'teal', 'gray', 'blue'): 2,
    ('red', 'navy', 'maroon', 'cyan'): 3,
    ('lime', 'orange', 'olive', 'cyan'): 4,
    ('blue', 'black', 'green', 'magenta'): 5,
    ('yellow', 'yellow', 'purple', 'silver'): 6,
    ('cyan', 'cyan', 'teal', 'grey'): 7,
    ('magenta', 'magenta', 'navy', 'maroon'): 8,
    ('silver', 'silver', 'orange', 'olive'): 9,
    ('grey', 'white', 'white', 'green'): 10,
    ('maroon', 'red', 'red', 'purple'): 11,
    ('olive', 'lime', 'lime', 'teal'): 12,
    ('green', 'blue', 'blue', 'navy'): 13,
    ('purple', 'gray', 'black', 'orange'): 14,
    ('teal', 'maroon', 'yellow', 'black'): 15,
    ('navy', 'olive', 'cyan', 'white'): 16,
    ('orange', 'green', 'magenta', 'red'): 17
}

keys=list(valid_pattern.keys())
