import pandas as pd
import os
from datetime import datetime

QUESTIONS_FILE = "questions.csv"
RESULTS_FILE = "results.csv"

def load_questions(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        exit()

def get_valid_answer():
    while True:
        ans = input("Your answer (A/B/C/D): ").strip().upper()
        if ans in ['A', 'B', 'C', 'D']:
            return ans
        print("Invalid input. Please enter A, B, C, or D.")

def calculate_feedback(score, total):
    percentage = (score / total) * 100
    if percentage >= 80:
        remark = "Excellent performance!"
    elif percentage >= 50:
        remark = "Good job, keep practicing."
    else:
        remark = "You can do better next time!"
    return percentage, remark

def save_result(name, score, total):
    percentage, remark = calculate_feedback(score, total)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "Name": name,
        "Score": f"{score}/{total}",
        "Percentage": f"{percentage:.2f}%",
        "Remark": remark,
        "Timestamp": now
    }
    file_exists = os.path.isfile(RESULTS_FILE)
    df_row = pd.DataFrame([row])
    if file_exists:
        df_row.to_csv(RESULTS_FILE, mode='a', header=False, index=False)
    else:
        df_row.to_csv(RESULTS_FILE, index=False)

def run_quiz(questions_df):
    while True:
        score = 0
        name = input("Enter your name: ").strip()
        if not name:
            name = "Player"

        print(f"\nHello {name}, welcome to the Quiz!\n")

        for index, row in questions_df.iterrows():
            print(f"Q{index+1}: {row['question']}")
            print(f"A. {row['optionA']}")
            print(f"B. {row['optionB']}")
            print(f"C. {row['optionC']}")
            print(f"D. {row['optionD']}")

            user_answer = get_valid_answer()

            if user_answer == row['answer'].strip().upper():
                print("Correct!\n")
                score += 1
            else:
                print(f"Wrong! The correct answer is {row['answer']}\n")

        total = len(questions_df)
        percentage, remark = calculate_feedback(score, total)
        print(f"Quiz completed! {name}, your final score is {score} out of {total}.")
        print(f"Percentage: {percentage:.2f}%")
        print(remark)

        save_result(name, score, total)
        print(f"Your result has been saved in {RESULTS_FILE}.\n")

        again = input("Do you want to play again? (Y/N): ").strip().upper()
        if again != 'Y':
            print("Thank you for playing. Goodbye!")
            break

def main():
    questions = load_questions(QUESTIONS_FILE)
    run_quiz(questions)

if __name__ == "__main__":
    main()
