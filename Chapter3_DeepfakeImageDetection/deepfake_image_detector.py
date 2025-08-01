import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator, image
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# ----------------------------
# Configuration
# ----------------------------
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 16
EPOCHS = 10
DATASET_PATH = "dataset"
TEST_IMAGE = "dataset/fake/img2.jpg"  # Change to your test image path

# ----------------------------
# Preprocess Dataset
# ----------------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)

# ----------------------------
# Build CNN Model
# ----------------------------
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(*IMAGE_SIZE, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # Binary classification
])

# ----------------------------
# Compile the Model
# ----------------------------
model.compile(
    optimizer=Adam(),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ----------------------------
# Train the Model
# ----------------------------
history = model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=val_gen
)

# ----------------------------
# Save the Model
# ----------------------------
model.save("saved_model.h5")
print("Model saved to saved_model.h5")

# ----------------------------
# Plot Training Accuracy
# ----------------------------
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Val')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# ----------------------------
# Test a Single Image
# ----------------------------
model = load_model("saved_model.h5")

img = image.load_img(TEST_IMAGE, target_size=IMAGE_SIZE)
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

prediction = model.predict(img_array)
confidence = float(prediction[0])

label = "FAKE" if confidence > 0.5 else "REAL"
print(f"[RESULT] The image is predicted as: {label} ({confidence:.2f})")


