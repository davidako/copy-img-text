"""
 Copy text from a screenshot.
"""

import os
import sys
import gi
import pytesseract
from PIL import Image
import locale

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import pycountry


def copy_gtk(text):
    """Copy text to clipboard."""
    display = Gdk.Display.get_default()
    clipboard = Gtk.Clipboard.get_default(display)
    clipboard.set_text(text, -1)
    clipboard.store()


def lang_code_map():
    """Map iso1 language codes to iso2."""
    lang_map = {}
    for lang in pycountry.languages:
        alpha2 = getattr(lang, 'alpha_2', None)
        alpha3 = getattr(lang, 'alpha_3', None)

        if alpha2 is not None and alpha3 is not None:
            lang_map[alpha2] = alpha3

    return lang_map


def get_default_lang():
    """Guess language based on configured system language."""
    return lang_code_map()[locale.getdefaultlocale()[0][:2]]


def copy_image_text():
    """Extract text from an image and copy to clipboard."""

    cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    image = cb.wait_for_image()
    clip_image = 'clipimage.png'

    if image is not None:
        image.savev(clip_image, "png", "", "")
        # subprocess.call(["xdg-open", clip_image])

        default_lang = get_default_lang()

        text = pytesseract.image_to_string(Image.open(clip_image), default_lang)
        copy_gtk(text)

        # Remove the temporary image.
        os.remove(clip_image)
    else:
        print("No image in clipboard found")
        sys.exit(1)

