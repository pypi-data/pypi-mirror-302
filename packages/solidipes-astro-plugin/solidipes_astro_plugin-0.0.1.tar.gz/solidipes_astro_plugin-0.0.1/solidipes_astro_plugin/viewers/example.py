import streamlit as st
from IPython.display import display
from solidipes.loaders.data_container import DataContainer
from solidipes.viewers import backends as viewer_backends
from solidipes.viewers.viewer import Viewer


class Example(Viewer):
    """Viewer for text"""

    def __init__(self, data=None):
        self.compatible_data_types = [str]
        #: Text to display
        self.text = ""
        super().__init__(data)

    def add(self, data):
        """Append text to the viewer"""
        self.check_data_compatibility(data)

        if isinstance(data, DataContainer):
            self.text += data.text

        elif isinstance(data, str):
            self.text += data

    def show(self):
        if viewer_backends.current_backend == "jupyter notebook":
            display(self.text)

        elif viewer_backends.current_backend == "streamlit":
            st.text(self.text)

        else:  # python
            print(self.text)
