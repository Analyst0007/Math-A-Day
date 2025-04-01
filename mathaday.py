# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 09:18:34 2025

@author: Hemal
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import time

def main():
    st.set_page_config(
        page_title="KidsMath App",
        page_icon="🧮",
        layout="wide"
    )

    # Custom CSS for better appearance
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .question-container {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .correct-answer {
        color: green;
        font-weight: bold;
    }
    .wrong-answer {
        color: red;
        font-weight: bold;
    }
    .big-font {
        font-size: 24px;
        font-weight: bold;
    }
    .results-container {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        border: 2px solid #4CAF50;
    }
    .quiz-summary {
        font-size: 18px;
        margin-bottom: 15px;
    }
    .badge-success {
        background-color: #4CAF50;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        margin-right: 5px;
    }
    .badge-warning {
        background-color: #ff9800;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        margin-right: 5px;
    }
    .badge-danger {
        background-color: #f44336;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        margin-right: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state for tracking quiz history
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []

    if 'username' not in st.session_state:
        st.session_state.username = ""

    # Title and Navigation
    st.title("🧮 KidsMath Learning App")

    # User identification
    if not st.session_state.username:
        st.session_state.username = st.text_input("Enter your name:", "Student")

    st.write(f"Welcome, {st.session_state.username}! Let's learn math in a fun way!")

    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["Math Quiz", "Quiz Results", "Multiplication Tables", "Unit Converters"],
        icons=["question-circle", "graph-up", "table", "arrow-left-right"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Math Quiz":
        math_quiz_section()
    elif selected == "Quiz Results":
        quiz_results_section()
    elif selected == "Multiplication Tables":
        multiplication_tables_section()
    elif selected == "Unit Converters":
        unit_converters_section()

def math_quiz_section():
    st.header("Math Quiz")

    # Quiz Type Selection
    quiz_type = st.selectbox(
        "Select Quiz Type",
        ["Addition", "Subtraction", "Multiplication", "Division", "Mixed"]
    )

    # Difficulty Selection
    difficulty = st.selectbox(
        "Select Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )

    # Set number range based on difficulty
    if difficulty == "Easy":
        num_range = 10
    elif difficulty == "Medium":
        num_range = 25
    else:
        num_range = 100

    # Number of questions
    num_questions = st.slider("Number of Questions", min_value=5, max_value=20, value=10)

    # Time limit option
    use_timer = st.checkbox("Use Timer")
    time_limit = 0

    if use_timer:
        time_limit = st.slider("Time Limit (seconds per question)", min_value=5, max_value=30, value=10)

    if st.button("Start Quiz"):
        st.session_state.quiz_in_progress = True
        st.session_state.current_question = 0
        st.session_state.questions = generate_questions(quiz_type, num_range, num_questions)
        st.session_state.user_answers = [None] * num_questions
        st.session_state.times_taken = [0] * num_questions
        st.session_state.quiz_start_time = time.time()
        st.rerun()

    if st.session_state.get('quiz_in_progress'):
        run_quiz(quiz_type, difficulty, use_timer, time_limit)

def generate_questions(quiz_type, num_range, num_questions):
    questions = []
    for i in range(num_questions):
        if quiz_type == "Addition" or (quiz_type == "Mixed" and np.random.choice([True, False, False, False])):
            a, b = np.random.randint(1, num_range), np.random.randint(1, num_range)
            correct_answer = a + b
            question = f"{a} + {b} = ?"
            operation = "addition"

        elif quiz_type == "Subtraction" or (quiz_type == "Mixed" and np.random.choice([True, False, False])):
            a = np.random.randint(1, num_range)
            b = np.random.randint(1, min(a, num_range))
            correct_answer = a - b
            question = f"{a} - {b} = ?"
            operation = "subtraction"

        elif quiz_type == "Multiplication" or (quiz_type == "Mixed" and np.random.choice([True, False])):
            a, b = np.random.randint(1, num_range//5 or 2), np.random.randint(1, num_range//5 or 2)
            correct_answer = a * b
            question = f"{a} × {b} = ?"
            operation = "multiplication"

        else:  # Division
            b = np.random.randint(1, 10)
            a = b * np.random.randint(1, num_range//10 or 2)
            correct_answer = a // b
            question = f"{a} ÷ {b} = ?"
            operation = "division"

        questions.append({
            "question": question,
            "answer": correct_answer,
            "operation": operation
        })
    return questions

def run_quiz(quiz_type, difficulty, use_timer, time_limit):
    current_question = st.session_state.current_question
    questions = st.session_state.questions
    user_answers = st.session_state.user_answers
    times_taken = st.session_state.times_taken

    if current_question < len(questions):
        st.markdown(f"<div class='question-container'>", unsafe_allow_html=True)
        st.markdown(f"<p class='big-font'>Question {current_question+1}: {questions[current_question]['question']}</p>", unsafe_allow_html=True)

        question_start_time = time.time()

        # If timer is enabled, show countdown
        if use_timer:
            placeholder = st.empty()
            for remaining in range(time_limit, 0, -1):
                placeholder.markdown(f"⏱️ Time remaining: {remaining} seconds")
                time.sleep(1)

                # Break if time is up
                if time.time() - question_start_time >= time_limit:
                    break

        user_answers[current_question] = st.number_input(f"Your answer for Q{current_question+1}", key=f"q{current_question}", step=1)

        question_end_time = time.time()
        times_taken[current_question] = question_end_time - question_start_time

        st.markdown("</div>", unsafe_allow_html=True)

        # Submit button for each question
        if st.button(f"Submit Answer for Question {current_question+1}", key=f"submit_{current_question}"):
            st.session_state.current_question += 1
            st.rerun()
    else:
        evaluate_quiz_results(questions, user_answers, times_taken, quiz_type, difficulty, st.session_state.quiz_start_time)
        st.session_state.quiz_in_progress = False

def evaluate_quiz_results(questions, user_answers, times_taken, quiz_type, difficulty, quiz_start_time):
    score = 0
    correct_answers = []
    incorrect_answers = []

    # Calculate total quiz time
    total_quiz_time = time.time() - quiz_start_time
    avg_time_per_question = total_quiz_time / len(questions) if questions else 0

    # Evaluate each answer
    for i, (q, ans, time_taken) in enumerate(zip(questions, user_answers, times_taken)):
        if ans == q["answer"]:
            score += 1
            correct_answers.append({
                "question": q["question"],
                "answer": q["answer"],
                "time_taken": time_taken,
                "operation": q["operation"]
            })
        else:
            incorrect_answers.append({
                "question": q["question"],
                "user_answer": ans,
                "correct_answer": q["answer"],
                "time_taken": time_taken,
                "operation": q["operation"]
            })

    # Calculate percentage
    percentage = (score / len(questions)) * 100 if questions else 0

    # Save quiz results to session state
    quiz_result = {
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "quiz_type": quiz_type,
        "difficulty": difficulty,
        "score": score,
        "total_questions": len(questions),
        "percentage": percentage,
        "total_time": total_quiz_time,
        "avg_time_per_question": avg_time_per_question,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers
    }

    st.session_state.quiz_history.append(quiz_result)

    # Display immediate results
    display_quiz_evaluation(quiz_result)

def display_quiz_evaluation(quiz_result):
    st.markdown("<div class='results-container'>", unsafe_allow_html=True)
    st.markdown("## 📊 Quiz Results")

    # Score and time info
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### Score: {quiz_result['score']}/{quiz_result['total_questions']}")
        st.markdown(f"### Percentage: {quiz_result['percentage']:.1f}%")

        # Performance badge
        if quiz_result['percentage'] >= 90:
            st.markdown("<span class='badge-success'>Excellent!</span>", unsafe_allow_html=True)
        elif quiz_result['percentage'] >= 70:
            st.markdown("<span class='badge-success'>Good Job!</span>", unsafe_allow_html=True)
        elif quiz_result['percentage'] >= 50:
            st.markdown("<span class='badge-warning'>Keep Practicing</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='badge-danger'>Needs Improvement</span>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"### Total Time: {quiz_result['total_time']:.1f} seconds")
        st.markdown(f"### Avg. Time per Question: {quiz_result['avg_time_per_question']:.1f} seconds")

        # Speed badge
        if quiz_result['avg_time_per_question'] < 5:
            st.markdown("<span class='badge-success'>Lightning Fast!</span>", unsafe_allow_html=True)
        elif quiz_result['avg_time_per_question'] < 10:
            st.markdown("<span class='badge-success'>Quick Thinker!</span>", unsafe_allow_html=True)
        elif quiz_result['avg_time_per_question'] < 20:
            st.markdown("<span class='badge-warning'>Good Pace</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='badge-warning'>Take Your Time</span>", unsafe_allow_html=True)

    # Correct answers review
    if quiz_result['correct_answers']:
        st.markdown("### ✅ Correct Answers")
        for i, ans in enumerate(quiz_result['correct_answers']):
            st.success(f"{ans['question']} = {ans['correct_answer']} (Time: {ans['time_taken']:.1f}s)")

    # Incorrect answers review
    if quiz_result['incorrect_answers']:
        st.markdown("### ❌ Incorrect Answers")
        for i, ans in enumerate(quiz_result['incorrect_answers']):
            st.error(f"{ans['question']} = {ans['correct_answer']} (Your answer: {int(ans['user_answer'])}, Time: {ans['time_taken']:.1f}s)")

    # Performance by operation type
    operation_stats = {}

    # Count correct answers by operation
    for ans in quiz_result['correct_answers']:
        operation = ans['operation']
        if operation not in operation_stats:
            operation_stats[operation] = {'correct': 0, 'total': 0}
        operation_stats[operation]['correct'] += 1
        operation_stats[operation]['total'] += 1

    # Count incorrect answers by operation
    for ans in quiz_result['incorrect_answers']:
        operation = ans['operation']
        if operation not in operation_stats:
            operation_stats[operation] = {'correct': 0, 'total': 0}
        operation_stats[operation]['total'] += 1

    # Display operation stats
    st.markdown("### 📈 Performance by Operation")

    operation_data = []
    operation_labels = []
    operation_colors = []

    for op, stats in operation_stats.items():
        percentage = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0

        # Set color based on performance
        if percentage >= 80:
            color = "#4CAF50"  # Green
        elif percentage >= 60:
            color = "#FFC107"  # Yellow
        else:
            color = "#F44336"  # Red

        st.markdown(f"- **{op.capitalize()}**: {stats['correct']}/{stats['total']} correct ({percentage:.1f}%)")

        operation_data.append(percentage)
        operation_labels.append(op.capitalize())
        operation_colors.append(color)

    # Create a simple bar chart if there's data
    if operation_data:
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(operation_labels, operation_data, color=operation_colors)

        # Add labels to bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom')

        ax.set_ylim(0, 110)  # Set y-axis limit to 110% to leave room for text
        ax.set_ylabel('Percentage Correct')
        ax.set_title('Performance by Operation Type')

        # Add a horizontal line at 70%
        ax.axhline(y=70, color='gray', linestyle='--')

        st.pyplot(fig)

    # Personalized feedback
    st.markdown("### 💡 Personalized Feedback")

    if quiz_result['percentage'] >= 90:
        st.success(f"Excellent work, {st.session_state.username}! You've mastered this level. Try a harder difficulty or a different operation type!")
    elif quiz_result['percentage'] >= 70:
        st.success(f"Good job, {st.session_state.username}! You're doing well, but there's still room for improvement.")
    elif quiz_result['percentage'] >= 50:
        st.warning(f"Nice effort, {st.session_state.username}! With more practice, you'll get better at this.")
    else:
        st.error(f"Keep trying, {st.session_state.username}! Math takes practice. Maybe try an easier difficulty level for now.")

    # Suggestions based on results
    st.markdown("### 🚀 Next Steps")

    # Identify weakest operation
    weakest_op = None
    lowest_percentage = 100

    for op, stats in operation_stats.items():
        percentage = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        if percentage < lowest_percentage and stats['total'] > 0:
            lowest_percentage = percentage
            weakest_op = op

    if weakest_op:
        st.info(f"💪 Focus on improving your {weakest_op} skills. Try the multiplication tables section if you need help with multiplication or division.")

    # Suggest next difficulty
    if quiz_result['percentage'] >= 85 and quiz_result['difficulty'] != "Hard":
        next_difficulty = "Medium" if quiz_result['difficulty'] == "Easy" else "Hard"
        st.info(f"🔼 You're ready to try the {next_difficulty} difficulty level!")
    elif quiz_result['percentage'] < 50 and quiz_result['difficulty'] != "Easy":
        prev_difficulty = "Easy" if quiz_result['difficulty'] == "Medium" else "Medium"
        st.info(f"🔽 You might want to practice more at the {prev_difficulty} difficulty level.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Option to try again or view results history
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Try Again"):
            st.rerun()

    with col2:
        if st.button("View All Results"):
            st.session_state.view_results = True
            st.rerun()

def quiz_results_section():
    st.header("📊 Quiz Results History")

    if not st.session_state.quiz_history:
        st.info("You haven't taken any quizzes yet. Go to the Math Quiz section to get started!")
        return

    # Display summary of all quizzes
    st.subheader("Summary of All Quizzes")

    # Create a dataframe of all quiz results
    quiz_data = []
    for i, quiz in enumerate(st.session_state.quiz_history):
        quiz_data.append({
            "Quiz #": i + 1,
            "Date": quiz["date"],
            "Type": quiz["quiz_type"],
            "Difficulty": quiz["difficulty"],
            "Score": f"{quiz['score']}/{quiz['total_questions']}",
            "Percentage": f"{quiz['percentage']:.1f}%",
            "Time (s)": f"{quiz['total_time']:.1f}"
        })

    # Convert to dataframe and display
    quiz_df = pd.DataFrame(quiz_data)
    st.table(quiz_df)

    # Progress chart
    st.subheader("Your Progress Over Time")

    # Extract scores and dates for plotting
    dates = [quiz["date"] for quiz in st.session_state.quiz_history]
    percentages = [quiz["percentage"] for quiz in st.session_state.quiz_history]

    # Create line chart of progress
    if len(dates) > 1:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(range(len(dates)), percentages, marker='o', linestyle='-', color='blue')

        # Add labels to points
        for i, (d, p) in enumerate(zip(dates, percentages)):
            ax.annotate(f"{p:.1f}%", (i, p), textcoords="offset points", xytext=(0,10), ha='center')

        ax.set_ylabel('Score Percentage')
        ax.set_title('Quiz Progress Over Time')
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels([f"Quiz {i+1}" for i in range(len(dates))], rotation=45)
        ax.grid(True, linestyle='--', alpha=0.7)

        # Add a horizontal line at 70%
        ax.axhline(y=70, color='green', linestyle='--', alpha=0.7, label='Target (70%)')

        ax.legend()
        st.pyplot(fig)
    else:
        st.info("Take more quizzes to see your progress over time!")

    # Performance by operation type across all quizzes
    st.subheader("Overall Performance by Operation Type")

    # Collect all operation stats
    all_operation_stats = {}

    for quiz in st.session_state.quiz_history:
        # Process correct answers
        for ans in quiz['correct_answers']:
            operation = ans['operation']
            if operation not in all_operation_stats:
                all_operation_stats[operation] = {'correct': 0, 'total': 0}
            all_operation_stats[operation]['correct'] += 1
            all_operation_stats[operation]['total'] += 1

        # Process incorrect answers
        for ans in quiz['incorrect_answers']:
            operation = ans['operation']
            if operation not in all_operation_stats:
                all_operation_stats[operation] = {'correct': 0, 'total': 0}
            all_operation_stats[operation]['total'] += 1

    # Create data for chart
    op_labels = []
    op_percentages = []
    op_colors = []

    for op, stats in all_operation_stats.items():
        percentage = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0

        # Set color based on performance
        if percentage >= 80:
            color = "#4CAF50"  # Green
        elif percentage >= 60:
            color = "#FFC107"  # Yellow
        else:
            color = "#F44336"  # Red

        st.markdown(f"- **{op.capitalize()}**: {stats['correct']}/{stats['total']} correct ({percentage:.1f}%)")

        op_labels.append(op.capitalize())
        op_percentages.append(percentage)
        op_colors.append(color)

    # Create a pie chart if there's data
    if op_labels:
        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            op_percentages,
            labels=op_labels,
            autopct='%1.1f%%',
            colors=op_colors,
            startangle=90,
            wedgeprops={'edgecolor': 'w', 'linewidth': 1}
        )

        # Customize text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)

        ax.set_title('Performance by Operation Type')
        st.pyplot(fig)

    # View specific quiz details
    st.subheader("View Specific Quiz Details")

    quiz_to_view = st.selectbox(
        "Select a quiz to view details",
        [f"Quiz {i+1}: {quiz['quiz_type']} ({quiz['difficulty']}) - {quiz['date']}"
         for i, quiz in enumerate(st.session_state.quiz_history)]
    )

    if quiz_to_view:
        quiz_index = int(quiz_to_view.split(":")[0].replace("Quiz ", "")) - 1
        display_quiz_evaluation(st.session_state.quiz_history[quiz_index])

    # Button to clear history
    if st.button("Clear Quiz History"):
        st.session_state.quiz_history = []
        st.rerun()

def multiplication_tables_section():
    st.header("Multiplication Tables")

    col1, col2 = st.columns(2)

    with col1:
        number = st.number_input("Enter a number", min_value=1, max_value=100, value=5, step=1)
        range_end = st.number_input("Table range up to", min_value=10, max_value=30, value=10, step=1)

    with col2:
        st.markdown("### Table Display")

        # Generate the table
        table_data = []
        for i in range(1, range_end + 1):
            result = number * i
            table_data.append([f"{number} × {i}", "=", result])

        # Create a dataframe
        table_df = pd.DataFrame(table_data, columns=["Multiplication", "", "Result"])
        st.table(table_df)

    # Interactive Quiz based on the table
    st.markdown("---")
    st.subheader("Practice This Table")

    if st.button("Start Practice Quiz"):
        with st.form(key="practice_form"):
            questions = np.random.sample(range(1, range_end + 1), min(5, range_end))

            user_answers = []
            for q in questions:
                user_answer = st.number_input(f"{number} × {q} = ?", key=f"quiz_{q}", step=1)
                user_answers.append((q, user_answer))

            submit_practice = st.form_submit_button(label="Check Answers")

        if submit_practice:
            correct_count = 0
            for q, ans in user_answers:
                correct = number * q
                if ans == correct:
                    st.success(f"{number} × {q} = {correct} ✅")
                    correct_count += 1
                else:
                    st.error(f"{number} × {q} = {correct} ❌ (Your answer: {int(ans)})")

            # Display score
            st.markdown(f"### Practice Score: {correct_count}/{len(questions)}")
            if correct_count == len(questions):
                st.balloons()
                st.success("Perfect! You've mastered this table!")

def unit_converters_section():
    st.header("Unit Converters for Kids")

    conversion_type = st.selectbox(
        "What would you like to convert?",
        ["Length", "Weight", "Temperature", "Time"]
    )

    if conversion_type == "Length":
        length_converter()
    elif conversion_type == "Weight":
        weight_converter()
    elif conversion_type == "Temperature":
        temperature_converter()
    elif conversion_type == "Time":
        time_converter()

def length_converter():
    st.subheader("Length Converter")

    col1, col2, col3 = st.columns(3)

    with col1:
        input_value = st.number_input("Enter Value", min_value=0.0, step=0.1, value=1.0)

    with col2:
        from_unit = st.selectbox(
            "From",
            ["Millimeters (mm)", "Centimeters (cm)", "Meters (m)", "Kilometers (km)",
             "Inches (in)", "Feet (ft)", "Yards (yd)", "Miles (mi)"]
        )

    with col3:
        to_unit = st.selectbox(
            "To",
            ["Centimeters (cm)", "Millimeters (mm)", "Meters (m)", "Kilometers (km)",
             "Inches (in)", "Feet (ft)", "Yards (yd)", "Miles (mi)"]
        )

    # Convert everything to meters first
    length_in_meters = 0

    # Convert from unit to meters
    if from_unit == "Millimeters (mm)":
        length_in_meters = input_value / 1000
    elif from_unit == "Centimeters (cm)":
        length_in_meters = input_value / 100
    elif from_unit == "Meters (m)":
        length_in_meters = input_value
    elif from_unit == "Kilometers (km)":
        length_in_meters = input_value * 1000
    elif from_unit == "Inches (in)":
        length_in_meters = input_value * 0.0254
    elif from_unit == "Feet (ft)":
        length_in_meters = input_value * 0.3048
    elif from_unit == "Yards (yd)":
        length_in_meters = input_value * 0.9144
    elif from_unit == "Miles (mi)":
        length_in_meters = input_value * 1609.34

    # Convert from meters to target unit
    result = 0
    if to_unit == "Millimeters (mm)":
        result = length_in_meters * 1000
    elif to_unit == "Centimeters (cm)":
        result = length_in_meters * 100
    elif to_unit == "Meters (m)":
        result = length_in_meters
    elif to_unit == "Kilometers (km)":
        result = length_in_meters / 1000
    elif to_unit == "Inches (in)":
        result = length_in_meters / 0.0254
    elif to_unit == "Feet (ft)":
        result = length_in_meters / 0.3048
    elif to_unit == "Yards (yd)":
        result = length_in_meters / 0.9144
    elif to_unit == "Miles (mi)":
        result = length_in_meters / 1609.34

    st.markdown("---")
    st.markdown(f"### Result: {input_value} {from_unit.split('(')[0].strip()} = {result:.4f} {to_unit.split('(')[0].strip()}")

    # Visual representation
    if from_unit.startswith(("Millimeters", "Centimeters", "Meters", "Kilometers")) and to_unit.startswith(("Millimeters", "Centimeters", "Meters", "Kilometers")):
        st.markdown("### Visual Comparison")
        from_size = input_value if from_unit == "Centimeters (cm)" else input_value * 100 if from_unit == "Meters (m)" else input_value * 0.1 if from_unit == "Millimeters (mm)" else input_value * 100000
        to_size = result if to_unit == "Centimeters (cm)" else result * 100 if to_unit == "Meters (m)" else result * 0.1 if to_unit == "Millimeters (mm)" else result * 100000

        max_size = max(from_size, to_size)
        scale_factor = 100 / max_size if max_size > 100 else 1

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"{from_unit.split('(')[0].strip()}")
            st.progress(min(from_size * scale_factor / 100, 1.0))
        with col2:
            st.markdown(f"{to_unit.split('(')[0].strip()}")
            st.progress(min(to_size * scale_factor / 100, 1.0))

    # Fun facts about length
    st.markdown("---")
    st.subheader("Fun Facts About Length")
    length_facts = [
        "An ant is about 5 millimeters long!",
        "A typical pencil is about 18 centimeters long.",
        "The average height of a 7-year-old child is about 1.2 meters.",
        "The tallest building in the world, the Burj Khalifa, is 828 meters tall!",
        "Light travels about 300,000 kilometers in just one second!",
        "A dollar bill is about 6 inches long.",
        "A typical school bus is about 35 feet long.",
        "A football field is 100 yards long."
    ]
    st.info(np.random.choice(length_facts))

def weight_converter():
    st.subheader("Weight Converter")

    col1, col2, col3 = st.columns(3)

    with col1:
        input_value = st.number_input("Enter Value", min_value=0.0, step=0.1, value=1.0)

    with col2:
        from_unit = st.selectbox(
            "From",
            ["Grams (g)", "Kilograms (kg)", "Ounces (oz)", "Pounds (lb)"]
        )

    with col3:
        to_unit = st.selectbox(
            "To",
            ["Kilograms (kg)", "Grams (g)", "Ounces (oz)", "Pounds (lb)"]
        )

    # Convert everything to grams first
    weight_in_grams = 0

    # Convert from unit to grams
    if from_unit == "Grams (g)":
        weight_in_grams = input_value
    elif from_unit == "Kilograms (kg)":
        weight_in_grams = input_value * 1000
    elif from_unit == "Ounces (oz)":
        weight_in_grams = input_value * 28.3495
    elif from_unit == "Pounds (lb)":
        weight_in_grams = input_value * 453.592

    # Convert from grams to target unit
    result = 0
    if to_unit == "Grams (g)":
        result = weight_in_grams
    elif to_unit == "Kilograms (kg)":
        result = weight_in_grams / 1000
    elif to_unit == "Ounces (oz)":
        result = weight_in_grams / 28.3495
    elif to_unit == "Pounds (lb)":
        result = weight_in_grams / 453.592

    st.markdown("---")
    st.markdown(f"### Result: {input_value} {from_unit.split('(')[0].strip()} = {result:.4f} {to_unit.split('(')[0].strip()}")

    # Fun facts about weight
    st.markdown("---")
    st.subheader("Fun Facts About Weight")
    weight_facts = [
        "A paperclip weighs about 1 gram.",
        "A typical apple weighs about 100 grams.",
        "A liter of water weighs exactly 1 kilogram!",
        "A typical car weighs around 1,500 kilograms.",
        "A slice of bread weighs about 1 ounce.",
        "A typical baseball weighs about 5 ounces.",
        "A typical textbook weighs about 1 pound.",
        "A gallon of milk weighs about 8.6 pounds."
    ]
    st.info(np.random.choice(weight_facts))

def temperature_converter():
    st.subheader("Temperature Converter")

    col1, col2, col3 = st.columns(3)

    with col1:
        input_value = st.number_input("Enter Temperature", value=20.0, step=0.1)

    with col2:
        from_unit = st.selectbox(
            "From",
            ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]
        )

    with col3:
        to_unit = st.selectbox(
            "To",
            ["Fahrenheit (°F)", "Celsius (°C)", "Kelvin (K)"]
        )

    # Convert everything to Celsius first
    temp_in_celsius = 0

    # Convert from unit to Celsius
    if from_unit == "Celsius (°C)":
        temp_in_celsius = input_value
    elif from_unit == "Fahrenheit (°F)":
        temp_in_celsius = (input_value - 32) * 5/9
    elif from_unit == "Kelvin (K)":
        temp_in_celsius = input_value - 273.15

    # Convert from Celsius to target unit
    result = 0
    if to_unit == "Celsius (°C)":
        result = temp_in_celsius
    elif to_unit == "Fahrenheit (°F)":
        result = (temp_in_celsius * 9/5) + 32
    elif to_unit == "Kelvin (K)":
        result = temp_in_celsius + 273.15

    st.markdown("---")
    st.markdown(f"### Result: {input_value} {from_unit.split('(')[0].strip()} = {result:.2f} {to_unit.split('(')[0].strip()}")

    # Visual representation
    st.markdown("### Temperature Scale")

    # Create a temperature scale
    temp_scale = pd.DataFrame({
        "Celsius": np.arange(-30, 110, 10),
        "Fahrenheit": np.arange(-30, 110, 10) * 9/5 + 32,
        "Kelvin": np.arange(-30, 110, 10) + 273.15
    })

    # Determine where the converted temperatures fall on the scale
    from_temp_celsius = temp_in_celsius
    to_temp_celsius = temp_in_celsius

    # Visual temperature scale
    st.markdown("Temperature ranges:")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Frozen Water: 0°C / 32°F / 273.15K")
        st.write("Room Temperature: ~20-25°C / ~68-77°F / ~293-298K")
        st.write("Body Temperature: 37°C / 98.6°F / 310.15K")

    with col2:
        st.write("Boiling Water: 100°C / 212°F / 373.15K")
        if -10 <= temp_in_celsius <= 40:
            if temp_in_celsius <= 0:
                st.info(f"At this temperature, water freezes! ❄️")
            elif temp_in_celsius >= 30:
                st.warning(f"This is a hot day! 🔥")
            elif 15 <= temp_in_celsius <= 25:
                st.success(f"This is a comfortable room temperature. 😊")

    # Fun facts about temperature
    st.markdown("---")
    st.subheader("Fun Facts About Temperature")
    temp_facts = [
        "The coldest temperature ever recorded on Earth was -89.2°C (-128.6°F) in Antarctica.",
        "The hottest temperature ever recorded on Earth was 56.7°C (134°F) in Death Valley, California.",
        "Water freezes at 0°C (32°F) and boils at 100°C (212°F) at sea level.",
        "The average human body temperature is about 37°C (98.6°F).",
        "Absolute zero, the lowest possible temperature, is -273.15°C (-459.67°F) or 0 Kelvin.",
        "Room temperature is typically between 20°C and 25°C (68°F to 77°F).",
        "The temperature on the surface of the Sun is about 5,500°C (9,940°F)!",
        "A fever is usually defined as a body temperature above 38°C (100.4°F)."
    ]
    st.info(np.random.choice(temp_facts))

def time_converter():
    st.subheader("Time Converter")

    col1, col2, col3 = st.columns(3)

    with col1:
        input_value = st.number_input("Enter Value", min_value=0.0, step=1.0, value=1.0)

    with col2:
        from_unit = st.selectbox(
            "From",
            ["Seconds", "Minutes", "Hours", "Days", "Weeks"]
        )

    with col3:
        to_unit = st.selectbox(
            "To",
            ["Minutes", "Seconds", "Hours", "Days", "Weeks"]
        )

    # Convert everything to seconds first
    time_in_seconds = 0

    # Convert from unit to seconds
    if from_unit == "Seconds":
        time_in_seconds = input_value
    elif from_unit == "Minutes":
        time_in_seconds = input_value * 60
    elif from_unit == "Hours":
        time_in_seconds = input_value * 3600
    elif from_unit == "Days":
        time_in_seconds = input_value * 86400
    elif from_unit == "Weeks":
        time_in_seconds = input_value * 604800

    # Convert from seconds to target unit
    result = 0
    if to_unit == "Seconds":
        result = time_in_seconds
    elif to_unit == "Minutes":
        result = time_in_seconds / 60
    elif to_unit == "Hours":
        result = time_in_seconds / 3600
    elif to_unit == "Days":
        result = time_in_seconds / 86400
    elif to_unit == "Weeks":
        result = time_in_seconds / 604800

    st.markdown("---")
    st.markdown(f"### Result: {input_value} {from_unit} = {result:.4f} {to_unit}")

    # Fun facts about time
    st.markdown("---")
    st.subheader("Fun Facts About Time")
    time_facts = [
        "There are 60 seconds in a minute.",
        "There are 60 minutes in an hour.",
        "There are 24 hours in a day.",
        "There are 7 days in a week.",
        "There are about 365 days in a year (actually 365.25, which is why we have leap years!).",
        "Light travels about 300,000 kilometers (186,000 miles) in just one second!",
        "It takes about 8 minutes for sunlight to reach Earth.",
        "A day on planet Venus is longer than its year!"
    ]
    st.info(np.random.choice(time_facts))

if __name__ == "__main__":
    main()
