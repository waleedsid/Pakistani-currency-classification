# Currency Classification Project

This project aims to classify different denominations of Pakistan currency notes using machine learning techniques.

## Project Overview

The goal of this project is to create a robust machine learning model capable of accurately identifying and classifying various denominations of Pakistan currency notes. The model will be trained on a dataset of labeled images, and the final application will allow users to upload images of currency notes and receive predictions regarding their denominations.

## Dataset

The dataset used for this project consists of images of Pakistan currency notes, categorized by denomination. The denominations included in the dataset are 10, 20, 50, 100, 500, and 1000 rupees. The images cover various angles, lighting conditions, and backgrounds to ensure the model's robustness in real-world scenarios.

## Project Structure

The project structure is organized as follows:

```
currency-classification/
│
├── data/          # Folder for the dataset
├── models/        # Folder for storing trained models
├── src/           # Source code for the project
│   ├── preprocess.py
│   ├── train.py
│   ├── predict.py
├── requirements.txt  # List of project dependencies
├── README.md         # Project documentation
```

- The `data` folder contains the dataset used for training and testing.
- The `models` folder stores the trained machine learning models.
- The `src` folder holds the source code for data preprocessing, training, and prediction scripts.

## Getting Started

To set up the project locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/waleedsid/currency-classification.git
    ```

2. Navigate to the project folder:

    ```bash
    cd currency-classification
    ```

3. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use venv\Scripts\activate
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Training the Model

To train the machine learning model, run the following command:

```bash
python src/train.py
```

This script will preprocess the data, train the model, and save the trained model to the `models` folder.

## Predictions

To make predictions using the trained model, use the following command:

```bash
python src/predict.py path/to/new_image.jpg
```

Replace `path/to/new_image.jpg` with the path to the image you want to classify.

## Dependencies

This project relies on the following Python libraries:

- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [scikit-learn](https://scikit-learn.org/)
- [tensorflow](https://www.tensorflow.org/)

Install these dependencies using the command provided in the "Getting Started" section.

## Contributing

If you'd like to contribute to this project, please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

