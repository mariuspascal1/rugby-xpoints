# Configuration file for the Sphinx documentation builder.

import os
import sys
from unittest.mock import MagicMock

# Permet à Sphinx de trouver le package rugby_xpoints/
sys.path.insert(0, os.path.abspath("../.."))

# Mock modules that require a GUI or external dependencies
MOCK_MODULES = [
    "tkinter",
    "tkinter.simpledialog",
    "_tkinter",
    "matplotlib",
    "matplotlib.pyplot",
    "matplotlib.image",
]
for module in MOCK_MODULES:
    sys.modules[module] = MagicMock()

# -- Project information -----------------------------------------------------
project = "rugby-xpoints"
author = "Marius Pascal"
copyright = "2025, Marius Pascal"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",  # Génère la doc depuis les docstrings
    "sphinx.ext.napoleon",  # Support Google/NumPy docstrings
]

templates_path = ["_templates"]
exclude_patterns = []

language = "en"  # ou 'fr' si tu veux, mais PAS autodoc ici

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]
