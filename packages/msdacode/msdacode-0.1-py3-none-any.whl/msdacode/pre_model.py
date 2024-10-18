def inception():
    code = '''
import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the pre-trained InceptionV3 model
model = InceptionV3(weights='imagenet')

# Load and preprocess the image
img_path = 'download.jpeg'  # Replace with your image path
img = image.load_img(img_path, target_size=(299, 299))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# Make predictions
predictions = model.predict(img_array)
decoded_predictions = decode_predictions(predictions, top=3)[0]
print(decoded_predictions[0][1])
    '''
    print(code)


def resnet():
    code= '''
import torch
from torchvision import models, transforms
from PIL import Image
import json

# Load the ImageNet class labels
!wget https://raw.githubusercontent.com/fitbyit/InceptionImage/main/imagenet-simple-labels.json
with open('imagenet-simple-labels.json', 'r') as f:
    labels = json.load(f)

# Load a pre-trained ResNet model
model = models.resnet50(pretrained=True)
model.eval()  # Set the model to evaluation mode

# Define the image transformations
preprocess = transforms.Compose([ transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load and preprocess an image
def process_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = preprocess(image)
    return image.unsqueeze(0)  # Add a batch dimension

# Predict the class of the image
def predict(image_path):
    image = process_image(image_path)
    with torch.no_grad():
        outputs = model(image)
    _, predicted_class = torch.max(outputs, 1)
    return predicted_class.item()

image_path = 'download.jpeg'  # Replace with your image path
class_label = labels[predict(image_path)]
print(f'Predicted class label:',class_label)
    '''

    print(code)