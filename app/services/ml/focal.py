from photoholmes.methods.focal import Focal, focal_preprocessing
from photoholmes.utils.image import read_image

weight_dir = "/home/nhat82125/photoholmes/weights/focal"
path_to_weights = {"ViT": f"{weight_dir}/VIT_weights.pth",
                   "HRNet": f"{weight_dir}/HRNET_weights.pth"}

FocalModel = Focal(
    weights=path_to_weights,
)

device = "cuda"
FocalModel.to_device(device)


def focal(image_path):
    image = read_image(image_path)
    image_data = {"image": image}

    model_input = focal_preprocessing(**image_data)

    output = FocalModel.predict(**model_input)

    output = output.cpu()

    normalized_output = (output - output.min()) / (output.max() - output.min())
    return (normalized_output * 255).byte().numpy()
