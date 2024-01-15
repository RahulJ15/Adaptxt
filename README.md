
# OCR and Translation Model

**Overview:**

This project is an end-to-end Optical Character Recognition (OCR) and translation model designed to extract text from images and PDFs, and then translate it into multiple languages. The implementation is done in Python using the Tesseract OCR engine, OpenCV for image processing, Googletrans for translation, and Streamlit for the frontend.

**Key Features:**

1. **OCR Processing:**
   - Utilizes Tesseract OCR to extract text from images and PDFs.
   - Implements image preprocessing techniques, including conversion to grayscale, removal of table lines, and noise reduction, to enhance OCR accuracy.

2. **Translation:**
   - Translates extracted text into five different languages (Hindi, French, Spanish, Mandarin, English) using the Googletrans API.

3. **PDF Support:**
   - Supports PDF extraction, recognizing text from each page and translating it.

4. **User Interaction:**
   - Allows the user to choose the target language for translation.

**Frontend with Streamlit:**

- Implements a user-friendly interface using [Streamlit](https://streamlit.io/) for easy interaction with the OCR and translation model.
- Users can upload images or PDFs, and the application displays the recognized text along with translation options.
- Provides a dropdown menu for selecting the target language, enhancing user customization.
- Streamlit simplifies the deployment process, making the application accessible through a web browser.

**Dependencies:**

- [Pillow (PIL)](https://python-pillow.org/)
- [Pytesseract](https://pypi.org/project/pytesseract/)
- [OpenCV](https://pypi.org/project/opencv-python/)
- [Googletrans](https://pypi.org/project/googletrans/)
- [PyPDF2](https://pythonhosted.org/PyPDF2/)
- [Streamlit](https://streamlit.io/)

**Usage:**

1. Access the OCR and translation model through the Streamlit web interface.
2. Upload images or PDFs using the provided file upload functionality.
3. The application processes the input, displays the recognized text, and allows translation into the user-selected language.

**How to Run:**

- Ensure the required libraries are installed using:
  ```bash
  pip install pillow pytesseract opencv-python googletrans pyPDF2 streamlit
  ```
- Make sure Tesseract OCR is properly installed on your system.

- Run the Streamlit application script:
  ```bash
  streamlit run streamlit_script.py
  ```

**Example:**

Visit `http://localhost:8501` in your web browser to access the Streamlit application.

Feel free to explore and enhance this project for your specific use case. Contributions and suggestions are welcome!

--- 
