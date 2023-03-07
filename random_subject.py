from random import randrange
from subject import Subject


class RandomSubject:
    """A class for holding questions and answers from random subjects."""

    def __init__(self, subjects, total_questions=10):
        self.questions = []
        self.answers = []

        self._chosen_subject = None
        self._subject_qa = None
        self._random_question_number = None

        self._set_random_qa(subjects, total_questions)

    def _set_random_subject(self, subjects):
        self._chosen_subject = subjects[randrange(len(subjects))]

    def _set_subject_qa(self):
        self._subject_qa = Subject(self._chosen_subject)

    def _set_random_question_number(self):
        self._random_question_number = randrange(len(self._subject_qa.questions))

    def _set_random_question(self):
        if self._subject_qa.questions[self._random_question_number] not in self.questions:
            self.questions.append(self._subject_qa.questions[self._random_question_number])

    def _set_random_answer(self):
        if self._subject_qa.answers[self._random_question_number] not in self.answers:
            self.answers.append(self._subject_qa.answers[self._random_question_number])

    def _set_random_qa(self, subjects, total_questions):
        while len(self.questions) < total_questions:
            self._set_random_subject(subjects)
            self._set_subject_qa()
            self._set_random_question_number()
            self._set_random_question()
            self._set_random_answer()
