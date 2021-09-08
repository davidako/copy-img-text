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
    """
    Map iso1 language codes to iso2.

    :return Dict of two-letter lang codes mapped to three-letter codes.
    """
    lang_map = {}
    for lang in pycountry.languages:
        alpha2 = getattr(lang, 'alpha_2', None)
        alpha3 = getattr(lang, 'alpha_3', None)

        if alpha2 is not None and alpha3 is not None:
            lang_map[alpha2] = alpha3

    return lang_map


def get_default_lang():
    """
    Allow users to set language as an env variable. Otherwise retrieve system lang.

    :return Language code.
    """
    env_lang = os.getenv('IMG_LANG')
    if env_lang is not None and len(env_lang) != 3:
        print("Please use three-digit language code, e.g. eng, deu etc.")
    else:
        return env_lang

    return lang_code_map()[locale.getdefaultlocale()[0][:2]]


def copy_image_text():
    """Extract text from an image and copy to clipboard."""

    cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    image = cb.wait_for_image()
    clip_image = 'clipimage.png'

    if image is not None:
        image.savev(clip_image, "png", "", "")
        # TODO maybe in the future add an option for showing the copied text in a popup?
        # subprocess.call(["xdg-open", clip_image])

        text = pytesseract.image_to_string(Image.open(clip_image), get_default_lang())
        copy_gtk(text)

        # Remove the temporary image.
        os.remove(clip_image)
    else:
        print("No image in clipboard found")
        sys.exit(1)
