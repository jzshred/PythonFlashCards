from random import randrange
from subject import Subject


class RandomSubject:
    """A class for holding questions and answers from random subjects."""

    def __init__(self, subjects, total_questions=10):
        self.questions = []
        self.answers = []

        self.__chosen_subject = None
        self.__subject_qa = None
        self.__random_question_number = None

        self.__build_random_qa(subjects, total_questions)

    def __choose_random_subject(self, subjects):
        self.__chosen_subject = subjects[randrange(len(subjects))]

    def __build_subject_qa(self):
        self.__subject_qa = Subject(self.__chosen_subject)

    def __choose_random_question_number(self):
        self.__random_question_number = randrange(len(self.__subject_qa.questions))

    def __add_random_question(self):
        if self.__subject_qa.questions[self.__random_question_number] not in self.questions:
            self.questions.append(self.__subject_qa.questions[self.__random_question_number])

    def __add_random_answer(self):
        if self.__subject_qa.answers[self.__random_question_number] not in self.answers:
            self.answers.append(self.__subject_qa.answers[self.__random_question_number])

    def __build_random_qa(self, subjects, total_questions):
        while len(self.questions) < total_questions:
            self.__choose_random_subject(subjects)
            self.__build_subject_qa()
            self.__choose_random_question_number()
            self.__add_random_question()
            self.__add_random_answer()
