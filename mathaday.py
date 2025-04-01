# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 09:18:34 2025

@author: Hemal
"""

import streamlit as st
import random

# Function to display the homepage
def homepage():
    st.title("Welcome to Interactive Math Learning!")
    st.write("Learn math and unit conversions in a fun and interactive way!")
    st.write("Choose an exercise or conversion tool to get started:")
    st.sidebar.success("Select an option above.")

# Function to generate math exercises
def generate_exercise(operation):
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    if operation == "addition":
        question = f"What is {num1} + {num2}?"
        answer = num1 + num2
    elif operation == "subtraction":
        question = f"What is {num1} - {num2}?"
        answer = num1 - num2
    elif operation == "multiplication":
        question = f"What is {num1} × {num2}?"
        answer = num1 * num2
    elif operation == "division":
        num2 = random.randint(1, 10)  # Avoid division by zero
        question = f"What is {num1 * num2} ÷ {num2}?"
        answer = num1
    return question, answer

# Function to handle math exercises
def math_exercise(operation):
    st.title(f"{operation.capitalize()} Exercise")
    question, answer = generate_exercise(operation)
    user_answer = st.number_input(question, min_value=0)
    if st.button("Submit"):
        if user_answer == answer:
            st.success("Correct! Great job!")
        else:
            st.error(f"Wrong answer. The correct answer is {answer}.")

# Function to handle length conversions
def length_conversion():
    st.title("Length Conversion")
    option = st.selectbox("Convert from", ["Meters", "Kilometers", "Miles", "Yards", "Feet", "Inches"])
    value = st.number_input("Enter value", min_value=0.0)

    if option == "Meters":
        meters = value
        kilometers = meters / 1000
        miles = meters / 1609.34
        yards = meters * 1.09361
        feet = meters * 3.28084
        inches = meters * 39.3701
    elif option == "Kilometers":
        kilometers = value
        meters = kilometers * 1000
        miles = kilometers / 1.60934
        yards = kilometers * 1093.61
        feet = kilometers * 3280.84
        inches = kilometers * 39370.1
    elif option == "Miles":
        miles = value
        kilometers = miles * 1.60934
        meters = miles * 1609.34
        yards = miles * 1760
        feet = miles * 5280
        inches = miles * 63360
    elif option == "Yards":
        yards = value
        meters = yards / 1.09361
        kilometers = yards / 1093.61
        miles = yards / 1760
        feet = yards * 3
        inches = yards * 36
    elif option == "Feet":
        feet = value
        meters = feet / 3.28084
        kilometers = feet / 3280.84
        miles = feet / 5280
        yards = feet / 3
        inches = feet * 12
    elif option == "Inches":
        inches = value
        meters = inches / 39.3701
        kilometers = inches / 39370.1
        miles = inches / 63360
        yards = inches / 36
        feet = inches / 12

    st.write(f"{value} {option} is equal to:")
    st.write(f"{meters:.4f} Meters")
    st.write(f"{kilometers:.4f} Kilometers")
    st.write(f"{miles:.4f} Miles")
    st.write(f"{yards:.4f} Yards")
    st.write(f"{feet:.4f} Feet")
    st.write(f"{inches:.4f} Inches")

# Function to handle weight conversions
def weight_conversion():
    st.title("Weight Conversion")
    option = st.selectbox("Convert from", ["Grams", "Kilograms", "Pounds", "Ounces"])
    value = st.number_input("Enter value", min_value=0.0)

    if option == "Grams":
        grams = value
        kilograms = grams / 1000
        pounds = grams / 453.592
        ounces = grams / 28.3495
    elif option == "Kilograms":
        kilograms = value
        grams = kilograms * 1000
        pounds = kilograms * 2.20462
        ounces = kilograms * 35.274
    elif option == "Pounds":
        pounds = value
        kilograms = pounds / 2.20462
        grams = pounds * 453.592
        ounces = pounds * 16
    elif option == "Ounces":
        ounces = value
        kilograms = ounces / 35.274
        grams = ounces * 28.3495
        pounds = ounces / 16

    st.write(f"{value} {option} is equal to:")
    st.write(f"{grams:.4f} Grams")
    st.write(f"{kilograms:.4f} Kilograms")
    st.write(f"{pounds:.4f} Pounds")
    st.write(f"{ounces:.4f} Ounces")

# Function to handle temperature conversions
def temperature_conversion():
    st.title("Temperature Conversion")
    option = st.selectbox("Convert from", ["Celsius", "Fahrenheit", "Kelvin"])
    value = st.number_input("Enter value", min_value=-273.15 if option == "Celsius" else 0.0)

    if option == "Celsius":
        celsius = value
        fahrenheit = (celsius * 9/5) + 32
        kelvin = celsius + 273.15
    elif option == "Fahrenheit":
        fahrenheit = value
        celsius = (fahrenheit - 32) * 5/9
        kelvin = (fahrenheit - 32) * 5/9 + 273.15
    elif option == "Kelvin":
        kelvin = value
        celsius = kelvin - 273.15
        fahrenheit = (kelvin - 273.15) * 9/5 + 32

    st.write(f"{value} {option} is equal to:")
    st.write(f"{celsius:.4f} Celsius")
    st.write(f"{fahrenheit:.4f} Fahrenheit")
    st.write(f"{kelvin:.4f} Kelvin")

# Function to handle volume conversions
def volume_conversion():
    st.title("Volume Conversion")
    option = st.selectbox("Convert from", ["Milliliters", "Liters", "Gallons", "Quarts", "Pints", "Cups", "Fluid Ounces"])
    value = st.number_input("Enter value", min_value=0.0)

    if option == "Milliliters":
        milliliters = value
        liters = milliliters / 1000
        gallons = milliliters / 3785.41
        quarts = milliliters / 946.353
        pints = milliliters / 473.176
        cups = milliliters / 236.588
        ounces = milliliters / 29.5735
    elif option == "Liters":
        liters = value
        milliliters = liters * 1000
        gallons = liters / 3.78541
        quarts = liters / 0.946353
        pints = liters / 0.473176
        cups = liters / 0.236588
        ounces = liters / 0.0295735
    elif option == "Gallons":
        gallons = value
        liters = gallons * 3.78541
        milliliters = gallons * 3785.41
        quarts = gallons * 4
        pints = gallons * 8
        cups = gallons * 16
        ounces = gallons * 128
    elif option == "Quarts":
        quarts = value
        liters = quarts * 0.946353
        milliliters = quarts * 946.353
        gallons = quarts / 4
        pints = quarts * 2
        cups = quarts * 4
        ounces = quarts * 32
    elif option == "Pints":
        pints = value
        liters = pints * 0.473176
        milliliters = pints * 473.176
        gallons = pints / 8
        quarts = pints / 2
        cups = pints * 2
        ounces = pints * 16
    elif option == "Cups":
        cups = value
        liters = cups * 0.236588
        milliliters = cups * 236.588
        gallons = cups / 16
        quarts = cups / 4
        pints = cups / 2
        ounces = cups * 8
    elif option == "Fluid Ounces":
        ounces = value
        liters = ounces * 0.0295735
        milliliters = ounces * 29.5735
        gallons = ounces / 128
        quarts = ounces / 32
        pints = ounces / 16
        cups = ounces / 8

    st.write(f"{value} {option} is equal to:")
    st.write(f"{milliliters:.4f} Milliliters")
    st.write(f"{liters:.4f} Liters")
    st.write(f"{gallons:.4f} Gallons")
    st.write(f"{quarts:.4f} Quarts")
    st.write(f"{pints:.4f} Pints")
    st.write(f"{cups:.4f} Cups")
    st.write(f"{ounces:.4f} Fluid Ounces")

# Main function to navigate between pages
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Addition", "Subtraction", "Multiplication", "Division", "Length Conversion", "Weight Conversion", "Temperature Conversion", "Volume Conversion"])

    if page == "Home":
        homepage()
    elif page == "Addition":
        math_exercise("addition")
    elif page == "Subtraction":
        math_exercise("subtraction")
    elif page == "Multiplication":
        math_exercise("multiplication")
    elif page == "Division":
        math_exercise("division")
    elif page == "Length Conversion":
        length_conversion()
    elif page == "Weight Conversion":
        weight_conversion()
    elif page == "Temperature Conversion":
        temperature_conversion()
    elif page == "Volume Conversion":
        volume_conversion()

if __name__ == "__main__":
    main()
