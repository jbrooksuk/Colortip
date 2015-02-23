import sublime_plugin, sublime
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

class ColortipCommand(sublime_plugin.EventListener):
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

        for region in view.sel():
            region_row, region_col = view.rowcol(region.begin())

            colors = self.generate_colors()

            view.show_popup(''.join(colors), location=-1, max_width=600, on_navigate=DisplayColortipCommand.handle_selected_color)

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

        colors.append('<style>body { margin:0; }</style>')

        for rgb in self.cycle(analogicSteps):
            hex_code = '#%02x%02x%02x' % rgb
            colors.append('<div style="display:inline-block; background-color:{0};"><a href="{0}" style="color:{0}; float: left; width: 20px; height: 20px; display: block;">HIYA</a></div>'.format(hex_code))

        return colors

    def handle_selected_color(self, color):
        self.view.run_command("insert", { "characters": color })
        self.view.hide_popup()
