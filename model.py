import tensorflow as tf
import os

# Define a simple sequential model
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(5,)),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    return model

# Create a basic model instance
model = create_model()

# Compile the model
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Create a directory to save the model
model_dir = 'saved_model/my_model'
os.makedirs(model_dir, exist_ok=True)

# Save the model
model.save(model_dir, save_format='tf')
print(f"Model saved to {model_dir}")
