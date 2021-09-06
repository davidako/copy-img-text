import gi

from cp_img_txt.cpimgtxt import copy_image_text

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf


def test_copy_img_text():
    """
    Make sure text is extracted properly from an image,
    """

    expected_text = "Nulla quis lorem ut libero malesuada feugiat. Pellentesque in ipsum id orci porta dapibus."

    # First copy the test image to clipboard.
    display = Gdk.Display.get_default()
    image = Pixbuf.new_from_file('tests/test-img.png')
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_image(image)
    clipboard.store()

    # Copy text from image to clipboard.
    copy_image_text()

    # Get the extracted text from clipboard and compare to the expected text.
    # Just in case remove a trailing newline.
    copied_text = clipboard.wait_for_text().rstrip()

    assert str(copied_text) == str(expected_text)
