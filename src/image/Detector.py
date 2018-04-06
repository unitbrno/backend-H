

class Detector:

    image = []

    def __init__(self, path):
        self.load_image(path)
        self.threshold()

    def load_image(self, path):
        pass

    def threshold(self):
        pass

    @property
    def balls(self):
        return
