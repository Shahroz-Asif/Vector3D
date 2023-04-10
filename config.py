window = {
    "dimensions": {
        "width": 600,
        "height": 700
    }
}

texts = {
    "title": "Vector3D",
    "dp_text": "Dot Product of provided vectors:",
    "dp_value": "No vectors provided!",
    "button": "PLOT",
    "credits": "Credits to Shahroz Asif, Saad Ehsan and Mubashir Abid"
}

colors = {
    "a_primary": "#E53935",
    "a_secondary": "#EF9A9A",
    "b_primary": "#1E88E5",
    "b_secondary": "#90CAF9",
    "dot": "#43A047"
}

graph = {
    "arrow_style": {
        "mutation_scale": 20,
        "lw": 2,
        "arrowstyle": "-|>"
    }
}

# === POSITIONAL ===

frames = {
    "title": {
        "sticky": "wne",
        "padx": 10,
        "pady": 10
    },
    "input": {
        "sticky": "we",
        "padx": 10,
        "pady": (0, 10)
    },
    "product": {
        "sticky": "we",
        "padx": 10,
        "pady": (0, 10)
    },
    "graph": {
        "sticky": "we",
        "padx": 10,
        "pady": (0, 10)
    },
    "credits": {
        "sticky": "wes",
        "padx": 10,
        "pady": (0, 10)
    }
}

entries = {
    "vector": {
        "padx": 10,
        "pady": 10,
        "sticky": "ns"
    },
    "comp": {
        "pady": 5,
        "padx": (0, 3),
        "sticky": "ns"
    }
}

buttons = {
    "generate": {
        "padx": 10,
        "pady": 10,
        "sticky": "nes"
    }
}

labels = {
    "dp_text": {
        "padx": 10,
        "pady": 10,
        "sticky": "wns"
    },
    "dp_value": {
        "padx": 10,
        "pady": 10,
        "sticky": "wns"
    },
    "vec": {
        "pady": 5,
        "padx": (8, 7)
    },
    "comp": {
        "pady": 5,
        "padx": (0, 8),
        "sticky": "ns"
    }
}

#  ((?<!")\w+(?!"))=
# \n        "$1":\s
