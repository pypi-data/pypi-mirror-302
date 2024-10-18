def dl():
    num = int(input())
    if(num==1):
        print('''
#Binary Class Classification 
import numpy as np
 
# Define activation functions and their derivatives
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
 
def sigmoid_derivative(x):
    return x * (1 - x)
 
# Mean squared error
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
 
# Inputs and expected outputs for XOR
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
outputs = np.array([[0], [1], [1], [0]])
 
# Initialize weights and biases
np.random.seed(42)
weights_input_hidden = np.random.rand(2, 2)
bias_hidden = np.random.rand(2)
weights_hidden_output = np.random.rand(2, 1)
bias_output = np.random.rand(1)
 
# Training parameters
learning_rate = 0.1
epochs = 10000
 
# Training loop
for epoch in range(epochs):
    # Forward pass
    hidden_output = sigmoid(np.dot(inputs, weights_input_hidden) + bias_hidden)
    final_output = sigmoid(np.dot(hidden_output, weights_hidden_output) + bias_output)
 
    # Compute loss
    loss = mse(outputs, final_output)
 
    # Backpropagation
    error_output = final_output - outputs
    gradient_output = error_output * sigmoid_derivative(final_output)
    error_hidden = gradient_output.dot(weights_hidden_output.T)
    gradient_hidden = error_hidden * sigmoid_derivative(hidden_output)
 
    # Update weights and biases
    weights_hidden_output -= learning_rate * hidden_output.T.dot(gradient_output)
    bias_output -= learning_rate * np.mean(gradient_output, axis=0)
    weights_input_hidden -= learning_rate * inputs.T.dot(gradient_hidden)
    bias_hidden -= learning_rate * np.mean(gradient_hidden, axis=0)
 
    # Print loss every 1000 epochs
    if (epoch + 1) % 1000 == 0:
        print(f"Epoch {epoch + 1} Loss {loss:.6f}")
 
#compute the output for each input pair after training
results=[]
for input_pair in inputs:
    hidden_input=np.dot(input_pair,weights_input_hidden)+bias_hidden
    hidden_output=sigmoid(hidden_input)
    final_input=np.dot(hidden_output,weights_hidden_output)+bias_output
    final_output=sigmoid(final_input)
    results.append((input_pair,np.round(final_output[0],2)))
 
print(results)
''')
    elif(num==2):
        print('''
# MultiClass Classification
 
import numpy as np
 
# Activation Functions
def relu(x):
    return np.maximum(0, x)
 
def relu_derivative(x):
    return (x > 0).astype(float)
 
def softmax(x):
    e_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
    return e_x / e_x.sum(axis=1, keepdims=True)
 
def log_loss(y, y_hat):
    return -np.sum(y * np.log(y_hat))
 
# Data Initialization
x = np.array([0.8, 0.6, 0.7]).reshape(1, -1)
y = np.array([0, 1, 0]).reshape(1, -1)
w1 = np.random.rand(3, 3)
b1 = np.random.rand(1, 3)
w2 = np.random.rand(3, 3)
b2 = np.random.rand(1, 3)
 
# Training Parameters
learning_rate = 0.1
num_epochs = 10
 
for epoch in range(num_epochs):
    # Forward Pass
    H1 = np.dot(x, w1) + b1
    A1 = relu(H1)
    H2 = np.dot(A1, w2) + b2
    a2 = softmax(H2)
    loss = log_loss(y, a2)
 
    # Backpropagation
    der_loss_w2 = np.outer(A1, a2 - y)
    der_loss_b2 = a2 - y
    der_loss_b1 = np.dot(a2 - y, w2.T) * relu_derivative(H1)
    der_loss_w1 = np.outer(x, der_loss_b1)
 
    # Weight Updates
    w2 -= learning_rate * der_loss_w2
    b2 -= learning_rate * der_loss_b2
    w1 -= learning_rate * der_loss_w1
    b1 -= learning_rate * np.mean(der_loss_b1, axis=0)
 
    # Print loss for this epoch
    print(f"Epoch {epoch + 1}: Loss = {loss:.6f}")
 
# Print final weights and biases
print("Final weights and biases:")
print("w1:", w1)
print("b1:", b1)
print("w2:", w2)
print("b2:", b2)
''')
    elif(num==3):
        print('''
#1) Function TO Perform Batch Gradient Descent
print('Function TO Perform Batch Gradient Descent')
import numpy as np
import matplotlib.pyplot as plt
 
# Generate data
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)
 
# Add a column of ones to X for the bias term
X_b = np.c_[np.ones((100, 1)), X]
 
# Batch Gradient Descent function
def batch_gradient_descent(X, y, learning_rate=0.1, n_iteration=1000):
    m = len(y)
    theta = np.random.randn(2, 1)  # Initialize theta randomly
    print('Initial Theta: ', theta)
    
    for iteration in range(n_iteration):
        gradients = 2/m * X.T.dot(X.dot(theta) - y)
        theta = theta - learning_rate * gradients
    
    return theta
 
# Perform Batch Gradient Descent
theta_bgd = batch_gradient_descent(X_b, y)
print('Final Theta (from BGD): ', theta_bgd)
 
# Plot the data and the linear regression line
plt.figure(figsize=(8, 6))
plt.plot(X, y, 'b.', label='Data points')  # Plot original data
 
# Use the computed theta to plot the regression line
X_new = np.array([[0], [2]])  # X values for the line (covering the range of the data)
X_new_b = np.c_[np.ones((2, 1)), X_new]  # Add a column of ones for the bias term
y_predict = X_new_b.dot(theta_bgd)  # Predict y values using the model
 
plt.plot(X_new, y_predict, 'r-', label='Predicted line')  # Plot the regression line
plt.xlabel('X')
plt.ylabel('y')
plt.title('Linear Regression using Batch Gradient Descent')
plt.legend()
plt.grid(True)
plt.show()
''')
    elif(num==4):
        print('''
#2) # Function To perfomr Stochastic batch gradient descent
print('Function To perfomr Stochastic batch gradient descent')
import numpy as np
import matplotlib.pyplot as plt
 
# Generate data
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)
 
# Add a column of ones to X for the bias term
X_b = np.c_[np.ones((100, 1)), X]
 
# Stochastic Gradient Descent function
def stochastic_gradient_descent(X, y, learning_rate=0.1, n_epochs=50):
    m = len(y)
    theta = np.random.randn(2, 1)  # Initialize theta randomly
    for epoch in range(n_epochs):
        for i in range(m):
            random_index = np.random.randint(m)
            xi = X[random_index:random_index + 1]
            yi = y[random_index:random_index + 1]
            gradients = 2 * xi.T.dot(xi.dot(theta) - yi)
            theta = theta - learning_rate * gradients
    return theta
 
# Perform Stochastic Gradient Descent
theta_sgd = stochastic_gradient_descent(X_b, y)
print('Final Theta (from SGD): ', theta_sgd)
 
# Plot the data and the linear regression line
plt.figure(figsize=(8, 6))
plt.plot(X, y, 'b.', label='Data points')  # Plot original data
 
# Use the computed theta to plot the regression line
X_new = np.array([[0], [2]])  # X values for the line (covering the range of the data)
X_new_b = np.c_[np.ones((2, 1)), X_new]  # Add a column of ones for the bias term
y_predict = X_new_b.dot(theta_sgd)  # Predict y values using the model
 
plt.plot(X_new, y_predict, 'r-', label='Predicted line (SGD)')  # Plot the regression line
plt.xlabel('X')
plt.ylabel('y')
plt.title('Linear Regression using Stochastic Gradient Descent')
plt.legend()
plt.grid(True)
plt.show()
''')
    elif(num==5):
        print('''
#3) # funtion to perform mini batch
print('function to perform mini batch')
 
import numpy as np
import matplotlib.pyplot as plt
 
# Generate data
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)
 
# Add a column of ones to X for the bias term
X_b = np.c_[np.ones((100, 1)), X]
 
# Mini-Batch Gradient Descent function
def mini_batch_gradient(X, y, learning_rate=0.1, n_iterations=50, batch_size=20):
    m = len(y)
    theta = np.random.randn(2, 1)  # Initialize theta randomly
    for iteration in range(n_iterations):
        shuffled_indices = np.random.permutation(m)  # Shuffle the dataset
        X_shuffled = X[shuffled_indices]
        y_shuffled = y[shuffled_indices]
        for i in range(0, m, batch_size):
            xi = X_shuffled[i:i + batch_size]
            yi = y_shuffled[i:i + batch_size]
            gradients = 2 / len(xi) * xi.T.dot(xi.dot(theta) - yi)
            theta = theta - learning_rate * gradients
    return theta
 
# Perform Mini-Batch Gradient Descent
theta_mbgd = mini_batch_gradient(X_b, y)
print('Final Theta (from MBGD): ', theta_mbgd)
 
# Plot the data and the linear regression line
plt.figure(figsize=(8, 6))
plt.plot(X, y, 'b.', label='Data points')  # Plot original data
 
# Use the computed theta to plot the regression line
X_new = np.array([[0], [2]])  # X values for the line (covering the range of the data)
X_new_b = np.c_[np.ones((2, 1)), X_new]  # Add a column of ones for the bias term
y_predict = X_new_b.dot(theta_mbgd)  # Predict y values using the model
 
plt.plot(X_new, y_predict, 'r-', label='Predicted line (MBGD)')  # Plot the regression line
plt.xlabel('X')
plt.ylabel('y')
plt.title('Linear Regression using Mini-Batch Gradient Descent')
plt.legend()
plt.grid(True)
plt.show()
''')
    elif(num==6):
        print('''
# 4) gradient descent with momentum 
print('gradient descenet with momentum')
import numpy as np
import matplotlib.pyplot as plt
 
# Define the gradient descent with momentum function
def gradient_descent_with_momentum(X, y, theta, learning_rate, gamma, num_iterations):
    m = len(y)
    velocity = np.zeros_like(theta)
    
    for i in range(num_iterations):
        gradient = (1/m) * X.T.dot(X.dot(theta) - y)
        velocity = gamma * velocity + learning_rate * gradient
        theta = theta - velocity
    return theta
 
# Generate data for visualization
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)
 
# Flatten y to avoid broadcasting error
y = y.flatten()
 
# Add bias term (ones column)
X_b = np.c_[np.ones((100, 1)), X]
 
# Initialize theta to zeros
theta = np.zeros(X_b.shape[1])
 
# Define parameters
learning_rate = 0.1
gamma = 0.9
num_iterations = 1000
 
# Perform gradient descent with momentum
theta_momentum = gradient_descent_with_momentum(X_b, y, theta, learning_rate, gamma, num_iterations)
print("Final Theta (from GD with Momentum):", theta_momentum)
 
# Plot the data and the linear regression line
plt.figure(figsize=(8, 6))
plt.plot(X, y, 'b.', label='Data points')  # Plot the original data points
 
# Use the final theta to plot the predicted line
X_new = np.array([[0], [2]])  # X values for the line
X_new_b = np.c_[np.ones((2, 1)), X_new]  # Add bias term
y_predict = X_new_b.dot(theta_momentum)  # Predicted values
 
plt.plot(X_new, y_predict, 'r-', label='Predicted line (GD with Momentum)')  # Plot the regression line
plt.xlabel('X')
plt.ylabel('y')
plt.title('Linear Regression using Gradient Descent with Momentum')
plt.legend()
plt.grid(True)
plt.show()
''')
    elif(num==7):
        print('''
# 5) Adagrad 
import numpy as np
import matplotlib.pyplot as plt
 
# Generate synthetic data
np.random.seed(42)  # For reproducibility
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)
X_b = np.c_[np.ones((100, 1)), X]  # Add bias term
 
# Hyperparameters
learning_rate = 0.1
epsilon = 1e-8
num_iterations = 1000
 
# Initialize parameters
theta = np.random.randn(2, 1)
gradient_accum = np.zeros((2, 1))
 
# Adagrad optimization
for iteration in range(num_iterations):
    gradients = 2/len(X_b) * X_b.T.dot(X_b.dot(theta) - y)
    gradient_accum += gradients ** 2  # Accumulate squared gradients
    adjusted_gradients = gradients / (np.sqrt(gradient_accum) + epsilon)
    theta -= learning_rate * adjusted_gradients
 
print("Theta:", theta)
 
# Plotting the results
plt.scatter(X, y, label='Data')
plt.plot(X, X_b.dot(theta), color='red', linewidth=2, label='Adagrad')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()
''')
    elif(num==8):
        print('''
# RMSprop
import numpy as np
import matplotlib.pyplot as plt
 
# Generate synthetic data
np.random.seed(42)  # For reproducibility
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)
X_b = np.c_[np.ones((100, 1)), X]  # Add bias term
 
# Hyperparameters
learning_rate = 0.01
epsilon = 1e-8
beta = 0.9
num_iterations = 1000
 
# Initialize parameters
theta = np.random.randn(2, 1)
s = np.zeros((2, 1))  # Initialize the running average of squared gradients
 
# RMSprop optimization
for iteration in range(num_iterations):
    gradients = 2 / len(X_b) * X_b.T.dot(X_b.dot(theta) - y)
    s = beta * s + (1 - beta) * gradients ** 2  # Update the running average of squared gradients
    adjusted_gradients = gradients / (np.sqrt(s) + epsilon)
    theta -= learning_rate * adjusted_gradients
 
    if iteration % 100 == 0:
        print(f"Iteration {iteration}: theta = {theta.ravel()}")
 
print("Theta:", theta)
 
# Plotting the results
plt.scatter(X, y, label='Data')
plt.plot(X, X_b.dot(theta), color='red', linewidth=2, label='RMSprop')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()
''')
    elif(num==9):
        print('''
#DL Sentiment of RNN
 
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense , LSTM , Embedding
from keras.datasets import imdb
 
#Loading datasets
(X_train , y_train) , (X_test , y_test) = imdb.load_data(num_words=5000)
 
#padding the sequences 
x_train = sequence.pad_sequences(X_train  , maxlen=80)
x_test = sequence.pad_sequences(X_test , maxlen=80)
 
# creating the model 
model = Sequential()
model.add(Embedding(input_dim = 5000 , output_dim = 128 , input_shape=(80,)))
model.add(LSTM(128 , activation="tanh" , recurrent_activation="sigmoid"))
model.add(Dense(1,activation="sigmoid"))
 
model.compile(loss="binary_crossentropy" , optimizer="adam" , metrics=['accuracy'])
model.summary()
 
 
lstm = model.fit(x_train , y_train , batch_size=32 , epochs=3 , validation_data=(x_test,y_test),shuffle=True  , verbose=1)
print(lstm)
 
op = model.predict(x_test)
print(op)
 
from random import randint
 
arr_ind = randint(0,24999)
index = imdb.get_word_index()
reverse_index = {}
for key , value in index.items():
    reverse_index[value] = key
 
 
decoded = ""
for i in x_test[arr_ind]:
    word = reverse_index.get(i-3  , "#")
    decoded = decoded + word + " "
decoded = decoded.strip()
 
print(decoded)
 
arr = []
for i in op:
    if i < 0.5:
        arr.append("negative")
    else:
        arr.append("postive")
print(arr[arr_ind])
print(op[arr_ind][0])
print(y_test[arr_ind])
''')
    elif(num==10):
        print('''
#CNN Using Mnist datasets
 
import tensorflow as tf
from tensorflow.keras import datasets , layers , models
import matplotlib.pyplot as plt
 
(train_images , train_labels) ,(test_images , test_labels) = datasets.mnist.load_data()
 
train_images = train_images.reshape((train_images.shape[0],28,28,1))
test_images = test_images.reshape((test_images.shape[0] , 28,28,1))
 
train_images , test_images = train_images / 255.0 , test_images / 255.0
 
model = models.Sequential()
model.add(layers.Conv2D(32,(3,3) , activation="relu" , input_shape=(28,28,1)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64,(3,3) , activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64,(3,3),activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64,activation='relu'))
model.add(layers.Dense(10,activation='softmax'))
 
model.compile(optimizer='adam' , loss = 'sparse_categorical_crossentropy',metrics=['accuracy'])
model.fit(train_images , train_labels  , epochs = 5 , batch_size=64 , validation_data=(test_images , test_labels))
test_loss , test_acc = model.evaluate(test_images , test_labels)
print(test_acc)
''')
    elif(num==11):
        print('''
# Filter on Mnist using CNN
 
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
 
# Load and preprocess the MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape((60000, 28, 28, 1)).astype('float32') / 255  # Reshape and normalize
x_test = x_test.reshape((10000, 28, 28, 1)).astype('float32') / 255
 
# One-hot encode the labels
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)
 
# Define the CNN model
def create_cnn_model():
    model = models.Sequential()
    
    # Convolutional layer with 3x3 filters (Sharpening Filter)
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    
    # Convolutional layer with 5x5 filters (Blur Filter)
    model.add(layers.Conv2D(64, (5, 5), activation='relu'))
    
    # Pooling layer
    model.add(layers.MaxPooling2D((2, 2)))
    
    # Another convolutional layer (Edge Detection Filter)
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    
    # Flattening layer
    model.add(layers.Flatten())
    
    # Fully connected layers
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))  # Dropout for regularization
    model.add(layers.Dense(10, activation='softmax'))  # Output layer
 
    return model
 
# Create and compile the model
model = create_cnn_model()
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
 
# Train the model
history = model.fit(x_train, y_train, epochs=10, batch_size=64, validation_data=(x_test, y_test))
 
# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test accuracy: {test_acc:.4f}')
 
# Plot training and validation accuracy
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='test accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()
plt.show()
 
# Plot training and validation loss
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='test loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()
''')
    elif(num==12):
        print('''
# CNN using Image Filters 
#pip install scikit-image
 
!pip install scikit-image
 
# CNN using Image Filters
import numpy as np
import matplotlib.pyplot as plt 
from skimage.io import imshow, imread
from skimage.color import rgb2gray
from scipy.signal import convolve2d
 
# Reading Image
dog = imread('image01-removebg-preview.png')
 
# Remove the alpha channel if present (RGBA to RGB)
if dog.shape[-1] == 4:
    dog = dog[:, :, :3]  # Keep only the first 3 channels (RGB)
 
# Display the original image
plt.figure(num=None, figsize=(8,6), dpi=80)
imshow(dog)
plt.title('Original Image')
 
# Filter Matrices
sharpen = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])
 
blur = np.array([[0.11, 0.11, 0.11],
                 [0.11, 0.11, 0.11],
                 [0.11, 0.11, 0.11]])
 
vertical = np.array([[-1, 0, 1],
                     [-2, 0, 2],
                     [-1, 0, 1]])
 
gaussian = (1/16.0) * np.array([[1, 2, 1],
                                [2, 4, 2],
                                [1, 2, 1]])
 
# Plotting the filters
fig, ax = plt.subplots(1, 3, figsize=(17, 10))
ax[0].imshow(sharpen, cmap='gray')
ax[0].set_title('Sharpen', fontsize=18)
 
ax[1].imshow(blur, cmap='gray')
ax[1].set_title('Blur', fontsize=18)
 
ax[2].imshow(vertical, cmap='gray')
ax[2].set_title('Vertical', fontsize=18)
 
# Grayscaling the image
dog_gray = rgb2gray(dog)
plt.figure(num=None, figsize=(8,6), dpi=80)
imshow(dog_gray)
plt.title('Grayscale Image')
 
# Function for applying filters to grayscale images
def multi_convolver(image, kernel, iterations):
    for i in range(iterations):
        image = convolve2d(image, kernel, 'same', boundary='fill', fillvalue=0)
    return image
 
# Applying sharpen filter to grayscale image
convolved_image = multi_convolver(dog_gray, sharpen, 1)
 
# Display the convolved image
plt.figure(num=None, figsize=(8,6), dpi=80)
imshow(convolved_image)
plt.title('Convolved Image (Sharpen Filter)')
 
# Function for applying filters to colored images (RGB)
def convolver_rgb(image, kernel, iterations=1):
    # Apply convolution on each channel (R, G, B)
    convolved_image_r = multi_convolver(image[:, :, 0], kernel, iterations)
    convolved_image_g = multi_convolver(image[:, :, 1], kernel, iterations)
    convolved_image_b = multi_convolver(image[:, :, 2], kernel, iterations)
 
    # Stack the channels back together
    reformed_image = np.dstack((np.rint(abs(convolved_image_r)), 
                                np.rint(abs(convolved_image_g)), 
                                np.rint(abs(convolved_image_b)))) / 255
 
    # Plot the channels separately
    fig, ax = plt.subplots(1, 3, figsize=(17, 10))
 
    ax[0].imshow(abs(convolved_image_r), cmap='Reds')
    ax[0].set_title('Red Channel', fontsize=15)
 
    ax[1].imshow(abs(convolved_image_g), cmap='Greens')
    ax[1].set_title('Green Channel', fontsize=15)
 
    ax[2].imshow(abs(convolved_image_b), cmap='Blues')
    ax[2].set_title('Blue Channel', fontsize=15)
 
    return np.array(reformed_image * 255).astype(np.uint8)
 
# Applying the vertical filter to the colored image
convolved_rgb_gauss = convolver_rgb(dog, vertical.T, 1)
 
# Display the convolved colored image
plt.figure(num=None, figsize=(8,6), dpi=80)
plt.imshow(convolved_rgb_gauss, vmin=0, vmax=255)
plt.title('Convolved RGB Image (Vertical Filter)')
''')
    elif(num==13):
        print('''
print('Simple autoencoder')
 
import numpy as np
import keras
from keras import layers
from keras.datasets import mnist
import matplotlib.pyplot as plt
 
# Load and preprocess data
(x_train, _), (x_test, _) = mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
print(x_train.shape)  # (60000, 784)
print(x_test.shape)   # (10000, 784)
 
# Build the autoencoder
input_img = keras.Input(shape=(784,))
encoded = layers.Dense(128, activation='sigmoid')(input_img)
decoded = layers.Dense(784, activation='sigmoid')(encoded)
autoencoder = keras.Model(input_img, decoded)
 
# Compile the model
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
 
# Train the model
autoencoder.fit(x_train, x_train,
                epochs=5,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))
 
# Generate reconstructions
encoded_imgs = autoencoder.predict(x_test)
 
# Visualization
n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # Display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
 
    # Display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(encoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
 
plt.show()
''')
    elif(num==14):
        print('''
print('Sparse Autoencoder')
 
import numpy as np
import keras
from keras import layers, regularizers
from keras.datasets import mnist
import matplotlib.pyplot as plt
 
# Load and preprocess data
(x_train, _), (x_test, _) = mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
print(x_train.shape)  # (60000, 784)
print(x_test.shape)   # (10000, 784)
 
# Build the sparse autoencoder
encoding_dim = 32
input_img = keras.Input(shape=(784,))
encoded = layers.Dense(encoding_dim, activation='relu',
                       activity_regularizer=regularizers.l1(10e-5))(input_img)
decoded = layers.Dense(784, activation='sigmoid')(encoded)
autoencoder = keras.Model(input_img, decoded)
 
# This model maps an input to its encoded representation
encoder = keras.Model(input_img, encoded)
 
# Create the decoder model
encoded_input = keras.Input(shape=(encoding_dim,))
decoder_layer = autoencoder.layers[-1]
decoder = keras.Model(encoded_input, decoder_layer(encoded_input))
 
# Compile the model
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
 
# Train the model
autoencoder.fit(x_train, x_train,
                epochs=20,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))
 
# Encode and decode some digits
encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)
 
# Visualization
n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # Display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
 
    # Display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
 
plt.show()
''')
    elif(num==15):
        print('''
# Denoising Autoencoder
 
print('Denoising Autoencoder')
import numpy as np
import keras
from keras.layers import Input, Dense, GaussianNoise
from keras.models import Model
from keras.datasets import mnist
import matplotlib.pyplot as plt
 
# Load and preprocess data
(x_train, _), (x_test, _) = mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
print(x_train.shape)  # (60000, 784)
print(x_test.shape)   # (10000, 784)
 
# Build the denoising autoencoder
input_img = Input(shape=(784,))
# Add Gaussian noise to the input
noisy_input = GaussianNoise(0.5)(input_img)
encoded = Dense(128, activation='sigmoid')(noisy_input)
decoded = Dense(784, activation='sigmoid')(encoded)
 
# Build the autoencoder model
autoencoder = Model(input_img, decoded)
 
# Compile the model
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
 
# Train the model
autoencoder.fit(x_train, x_train,
                epochs=5,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))
 
# Generate noisy images for testing
noise_factor = 0.5
x_test_noisy = x_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape)
x_test_noisy = np.clip(x_test_noisy, 0., 1.)
 
# Encode and decode some digits
encoded_imgs = autoencoder.predict(x_test_noisy)
 
# Visualization
n = 10
plt.figure(figsize=(20, 6))
for i in range(n):
    # Display original
    ax = plt.subplot(3, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
 
    # Display noisy
    ax = plt.subplot(3, n, i + 1 + n)
    plt.imshow(x_test_noisy[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
 
    # Display reconstruction
    ax = plt.subplot(3, n, i + 1 + 2*n)
    plt.imshow(encoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
 
plt.show()
 
''')
    elif(num==16):
        print('''
# DropOut with CNN on Mnist dataset
 
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
 
# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()
 
# Preprocess data
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0
 
# One-hot encode labels
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)
 
# Build CNN model with Dropout
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    
    layers.Conv2D(64, (3, 3), activation='relu'),
    
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),  # Dropout layer with 50% rate
    layers.Dense(10, activation='softmax')
])
 
# Compile the model
model.compile(optimizer='adam', 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])
 
# Train the model
history = model.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_test, y_test))
 
# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test accuracy: {test_acc:.4f}')
 
# Plot training & validation accuracy and loss
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()
 
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()
 
plt.show()
''')
    elif(num==17):
        print('''
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
 
# Load the MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape((60000, 28, 28, 1)).astype('float32') / 255  # Reshape and normalize
x_test = x_test.reshape((10000, 28, 28, 1)).astype('float32') / 255
 
# One-hot encode the labels
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)
 
# Data Augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical", input_shape=(28, 28, 1)),  # Specify input shape here
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.1),
])
 
# Create a simple CNN model
def create_cnn_model():
    model = models.Sequential()
    model.add(data_augmentation)  # Include data augmentation in the model
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))  # Output layer
 
    return model
 
# Create and compile the model
model = create_cnn_model()
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
 
# Train the model with data augmentation
history = model.fit(x_train, y_train, epochs=10, batch_size=64, validation_data=(x_test, y_test))
 
# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test accuracy: {test_acc:.4f}')
 
# Plot training and validation accuracy
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='test accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()
plt.show()
 
# Plot training and validation loss
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='test loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()
''')

    else:
        print('''
    1:BinaryClassClassification
    2:MultiClassClassification
    3:BatchGradientDescent
    4:Stochasticbatchgradientdescent
    5:performminibatch
    6:gradientdescentwithmomentum 
    7:Adagrad 
    8:RMSprop
    9:Sentiment Analysis of RNN
    10:CNN Using Mnist Dataset
    11:CNN Using Types Of Filter on Mnist
    12:Filter on Images
    13: simple autoencoder
    14:sparse
    15:denosing
    16:ropOut with CNN on Mnist dataset
    17:Augmentation
    
''')

