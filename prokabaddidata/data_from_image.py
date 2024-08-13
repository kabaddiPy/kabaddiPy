import cv2
import numpy as np
import pytesseract
from PIL import Image
import pandas as pd

def preprocess_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to preprocess the image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilation to merge letters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    dilation = cv2.dilate(thresh, kernel, iterations=2)
    
    return dilation

def extract_table(preprocessed_image):
    # Perform OCR on the image
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(preprocessed_image, output_type=pytesseract.Output.DICT, config=custom_config)
    
    # Extract words and their positions
    words = data['text']
    left = data['left']
    top = data['top']
    
    # Group words into rows based on their vertical position
    rows = {}
    for i, word in enumerate(words):
        if word.strip():
            if top[i] not in rows:
                rows[top[i]] = []
            rows[top[i]].append((left[i], word))
    
    # Sort rows by vertical position
    sorted_rows = [row for _, row in sorted(rows.items())]
    
    # Sort words in each row by horizontal position
    table_data = [' '.join(word for _, word in sorted(row)) for row in sorted_rows]
    
    return table_data

def create_dataframe(table_data):
    # Split each row into columns
    split_data = [row.split() for row in table_data]
    
    # Find the maximum number of columns
    max_columns = max(len(row) for row in split_data)
    
    # Pad rows with fewer columns
    padded_data = [row + [''] * (max_columns - len(row)) for row in split_data]
    
    # Create DataFrame
    df = pd.DataFrame(padded_data)
    
    # Use the first row as header if it seems to contain column names
    if df.iloc[0].str.contains(r'[a-zA-Z]').all():
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)
    
    return df

def main(image_path):
    preprocessed_image = preprocess_image(image_path)
    table_data = extract_table(preprocessed_image)
    df = create_dataframe(table_data)
    
    print(df)
    return df

# Usage
if __name__ == "__main__":
    image_path = 'tableau.jpeg'  # Replace with your image path
    result_df = main(image_path)
    
    # Optionally, save to CSV
    result_df.to_csv('extracted_table.csv', index=False)