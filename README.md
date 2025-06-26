# 💎 Diamond Price Predictor

This is a Flask-based web application that predicts the price of a diamond based on user input features such as carat, cut, color, clarity, and dimensions. The prediction is powered by a trained machine learning model.

---

## Features

- User-friendly web form to input diamond attributes
- Price prediction using a pre-trained ML model
- Beautiful UI with modern design (HTML + CSS)
- Runs locally on your machine

---

## Tech Stack

- Python 3.x
- Flask
- Scikit-learn / Regression models
- VS Code
- HTML5 + CSS3
---

## Installation & Setup

1. **Clone the repository**  
   git clone https://github.com/Manmohan-MH/Diamond_price_prediction.git <br>
   cd diamond-price-predictor

2. **Create and activate a virtual environment (recommended)** <br>
    conda create -p \venv == python 3.8 <br>
    conda activate .\venv

3. **Install dependencies**
    pip install -r requirements.txt

4. **Run the Flask app**
    python app.py

5. **Open your browser and go to**
    http://127.0.0.1:5000/

6. **Input Features**


| Feature | Description                                                |
| ------- | ---------------------------------------------------------- |
| Carat   | Weight of the diamond                                      |
| Depth   | Total depth percentage                                     |
| Table   | Width of top of the diamond                                |
| X       | Length in mm                                               |
| Y       | Width in mm                                                |
| Z       | Depth in mm                                                |
| Cut     | Quality of the cut (Fair, Good, Very Good, Premium, Ideal) |
| Color   | Diamond color grade (D to J)                               |
| Clarity | Clarity grade (I1 to IF)                                   |
