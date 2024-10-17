from solidipes.loaders.file import File


class Example(File):
    """Text file"""

    supported_mime_types = {"text/plain": "txt"}

    def __init__(self, **kwargs):
        from ..viewers.example import Example as ExampleViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [ExampleViewer]

    @File.loadable
    def text(self):
        text = ""
        with open(self.file_info.path, "r") as f:
            text = f.read()
        return text
