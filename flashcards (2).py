import random
def load_scores(filename="scores.txt"):
    try:
        with open("scores.txt", "r") as score_file:
            user_scores = {}
            for line in score_file:
                name, scores = line.strip().split(":")
                scores_list = list(map(int, scores.split(",")))
                user_scores[name] = scores_list
    except FileNotFoundError:
        user_scores = {}
    return user_scores
def load_questions(filename="reviewmaterial.txt"):
    categories = {}
    current_category = None
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_category = line[1:-1]
                categories[current_category] = {}
            elif "?" in line and current_category:
                question_mark_index = line.find("?")
                question = line[:question_mark_index + 1].strip()
                answer = line[question_mark_index + 1:].strip()
                categories[current_category][question] = answer
    return categories

def display_categories(categories):
    print("Available categories:")
    for idx, category in enumerate(categories.keys(), start=1):
        print(f"{idx}. {category}")
def select_category(categories):
    while True:
        try:
            category_choice = int(input("Choose a category by number: "))
            if 1 <= category_choice <= len(categories):
                selected_category = list(categories.keys())[category_choice - 1]
                print(f"You selected: {selected_category}")
                return categories[selected_category]
            else:
                print("Invalid choice. Please select a valid category number.")
        except ValueError:
            print("Please enter a number corresponding to your choice.")
def welcome_user(user_scores):
    username = input("Enter a username: ").strip()
    if username in user_scores:
        highest_score = max(user_scores[username])
        print(f"Welcome back, {username}! Your highest score is {highest_score}.")
    else:
        print(f"Hi, {username}! This is your first time here.")
        user_scores[username] = []
    return username

def ask_max_wrong():
    while True:
        try:
            maxWrong = int(input("What is the max number of wrong answers? "))
            return maxWrong
        except ValueError:
            print("Please enter a valid integer.")

def ask_questions(questionsDict, maxWrong):
    correct = 0
    incorrect = 0
    questions_list = list(questionsDict.items())
    random.shuffle(questions_list)

    for n, (question, answer) in enumerate(questions_list, start=1):
        if incorrect >= maxWrong:
            print("You lose!")
            break
        print(f"\nQuestion {n}:")
        userAnswer = input(f"{question} ").strip()
        if userAnswer.lower() == "stop":
            print("Game stopped by user.")
            break
        elif userAnswer.lower() == "?":
            print(f"Hint: The answer starts with '{answer[0]}'.")
            userAnswer = input(f"Try again: {question} ").strip()

        if userAnswer.lower() != answer.lower():
            print(f"❌ Incorrect! The correct answer is: {answer}")
            incorrect += 1
        else:
            print("⭐Correct!⭐")
            correct += 1

    print("\nQuiz Finished!")
    print(f"Correct Answers: {correct}")
    print(f"Wrong Answers: {incorrect}")
    return correct

def update_scores(user_scores, username, correct):
    user_scores[username].append(correct)
    highest_score = max(user_scores[username])
    if len(user_scores[username]) == 1 and correct == highest_score:
        print(f"🎉 New high score! This is your first score!")
    elif correct == highest_score:
        print(f"🎉 New high score!")
    else:
        print(f"Your highest score remains {highest_score}.")

def add_score(user_scores, filename="scores.txt"):
    with open(filename, "w") as score_file:
        for name, scores in user_scores.items():
            score_file.write(f"{name}:{','.join(map(str, scores))}\n")
def main():
    user_scores = load_scores()
    categories = load_questions()
    display_categories(categories)
    questionsDict = select_category(categories)
    username = welcome_user(user_scores)
    maxWrong = ask_max_wrong()
    correct = ask_questions(questionsDict, maxWrong)
    update_scores(user_scores, username, correct)
    add_score(user_scores)
if __name__ == "__main__":
    main()
