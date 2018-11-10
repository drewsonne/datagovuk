import pkg_resources


class NoProcessorAvailable(Exception): pass



class PluginController(object):
    plugins = None

    def find_processor(self, filetype, resource_name):
        self.load_plugins()

        specific = filetype + '.' + resource_name
        general = filetype

        if specific in self.plugins:
            return self.plugins[specific]
        if general in self.plugins:
            return self.plugins[general]

        raise NoProcessorAvailable()

    def load_plugins(self):
        if self.plugins is None:
            self.plugins = {}
            for entry_point in pkg_resources.iter_entry_points('datagovuk.plugins.processors'):
                plugin = entry_point.load()()
                for handler in plugin.handlers:
                    self.plugins[handler] = plugin


plugins = PluginController()
