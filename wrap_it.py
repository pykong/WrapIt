import sublime
import sublime_plugin
import re

SETTINGS_FILE = 'wrap_it.sublime-settings'
prefs = sublime.load_settings(SETTINGS_FILE)
DEFINITIONS = prefs.get('definitions')
SELECTION_TAG = "<sel>"


def detect_syntax(window):
    """ Detects syntax and returns wrappers. """
    active_syntax = window.active_view().settings().get('syntax')
    for language in DEFINITIONS:
        if active_syntax in language["syntaxes"]:
            active_wrappers = [w
                               for w in language["wrappers"]
                               if w["name"] and w["template"]]

            if not active_wrappers:
                window.status_message('WrapIt: Current Syntax NOT Supported')
                return

            opts = [[w["name"], w["description"]] for w in active_wrappers]
            templates = [w["template"] for w in active_wrappers]

            return opts, templates


class WrapItCommand(sublime_plugin.TextCommand):
    def run(self, edit, template_name):
        _, templates = detect_syntax(self.window)
        try:
            template = templates[template_name]
        except KeyError:
            msg = "WrapIt:: Template: {} not defined or wrong syntax."
            self.view.active_window.status_message(msg.format(template_name))
        else:
            self.view.run_command('wrap', {"template": template})


class WrapItMenuCommand(sublime_plugin.WindowCommand):
    """ Detect current file syntax and return the menu chosen template.
    An unsupported syntax will trigger a status bar warning. """

    def run(self):
        opts, self.templates = detect_syntax(self.window)
        self.window.show_quick_panel(opts, self.on_done)

    def on_done(self, opt):
        """ Callback for quick panel, calls wrap command. """
        try:
            template = self.templates[opt]
        except IndexError:
            self.window.status_message('WrapIt: Sublime Wrap Cancelled.')
        except KeyError:
            msg = "WrapIt: Definitions malformed or template missing."
            self.window.status_message(msg)
        else:
            active_view = self.window.active_view()
            active_view.run_command('wrap', {"template": template})


class WrapCommand(sublime_plugin.TextCommand):
    def get_indent(self, text):
        """ Returns smallest indentation (distance from line start). """
        spaces = []
        tabs = []

        for line in text.splitlines():
            space_match = re.search("^ +", line)
            tab_match = re.search("^\t+", line)

            if space_match:
                spaces.append(space_match.group(0))

            if tab_match:
                tabs.append(tab_match.group(0))

        if spaces:
            indent = ' ' * len(min(spaces))
        elif tabs:
            indent = '\t' * len(min(tabs))
        else:
            indent = ''

        return indent

    def fill_template(self, text, template, indent, tab_size):
        tab_sel_tag = "\t" + SELECTION_TAG

        # if selection should be indentend and is not already:
        if not re.search(tab_sel_tag, template):
            tab_sel_tag = SELECTION_TAG
        else:  # else indent one tab_size
            spacer = " " * tab_size
            lines = text.splitlines()
            lines = [spacer + l.strip() for l in lines]
            text = "\n".join(lines)

        return re.sub(tab_sel_tag, text, template)

    def run(self, edit, template):
        for sel in self.view.sel():
            # window = sublime.active_window()
            # view = window.active_view()
            settings = self.view.settings()

            tab_size = 4
            if settings.has("translate_tabs_to_spaces"):
                tab_size = settings.get("tab_size", 4)

            region = self.view.line(sel)
            text = self.view.substr(region)

            indent = self.get_indent(text)

            filled_template = self.fill_template(
                text, template, indent, tab_size)

            lines = [indent + l for l in filled_template.splitlines() if l]

            new_text = '\n'.join(lines)

            if template.startswith('\n'):
                new_text = '\n' + new_text

            self.view.erase(edit, region)
            self.view.run_command('insert_snippet', {'contents': new_text})
