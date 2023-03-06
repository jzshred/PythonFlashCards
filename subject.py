class Subject:
    """A class for holding questions and answers from a particular subject."""

    def __init__(self, chosen_subject):
        self.questions = []
        self.answers = []

        self._set_questions(chosen_subject)
        self._set_answers(chosen_subject)

    def _set_questions(self, chosen_subject):
        filename = chosen_subject + "_questions.txt"
        with open(filename) as file_object:
            self.questions = file_object.readlines()

    def _set_answers(self, chosen_subject):
        filename = chosen_subject + "_answers.txt"
        with open(filename) as file_object:
            self.answers = file_object.readlines()
