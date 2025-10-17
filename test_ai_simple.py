# Simple AI Model Test
import tensorflow as tf
import numpy as np

print("ðŸ¤– Testing TensorFlow AI Model")
print("=" * 40)

# Test TensorFlow
print(f"âœ… TensorFlow version: {tf.__version__}")
print(f"âœ… GPU available: {tf.config.list_physical_devices('GPU')}")

# Create simple model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(64, 64, 3)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(66, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("âœ… AI model created successfully!")
print(f"ðŸ“Š Total parameters: {model.count_params():,}")

# Test prediction
test_image = np.random.random((1, 64, 64, 3))
prediction = model.predict(test_image, verbose=0)
print(f"âœ… Prediction shape: {prediction.shape}")
print(f"âœ… Max confidence: {np.max(prediction):.4f}")

print("\nðŸŽ‰ AI Model Test Complete!")
print("ðŸ“ˆ Ready for Phase 2 implementation!")
