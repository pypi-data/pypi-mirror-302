def cnnfilter():
    code ='''
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imshow, imread    #pip install scikit-image
from skimage.color import rgb2yuv, rgb2hsv, rgb2gray, yuv2rgb, hsv2rgb
from scipy.signal import convolve2d

# Load and display the image
img = Image.open("C:/Users/fizap/Downloads/DL-main/image.png")
plt.imshow(img)
plt.axis('off')  # Hide the axis for a cleaner look
plt.show()

#filter matric
sharpen =np.array([[0,-1,0],
                  [-1,5,-1],
                  [0,-1,0]])

blur = np.array([[0.11,0.11,0.11],
                    [0.11,0.11,0.11],
                    [0.11,0.11,0.11]])


vertical = np.array([[-1,0,1],
                    [-2,0,2],
                    [-1,0,1]])


gaussian = (1/16.0) * np.array([[1,2,1],
                                [2,4,2],
                                [1,2,1]])

#plotting the filters

fig,ax = plt.subplots(1,4, figsize = (8,6))
ax[0].imshow(sharpen, cmap='gray')
ax[0].set_title(f'Sharpen', fontsize=18)

ax[1].imshow(blur, cmap='gray')
ax[1].set_title(f'Blur', fontsize=18)

ax[2].imshow(vertical, cmap='gray')
ax[2].set_title(f'Vertical', fontsize=18)

ax[3].imshow(gaussian, cmap='gray')
ax[3].set_title(f'Gaussian', fontsize=18)

#Grayscaling Image
spong_gray = rgb2gray(img)
plt.figure(num=None, figsize=(6,4), dpi=80)
imshow(spong_gray)

#Function for applying filters
def multi_convolver(image, kernel, iterations):
  for i in range(iterations):
    image = convolve2d(image, kernel, 'same',
                       boundary = 'fill', fillvalue = 0)
  return image

convolved_image = multi_convolver(spong_gray, blur, 20)

plt.figure(num=None, figsize=(6,4), dpi=80)
imshow(convolved_image);

#Function for applying filters
def multi_convolver(image, kernel, iterations):
  for i in range(iterations):
    image = convolve2d(image, kernel, 'same',
                       boundary = 'fill', fillvalue = 0)
  return image

convolved_image = multi_convolver(spong_gray, sharpen, 1)

plt.figure(num=None, figsize=(6,4), dpi=80)
imshow(convolved_image)

#For colored Image
def convolver_rgb(image, kernel, iterations = 1):
  convolved_image_r = multi_convolver(image[:,:,0], kernel, iterations)
  convolved_image_g = multi_convolver(image[:,:,1], kernel, iterations)
  convolved_image_b = multi_convolver(image[:,:,2], kernel, iterations)

  reformed_image = np.dstack((np.rint(abs(convolved_image_r)),
                              np.rint(abs(convolved_image_g)),
                              np.rint(abs(convolved_image_b))))/255

  fig,ax = plt.subplots(1,3, figsize = (8,6))

  ax[0].imshow(abs(convolved_image_r), cmap='Reds')
  ax[0].set_title(f'Red', fontsize=15)

  ax[1].imshow(abs(convolved_image_g), cmap='Greens')
  ax[1].set_title(f'Green', fontsize=18)

  ax[2].imshow(abs(convolved_image_b), cmap='Blues')
  ax[2].set_title(f'Blue', fontsize=18)

  return np.array(reformed_image*255).astype(np.uint8)

#Can add different filters (defined above) here
spong = np.array(img)  # Convert to NumPy array
convolved_rgb_gauss = convolver_rgb(spong, blur ,1)

plt.imshow(convolved_rgb_gauss,vmin=0,vmax=255);    
    '''
    print(code)


def dataaug():
    code = '''
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

# Create an instance of ImageDataGenerator with desired augmentation options
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Load an image from file
img = load_img('download.jpeg')  
x = img_to_array(img)                       
x = np.expand_dims(x, axis=0)               # Reshape to (1, height, width, channels)

# Generate and display augmented images
i = 0
for batch in datagen.flow(x, batch_size=1):
    plt.imshow(img_to_array(batch[0]).astype('uint8'))  
    plt.axis('off')                                    
    plt.show()
    i += 1
    if i > 20: 
        break
    '''
    print(code)

def cnnmaxpool():
    code = '''
#cnn paramater & max pooling
from keras.models import Sequential
from keras.layers import Conv2D
model = Sequential()
model.add(Conv2D(32, input_shape=(28,28,3),
                 kernel_size = (5,5),
                 padding='same',
                 use_bias=False))
model.add(Conv2D(17, (3,3), padding='same', use_bias=False))
model.add(Conv2D(13, (3,3), padding='same', use_bias=False))
model.add(Conv2D(7, (3,3), padding='same', use_bias=False))
model.compile(loss = 'categorical_crossentropy', optimizer='adam')
model.summary()


#MaxPooling on model parameters
import tensorflow as tf
x = tf.constant([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])
x = tf.reshape(x, [1, 3, 3, 1])
max_pool_2d = tf.keras.layers.MaxPooling2D(pool_size=(2, 2),
                                           strides=(1, 1), padding='valid')
max_pool_2d(x)
    '''
    print(code)


def dropout():
    code = '''
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt

# Load and preprocess the data
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1)).astype('float32') / 255
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1)).astype('float32') / 255
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

# Build the CNN model
def create_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.25))  # Dropout layer
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.25))  # Dropout layer
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))  # Dropout layer
    model.add(layers.Dense(10, activation='softmax'))
    return model

model = create_model()
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(x_train, y_train, epochs=10, batch_size=128, validation_split=0.2)

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test accuracy:', test_acc)

# Plot training & validation accuracy and loss values
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()
    '''
    print(code)