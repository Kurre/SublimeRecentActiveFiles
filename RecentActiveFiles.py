import sublime, sublime_plugin
import os

class RecentActiveFilesEventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        if view.file_name():
            view.window().run_command("recent_active_files", { "file_name": view.file_name() })

class RecentActiveFilesCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)
        self.recent_active_files = []

    def unshift(self, file_name):
        if file_name in self.recent_active_files:
            self.recent_active_files.remove(file_name)
        self.recent_active_files.insert(0, file_name)

    def path_form_project(self, path):
        for folder in self.window.folders():
            path = path.replace(folder + '/', '', 1)
        return path

    def get_recent_file_by_name (self, file_name):
        return next( ( f for f in self.recent_active_files if f == file_name ), None);

    def run(self, file_name=None):
        if file_name:
            self.unshift(file_name)
        else:
            items = [[os.path.basename(f), self.path_form_project(f), f] for f in self.recent_active_files]

            if len(items) > 0:
                current = items.pop(0)

            def on_done(index):
                if index >= 0:
                    self.window.open_file(self.get_recent_file_by_name(items[index][2]))
                else:
                    if len(self.recent_active_files) > 0:
                        self.window.open_file(self.get_recent_file_by_name(current[2]))

            def on_highlight(index):
                if index >= 0:
                    self.window.open_file(self.get_recent_file_by_name(items[index][1]), sublime.TRANSIENT)

            self.window.show_quick_panel(items, on_done, 0, -1, on_highlight)
