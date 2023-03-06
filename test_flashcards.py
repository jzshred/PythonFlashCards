import pytest
from flashcards import Flashcard


@pytest.fixture()
def cardset():
    return Flashcard()


@pytest.fixture()
def cardset_with_subject(cardset):
    """Return a Flashcard object with built answers."""
    cardset._Flashcard__chosen_subject = 0
    cardset._Flashcard__build_subject_qa_session()
    return cardset


def test_choose_subject_case_valid_subject(cardset, monkeypatch):
    chosen_subject = 1
    monkeypatch.setattr("builtins.input", lambda: chosen_subject)
    cardset._Flashcard__choose_subject()
    assert cardset._Flashcard__chosen_subject == 0


def test_choose_subject_case_quit_session(cardset, monkeypatch):
    chosen_subject = 'q'
    monkeypatch.setattr("builtins.input", lambda: chosen_subject)
    cardset._Flashcard__choose_subject()
    assert cardset._Flashcard__quit_session


def test_build_subject_qa_session_case_length(cardset):
    """Test that each subject's questions and answers match in length."""
    for i in range(len(cardset._Flashcard__subjects) - 1):
        cardset._Flashcard__chosen_subject = i
        cardset._Flashcard__build_subject_qa_session()
        assert len(cardset._Flashcard__subject_questions) == \
               len(cardset._Flashcard__subject_answers)


def test_choose_random_subject(cardset):
    """Test that the chosen random subject is within the range of available subjects."""
    cardset._Flashcard__choose_random_subject()
    assert cardset._Flashcard__chosen_subject in range(cardset._Flashcard__random_subject)


def test_choose_random_question_number(cardset_with_subject):
    """Test that the chosen question number is within the range of available questions."""
    cardset_with_subject._Flashcard__choose_random_question_number()
    assert cardset_with_subject._Flashcard__random_question_number \
           in range(len(cardset_with_subject._Flashcard__subject_questions))


def test_build_random_qa_session_questions(cardset):
    """Test that the random Q&A session gets created with the correct number of questions."""
    cardset._Flashcard__build_random_qa_session()
    assert len(cardset._Flashcard__subject_questions) == cardset._Flashcard__number_of_random_questions


def test_build_random_qa_session_answers(cardset):
    """Test that the random Q&A session gets created with the correct number of answers."""
    cardset._Flashcard__build_random_qa_session()
    assert len(cardset._Flashcard__subject_answers) == cardset._Flashcard__number_of_random_questions


def test_set_number_of_questions_in_subject_case_subject(cardset_with_subject):
    cardset_with_subject._Flashcard__set_number_of_questions_in_subject()
    assert cardset_with_subject._Flashcard__number_of_questions_in_subject \
           == len(cardset_with_subject._Flashcard__subject_questions)


def test_set_number_of_questions_in_subject_case_random(cardset):
    cardset._Flashcard__chosen_subject = cardset._Flashcard__random_subject
    cardset._Flashcard__set_number_of_questions_in_subject()
    assert cardset._Flashcard__number_of_questions_in_subject == cardset._Flashcard__number_of_random_questions


def test_display_subject_title_case_subject(cardset_with_subject, capsys):
    cardset_with_subject._Flashcard__display_subject_title()
    stdout, stderr = capsys.readouterr()
    assert stdout == (f"\n--- "
                      f"{cardset_with_subject._Flashcard__subjects[cardset_with_subject._Flashcard__chosen_subject]}: "
                      f"{cardset_with_subject._Flashcard__number_of_questions_in_subject} questions ---\n")


def test_display_subject_title_case_random(cardset, capsys):
    cardset._Flashcard__chosen_subject = cardset._Flashcard__random_subject
    cardset._Flashcard__display_subject_title()
    stdout, stderr = capsys.readouterr()
    assert stdout == (f"\n--- "
                      f"{cardset._Flashcard__subjects[cardset._Flashcard__random_subject]}: "
                      f"{cardset._Flashcard__number_of_random_questions} questions ---\n")


def test_remove_whitespaces(cardset):
    answer = "(a, b, c)"
    answer_without_whitespaces = cardset._Flashcard__remove_whitespaces(answer)
    assert answer_without_whitespaces == "(a,b,c)"


@pytest.mark.parametrize("mock_answer, expected_result",
                         [("type(num)", "correct"), ("type ( num ) ", "correct"), ('q', "quit"), ('a', "incorrect")])
def test_check_answer(cardset_with_subject, monkeypatch, mock_answer, expected_result):
    question_number = 0
    monkeypatch.setattr("builtins.input", lambda: mock_answer)
    assert cardset_with_subject._Flashcard__check_answer(question_number) == expected_result


def test_compute_score_case_correct_answer(cardset):
    response = "correct"
    cardset._Flashcard__compute_score(response)
    assert cardset._Flashcard__correct_answers == 1


def test_compute_score_case_incorrect_answer(cardset):
    response = "incorrect"
    cardset._Flashcard__compute_score(response)
    assert cardset._Flashcard__incorrect_answers == 1


def test_display_score(cardset, capsys):
    cardset._Flashcard__correct_answers = 1
    cardset._Flashcard__incorrect_answers = 1
    cardset._Flashcard__display_score()
    stdout, stderr = capsys.readouterr()
    assert stdout == "\n--- Results ---\nCorrect answers: 1\nIncorrect answers: 1\nAccuracy rate: 50.00%\n"


@pytest.mark.parametrize("mock_answer, expected_result",
                         [('y', False), ('n', True)])
def test_ask_to_continue(cardset, monkeypatch, mock_answer, expected_result):
    monkeypatch.setattr("builtins.input", lambda: mock_answer)
    cardset._Flashcard__ask_to_continue()
    assert cardset._Flashcard__quit_session == expected_result
