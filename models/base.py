from abc import ABC, abstractmethod


class ForgeryDetector(ABC):
    @abstractmethod
    def detect(self, img_path):
        pass
