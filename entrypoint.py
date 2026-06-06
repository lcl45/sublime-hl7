import sublime
import sublime_plugin

from .hl7.hl7_parser import is_parseable_hl7


class Hl7StatusListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        view.settings().clear_on_change("hl7_syntax_watch")
        view.settings().add_on_change("hl7_syntax_watch", lambda: _on_syntax_changed(view))
        file_name = view.file_name()
        if file_name is not None and file_name.endswith(".hl7"):
            _update_view(view)

    def on_modified_async(self, view):
        if not _is_hl7_candidate(view):
            return
        _update_view(view)


def _on_syntax_changed(view):
    if view.match_selector(0, "source.hl7"):
        _update_view(view)


def _is_hl7_candidate(view):
    if view.match_selector(0, "source.hl7"):
        return True
    file_name = view.file_name()
    return file_name is not None and file_name.endswith(".hl7")


def _update_view(view):
    text = view.substr(sublime.Region(0, view.size()))
    if is_parseable_hl7(text):
        if not view.match_selector(0, "source.hl7"):
            view.assign_syntax("Packages/HL7/HL7.sublime-syntax")
        view.erase_status("hl7")
    else:
        if view.match_selector(0, "source.hl7"):
            view.assign_syntax("Packages/Text/Plain text.tmLanguage")
        view.set_status("hl7", "Not a valid HL7 message")
