from random import randrange


class Flashcard:
    """A class for running Python Q&A sessions."""

    def __init__(self):
        self.__subjects_folder = "subjects/"
        self.__subjects = ["Built-in functions", "Strings", "Lists", "Dictionaries", "Tuples", "Sets",
                           "Functions", "Classes", "File handling", "Math library", "Random questions"]
        self.__chosen_subject = 0
        self.__subject_questions = []
        self.__subject_answers = []
        self.__number_of_questions_in_subject = 0

        self.__random_subject = len(self.__subjects) - 1
        self.__random_questions = []
        self.__random_answers = []
        self.__number_of_random_questions = 10
        self.__random_question_number = 0

        self.__correct_answers = 0
        self.__incorrect_answers = 0
        self.__intro_displayed = False
        self.__quit_session = False

    def start(self):
        if not self.__quit_session:
            self.__display_intro()
            self.__display_subjects()
            self.__choose_subject()
            if not self.__quit_session:
                self.__build_qa_session()
                self.__display_subject_title()
                self.__ask_questions()
                self.__display_score()
                self.__ask_to_continue()
                self.start()

    def __display_intro(self):
        if not self.__intro_displayed:
            title_length = 35
            banner = "=" * title_length
            title = "Python Q&A Session"
            print(banner)
            print(title.center(title_length))
            print(banner)
            self.__intro_displayed = True

    def __display_subjects(self):
        print("Choose your subject:")
        for i, j in enumerate(self.__subjects):
            print(f"{(i + 1):>2}. {j}")
        print("On any question, input 'q' to quit.")

    def __choose_subject(self):
        chosen_subject = input()
        try:
            self.__check_valid_subject(chosen_subject)
        except ValueError:
            self.__check_quit_session(chosen_subject)

    def __check_valid_subject(self, chosen_subject):
        chosen_subject = int(chosen_subject)
        if 1 <= chosen_subject <= len(self.__subjects):
            self.__chosen_subject = chosen_subject - 1
        else:
            self.__invalid_subject()

    def __check_quit_session(self, chosen_subject):
        if chosen_subject.lower() == 'q':
            self.__display_score()
            self.__quit_session = True
        else:
            self.__invalid_subject()

    def __invalid_subject(self):
        print("Invalid option. Please choose again.")
        self.__choose_subject()

    def __build_qa_session(self):
        if self.__chosen_subject == self.__random_subject:
            self.__build_random_qa_session()
        else:
            self.__build_subject_qa_session()

    def __build_subject_qa_session(self):
        self.__clear_subject_qa_session()
        self.__build_subject_questions()
        self.__build_subject_answers()

    def __clear_subject_qa_session(self):
        self.__subject_questions.clear()
        self.__subject_answers.clear()

    def __build_subject_questions(self):
        filename = self.__subjects_folder \
            + self.__subjects[self.__chosen_subject].lower().replace(' ', '_') \
            + "_questions.txt"
        with open(filename) as file_object:
            self.__subject_questions = file_object.readlines()

    def __build_subject_answers(self):
        filename = self.__subjects_folder\
            + self.__subjects[self.__chosen_subject].lower().replace(' ', '_')\
            + "_answers.txt"
        with open(filename) as file_object:
            self.__subject_answers = file_object.readlines()

    def __build_random_qa_session(self):
        self.__clear_random_qa_session()
        while len(self.__random_questions) < self.__number_of_random_questions:
            self.__choose_random_subject()
            self.__build_subject_qa_session()
            self.__choose_random_question_number()
            self.__build_random_question()
            self.__build_random_answer()
        self.__copy_random_questions_and_answers()
        self.__reset_random_subject()

    def __clear_random_qa_session(self):
        self.__random_questions.clear()
        self.__random_answers.clear()

    def __choose_random_subject(self):
        self.__chosen_subject = randrange(self.__random_subject)

    def __choose_random_question_number(self):
        self.__random_question_number = randrange(len(self.__subject_questions))

    def __build_random_question(self):
        if self.__subject_questions[self.__random_question_number] not in self.__random_questions:
            self.__random_questions.append(self.__subject_questions[self.__random_question_number])

    def __build_random_answer(self):
        if self.__subject_answers[self.__random_question_number] not in self.__random_answers:
            self.__random_answers.append(self.__subject_answers[self.__random_question_number])

    def __copy_random_questions_and_answers(self):
        self.__subject_questions = self.__random_questions
        self.__subject_answers = self.__random_answers

    def __reset_random_subject(self):
        self.__chosen_subject = self.__random_subject

    def __display_subject_title(self):
        self.__set_number_of_questions_in_subject()
        print(f"\n--- {self.__subjects[self.__chosen_subject]}: {self.__number_of_questions_in_subject} questions ---")

    def __set_number_of_questions_in_subject(self):
        if self.__chosen_subject == self.__random_subject:
            self.__number_of_questions_in_subject = self.__number_of_random_questions
        else:
            self.__number_of_questions_in_subject = len(self.__subject_questions)

    def __ask_questions(self):
        for question_number, question in enumerate(self.__subject_questions):
            print(f"Q{question_number + 1}. {question[:-1]}")
            response = self.__check_answer(question_number)
            if response == "quit":
                self.__quit_session = True
                break
            else:
                self.__compute_score(response)

    def __check_answer(self, question_number):
        answer = input()
        answer_without_whitespaces = self.__remove_whitespaces(answer)
        correct_answer = self.__subject_answers[question_number][:-1]
        correct_answer_without_whitespaces = self.__remove_whitespaces(correct_answer)
        if answer_without_whitespaces == correct_answer_without_whitespaces:
            print("Correct!")
            return "correct"
        elif answer.lower() == 'q':
            return "quit"
        else:
            print("Incorrect. The correct answer is:")
            print(correct_answer)
            return "incorrect"

    @staticmethod
    def __remove_whitespaces(text):
        return text.replace(" ", "")

    def __compute_score(self, response):
        if response == "correct":
            self.__correct_answers += 1
        elif response == "incorrect":
            self.__incorrect_answers += 1

    def __display_score(self):
        total_answers = self.__correct_answers + self.__incorrect_answers
        if total_answers > 0:
            print("\n--- Results ---")
            print(f"Correct answers: {self.__correct_answers}")
            print(f"Incorrect answers: {self.__incorrect_answers}")
            accuracy = self.__correct_answers / total_answers
            print(f"Accuracy rate: {accuracy:.2%}")

    def __ask_to_continue(self):
        if not self.__quit_session:
            print("\nWould you like to continue with another subject? (y/n)")
            continue_with_qa = input()
            if continue_with_qa.lower() != 'y':
                self.__quit_session = True
