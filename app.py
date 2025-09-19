import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image

# --- 1. Load the Trained Model ---
print("Loading the model...")
try:
    model = tf.keras.models.load_model('best_model.h5')
except OSError:
    print("Error: 'best_model.h5' not found. Please run 'train_model.py' first.")
    exit()
print("Model loaded successfully.")

# --- 2. Define Prediction Function ---
def predict_digit(image):
    """
    Preprocesses the image and makes a prediction.
    """
    if image is None:
        return "Please upload an image."
    
    image = image.convert('L')
    image = image.resize((28, 28))
    image_array = np.array(image) / 255.0
    image_array = image_array.reshape(1, 28, 28, 1)
    
    prediction = model.predict(image_array)
    
    label_dict = {str(i): float(prediction[0][i]) for i in range(10)}
    
    return label_dict

iface = gr.Interface(
    fn=predict_digit,
    inputs=gr.Image(
        type='pil', 
        image_mode='L', 
        label="Upload a handwritten digit"
    ),
    outputs=gr.Label(
        num_top_classes=3, 
        label="Prediction"
    ),
    title="Handwritten Digit Recognizer",
    description="Upload a handwritten digit (0-9). The model will predict what number it is and show the top 3 confidence scores."
)

print("Launching Gradio interface...")
iface.launch(share=True)