from dsplayer.plugin_system.plugin_interface import PluginInterface

class TestPlugin(PluginInterface):
    def __init__(self):
        super().__init__()
        self.name = "TestPlugin"
        self.version = "1.0"
        self.author = "Test Author"
        self.description = "This is a test plugin"

    def debug(self):
        mode = True

    def on_plugin_load(self) -> None:
        print("TestPlugin loaded")

    def on_plugin_unload(self) -> None:
        print("TestPlugin unloaded")

    def get_plugin_name(self) -> str:
        print(f"Plugin name: {self.name}")
        return self.name

    def get_plugin_type(self) -> str:
        return "addon"

    def plugin_sum(self, a, b):
        return a + b