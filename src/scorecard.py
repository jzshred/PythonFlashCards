class Scorecard:
    """A class for holding scores for Q&A sessions."""

    def __init__(self, subjects):
        self._subjects = subjects
        self._correct_answers = [0] * len(subjects)
        self._incorrect_answers = [0] * len(subjects)
        self._accuracy_rates = [0.0] * len(subjects)
        self._total_results = [0, 0, 0.0]

    def _print_current_session(self, subject):
        index = self._subjects.index(subject)
        print("--- Current Session ---\n"
              f"Subject:   {self._subjects[index]}\n"
              f"Correct:   {self._correct_answers[index]}\n"
              f"Incorrect: {self._incorrect_answers[index]}\n"
              f"Accuracy:  {self._accuracy_rates[index]:.2%}")

    def _print_all_sessions(self):
        char_count = [len(subject) for subject in self._subjects]
        spacing = max(char_count)

        scores = "\n--- All Sessions ---\n"
        scores += "Subject".ljust(spacing)
        scores += "\tCor Inc Acc\n"
        for i in range(len(self._subjects)):
            scores += self._subjects[i].ljust(spacing)
            scores += (f"\t{self._correct_answers[i]:<4}"
                       f"{self._incorrect_answers[i]:<4}"
                       f"{self._accuracy_rates[i]:<.2%}\n")

        scores += "-" * spacing
        scores += "\n"
        scores += "Total".ljust(spacing)
        scores += (f"\t{self._total_results[0]:<4}"
                   f"{self._total_results[1]:<4}"
                   f"{self._total_results[2]:<.2%}")

        print(scores)

    def _compute_accuracy(self):
        for i in range(len(self._accuracy_rates)):
            total_answers = self._correct_answers[i] + self._incorrect_answers[i]
            if total_answers > 0:
                self._accuracy_rates[i] = self._correct_answers[i] / total_answers

    def _compute_total(self):
        total_correct = sum(self._correct_answers)
        total_incorrect = sum(self._incorrect_answers)
        total_answers = total_correct + total_incorrect
        if total_answers > 0:
            total_accuracy = total_correct/total_answers
            self._total_results[0] = total_correct
            self._total_results[1] = total_incorrect
            self._total_results[2] = total_accuracy

    def log_score(self, answer, subject):
        index = self._subjects.index(subject)
        if answer == "correct":
            self._correct_answers[index] += 1
        elif answer == "incorrect":
            self._incorrect_answers[index] += 1
        self._compute_accuracy()
        self._compute_total()

    def print_results(self, subject=None):
        if subject is not None:
            self._print_current_session(subject)
        self._print_all_sessions()
