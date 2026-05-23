import sublime
import sublime_plugin

from .hl7.hl7_parser import is_parseable_hl7


class Hl7StatusListener(sublime_plugin.EventListener):
    def on_selection_modified_async(self, view):
        """called when selecting things inside the editor"""

        if not view.match_selector(0, "source.hl7"): # no need to re-check the text content here
            return

    def on_modified_async(self, view):
        """when updating text"""
        
        if not can_handle_view(view):
            return

    def on_activated(self, view):        
        """called when a view is focused. on_load seems to not be called if the file was already opened"""

        if not can_handle_view(view):
            return


def can_handle_view(view):
    text = view.substr(sublime.Region(0, view.size()))

    if is_parseable_hl7(text):
        view.assign_syntax("Packages/HL7/HL7.sublime-syntax")
        view.erase_status("hl7")
        return True
    else:
        view.assign_syntax("Packages/Text/Plain text.tmLanguage") # not sure about this. will this always exist?
        view.set_status("hl7", "Not a valid HL7 message")
        return False
