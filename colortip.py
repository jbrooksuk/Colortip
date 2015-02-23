import sublime_plugin, sublime
import re
from time import time

wheel = [
    (255,0,0),
    (255,51,0),
    (255,102,0),
    (255,128,0),
    (255,153,0),
    (255,178,0),
    (255,204,0),
    (255,229,0),
    (255,255,0),
    (204,255,0),
    (153,255,0),
    (51,255,0),
    (0,204,0),
    (0,178,102),
    (0,153,153),
    (0,102,178),
    (0,51,204),
    (25,25,178),
    (51,0,153),
    (64,0,153),
    (102,0,153),
    (153,0,153),
    (204,0,153),
    (229,0,102),
]

class ColortipEventCommand(sublime_plugin.EventListener):
    colors = None

    def on_activate(self, view):
        sublime.set_timeout(lambda:self.run(view, 'activated'), 0)

    def on_selection_modified(self, view):
        now = time()
        sublime.set_timeout(lambda:self.run(view, 'selection_modified'), 0)

    def run(self, view, where):
        view_settings = view.settings()
        if view_settings.get('is_widget'):
            return

        # If we have multiple selections, don't show anything.
        if len(view.sel()) > 1:
            return
        else:
            view.hide_popup();

        scopes = [
            "constant.other.color.rgb-value.css",
            "meta.property-value.css"
        ]

        if not self.colors:
            self.colors = self.generate_colors()

        scope_name = view.scope_name(view.sel()[0].b)

        for scope in scopes:
            if (scope+'') in scope_name:
                if '#' in view.substr(view.word(view.sel()[0])):
                    view.show_popup(''.join(self.colors), sublime.COOPERATE_WITH_AUTO_COMPLETE, location=-1, max_width=500, on_navigate=ColortipTextCommand.handle_selected_color)

    def cycle(self, steps):
        for n in range(len(wheel)):
            yield wheel[steps[n]]

    def generate_colors(self):
        # Map of colors
        colors = []

        analogicOffsets = [0, 12, 18, 6, 1, 13, 19, 7]
        analogicSteps = []

        for offset in analogicOffsets:
            analogicSteps.append(offset)
            analogicSteps.append((offset + 2) % 24)
            analogicSteps.append((offset + 4) % 24)

        colors.append('<style>body { margin:0; padding: 0; }</style>')

        for rgb in self.cycle(analogicSteps):
            hex_code = '#%02x%02x%02x' % rgb
            colors.append('<span style="background-color: {0}; padding: 0; margin: 0;"><a href="{0}" style="color:{0}; width: 20px; height: 20px;">██</a></span>'.format(hex_code))

        return colors

class ColortipTextCommand(sublime_plugin.TextCommand):
    def handle_selected_color(self, color):
        self.view.run_command("insert", { "characters": color })
        self.view.hide_popup()
