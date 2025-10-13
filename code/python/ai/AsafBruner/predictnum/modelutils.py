import numpy as np
import pandas as pd
import tensorflow as tf
import argparse
from datetime import datetime
from matplotlib import pyplot as plt

# Load and preprocess the data
def load_and_preprocess_data():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)
    return (x_train, y_train), (x_test, y_test)


# Define the model
def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Train the model
def train_model(model, x_train, y_train, x_test, y_test):
    (x_train, y_train), (x_test, y_test) = load_and_preprocess_data()
    model = create_model()
    
    # Set up TensorBoard logging
    logdir = "logs/scalars/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)


    model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test), callbacks=[tensorboard_callback])
    model.evaluate(x_test, y_test)
    model.save_weights('mnist_model.weights.h5')

# Load model weights
def load_model_weights(model):
    model.load_weights('mnist_model.weights.h5')

# Function to print model weights
def print_model_weights(model):
    for layer in model.layers:
        if len(layer.get_weights()) > 0:
            weights, biases = layer.get_weights()
            print(f"Layer: {layer.name}")

            print("Weights:")
            weights_df = pd.DataFrame(weights.reshape(-1, weights.shape[-1]))
            print(weights_df)

            print("Biases:")
            biases_df = pd.DataFrame(biases.reshape(1, -1))
            print(biases_df)
            print("\n")

def predict_and_print_layers(model):
    conv_layers = [0,1,4,5,len(model.layers) - 1] # Indexes of convolutional layers to print (always include the last layer)
    output_layers = [model.layers[i].output for i in conv_layers]
    model = tf.keras.models.Model(inputs=model.inputs, outputs=output_layers)

    # load the image
    img = tf.keras.preprocessing.image.load_img('digit.png')
    img = img.resize((28, 28)).convert('L')
    img = np.array(img)
    img = np.clip(img, 0, 255)
    img = 255 - img
    img = img / 255.0
    img = img.reshape(1, 28, 28, 1)
    activation_maps = model.predict(img)

    # Print selected layers
    box = 2
    cv_idx = 0
    for amap in activation_maps:
        i = 1
        print(f'layer: {str(conv_layers[cv_idx])}')
        
        for _ in range(box):
            for _ in range(box):
                axes = plt.subplot(box, box, i)
                if len(amap.shape) == 4:
                    plt.imshow(amap[0, :, :, i-1], cmap='gray')
                elif len(amap.shape) == 2:
                    # plt.imshow(amap, cmap='gray')
                    print(amap[0]) # one dimensional array are printed as is because they cannot be represented as images
                i += 1
            
        if len(amap.shape) == 4:
            axes.figure.suptitle(f'layer: {str(conv_layers[cv_idx])}')
            plt.show()
        cv_idx += 1
    
    plt.close(axes.figure) # Close the last figure

    # Display output layer
    array = activation_maps[-1][0]
    array = np.round(array * 100, 2) # Convert to percentage and round to 2 decimal places
    fig= plt.figure(figsize=(10, 2))
    ax = fig.add_subplot(111)
    ax.set_facecolor('grey')
    ax.yaxis.set_visible(False)
    plt.scatter(range(len(array)), [0] * len(array), c=array, cmap='gray', s=200)
    plt.xticks(range(len(array)), array) 
    plt.title(f'output layer')
    plt.show()   

# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train a model or print its weights.')
    parser.add_argument('command', choices=['train', 'print_weights', 'print_layers'], help='Command to execute: "train" or "print_weights"')

    args = parser.parse_args()

    (x_train, y_train), (x_test, y_test) = load_and_preprocess_data()
    model = create_model()
    print(model.summary())

    if args.command == 'train':
        train_model(model, x_train, y_train, x_test, y_test)
    elif args.command == 'print_weights':
        load_model_weights(model)
        print_model_weights(model)
    elif args.command == 'print_layers':
        load_model_weights(model)
        predict_and_print_layers(model)    