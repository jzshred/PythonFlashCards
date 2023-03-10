from subject import Subject
from random_subject import RandomSubject


class Flashcard:
    """A class for running Python Q&A sessions."""

    def __init__(self):
        self._subjects_folder = "subjects/"
        self._subjects = ["Built-in Functions", "Strings", "Lists", "Dictionaries", "Tuples", "Sets",
                          "Functions", "Classes", "File Handling", "Math Library", "Random Questions"]
        self._chosen_subject = None
        self._chosen_subject_address = None
        self._questions = []
        self._answers = []
        self._intro_displayed = False
        self._quit_session = False
        self._correct_answers = 0
        self._incorrect_answers = 0

    def start(self):
        if not self._quit_session:
            self._display_intro()
            self._display_subjects()
            self._choose_subject()
            if not self._quit_session:
                self._parse_address()
                self._build_qa_session()
                self._display_subject_title()
                self._ask_questions()
                self._display_score()
                self._ask_to_continue()
                self.start()

    def _display_intro(self):
        if not self._intro_displayed:
            title_length = 35
            banner = "=" * title_length
            title = "Python Q&A Session"
            print(banner)
            print(title.center(title_length))
            print(banner)
            self._intro_displayed = True

    def _display_subjects(self):
        print("Choose your subject:")
        for i, j in enumerate(self._subjects):
            print(f"{(i + 1):>2}. {j}")
        print("On any question, input 'q' to quit.")

    def _choose_subject(self):
        chosen_subject = input()
        try:
            self._check_valid_subject(chosen_subject)
        except ValueError:
            self._check_quit_session(chosen_subject)

    def _check_valid_subject(self, chosen_subject):
        chosen_subject = int(chosen_subject) - 1
        if chosen_subject in range(len(self._subjects)):
            self._chosen_subject = self._subjects[chosen_subject]
        else:
            self._invalid_subject()

    def _check_quit_session(self, chosen_subject):
        if chosen_subject.lower() == 'q':
            self._display_score()
            self._quit_session = True
        else:
            self._invalid_subject()

    def _invalid_subject(self):
        print("Invalid option. Please choose again.")
        self._choose_subject()

    def _parse_address(self):
        if self._chosen_subject == "Random Questions":
            self._chosen_subject_address = []
            for subject in self._subjects[:-1]:
                parsed_subject = f"{self._subjects_folder}{subject.lower().replace(' ', '_')}"
                self._chosen_subject_address.append(parsed_subject)
        else:
            self._chosen_subject_address = \
                f"{self._subjects_folder}{self._chosen_subject.lower().replace(' ', '_')}"

    def _build_qa_session(self):
        if self._chosen_subject == "Random Questions":
            qa_session = RandomSubject(self._chosen_subject_address)
        else:
            qa_session = Subject(self._chosen_subject_address)
        self._questions = qa_session.questions
        self._answers = qa_session.answers

    def _display_subject_title(self):
        print(f"\n--- {self._chosen_subject}: {len(self._questions)} questions ---")

    def _ask_questions(self):
        for question_number, question in enumerate(self._questions):
            print(f"Q{question_number + 1}. {question[:-1]}")
            response = self._check_answer(question_number)
            if response == "quit":
                self._quit_session = True
                break
            else:
                self._compute_score(response)

    def _check_answer(self, question_number):
        answer = input()
        answer_without_whitespaces = self._remove_whitespaces(answer)
        correct_answer = self._answers[question_number][:-1]
        correct_answer_without_whitespaces = self._remove_whitespaces(correct_answer)
        if answer_without_whitespaces == correct_answer_without_whitespaces:
            print("Correct!\n")
            return "correct"
        elif answer.lower() == 'q':
            return "quit"
        else:
            print("Incorrect. The correct answer is:")
            print(correct_answer, "\n")
            return "incorrect"

    @staticmethod
    def _remove_whitespaces(text):
        return text.replace(" ", "")

    def _compute_score(self, response):
        if response == "correct":
            self._correct_answers += 1
        elif response == "incorrect":
            self._incorrect_answers += 1

    def _display_score(self):
        total_answers = self._correct_answers + self._incorrect_answers
        if total_answers > 0:
            print("\n--- Results ---")
            print(f"Correct answers: {self._correct_answers}")
            print(f"Incorrect answers: {self._incorrect_answers}")
            accuracy = self._correct_answers / total_answers
            print(f"Accuracy rate: {accuracy:.2%}")

    def _ask_to_continue(self):
        if not self._quit_session:
            print("\nWould you like to continue with another subject? (y/n)")
            continue_with_qa = input()
            if continue_with_qa.lower() != 'y':
                self._quit_session = True
