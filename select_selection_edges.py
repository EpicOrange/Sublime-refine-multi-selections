import sublime, sublime_plugin

class SelectSelectionEdgesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selections = self.view.sel()
        if len(selections) > 0:
            positions = set()
            for i in selections:
                positions.add(i.a)
                positions.add(i.b)
            selections.clear()
            for i in positions:
                self.view.sel().add(sublime.Region(i, i))