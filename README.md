
Project Description: Multilingual OCR and Translation Tool

Overview:
This project is a versatile Optical Character Recognition (OCR) and translation tool designed to process both images and PDF documents. Leveraging computer vision and natural language processing libraries, it offers functionalities to enhance image quality, extract text, and provide translations in multiple languages. The project is integrated with Streamlit for easy deployment and user interaction.

Key Features:

Image Processing:

Conversion to JPEG format: Automatically converts non-JPEG images to JPEG format for standardized processing.
Deskewing: Corrects image skew to improve OCR accuracy.
Table Line Removal: Eliminates lines from tables in the image for better text extraction.
Text Extraction:

OCR Engine: Utilizes Tesseract OCR to extract text from preprocessed images.
PDF Text Extraction: Extracts text from PDF documents using PyPDF2.
Image Preprocessing:

Grayscale Conversion: Converts the image to grayscale for enhanced feature extraction.
Binary Image Creation: Generates a binary image to highlight text features.
Noise Removal: Applies morphological operations and blurring to reduce noise in the binary image.
Translation:

Language Selection: Allows users to choose the target language for translation from a predefined set.
Google Translate Integration: Uses the Google Translate API to provide translations of extracted text.
Streamlit Integration:

User-Friendly Interface: Deployed with Streamlit, providing an intuitive web interface for users.
PDF Processing: Offers seamless processing and translation of text from PDF documents.
Real-time Interaction: Enables users to view recognized and translated text instantly.
