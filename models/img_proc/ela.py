from PIL import Image, ImageChops, ImageEnhance
from models.base import ForgeryDetector


class ErrorLevelAnalysis(ForgeryDetector):
    def detect(self, img_path):
        ela_img = self.convert_to_ela_img(img_path)
        return ela_img

    def convert_to_ela_img(self, img_path, quality=75, scale_factor=350.0):
        original_img = Image.open(img_path).convert('RGB')

        resaved_file_name = './ela_resaved_img.jpg'
        original_img.save(resaved_file_name, 'JPEG', quality=quality)
        resaved_img = Image.open(resaved_file_name)

        ela_img = ImageChops.difference(original_img, resaved_img)

        extrema = ela_img.getextrema()
        max_difference = max([pix[1] for pix in extrema])
        max_difference = max_difference if max_difference > 0 else 1

        scale = scale_factor / max_difference
        ela_img = ImageEnhance.Brightness(ela_img).enhance(scale)

        return ela_img
