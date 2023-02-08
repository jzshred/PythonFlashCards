import pytest
from flashcards import Flashcard
from random import randrange


def test_randrange():
    """Test imported function randrange from random module."""
    assert randrange(1) == 0


@pytest.fixture()
def cardset():
    """Return a Flashcard object."""
    return Flashcard()


@pytest.fixture()
def cardset_with_subject_qa_session(cardset):
    """Return a Flashcard object with built answers."""
    cardset._Flashcard__chosen_subject = 0
    cardset._Flashcard__build_qa_session()
    return cardset


def test_choose_subject(cardset, monkeypatch):
    """Test a valid input for the Q&A subject."""
    chosen_subject = 1
    monkeypatch.setattr("builtins.input", lambda: chosen_subject)
    cardset._Flashcard__choose_subject()
    assert cardset._Flashcard__chosen_subject == 0


def test_display_subject_title(cardset, capsys):
    """Test that the correct subject title is displayed."""
    cardset._Flashcard__chosen_subject = 0
    cardset._Flashcard__display_subject_title()
    stdout, stderr = capsys.readouterr()
    assert stdout == "\n--- Built-in functions ---\n"


def test_subject_qa_length(cardset):
    """Test that each subject's questions and answers match in length."""
    for i in range(len(cardset._Flashcard__subjects) - 1):
        cardset._Flashcard__chosen_subject = i
        cardset._Flashcard__build_subject_questions()
        cardset._Flashcard__build_subject_answers()
        assert len(cardset._Flashcard__subject_questions) == \
               len(cardset._Flashcard__subject_answers)


def test_choose_random_subject(cardset):
    """Test that the chosen random subject is within the range of available subjects."""
    cardset._Flashcard__choose_random_subject()
    assert cardset._Flashcard__chosen_subject in range(cardset._Flashcard__random_subject)


def test_choose_random_question_number(cardset_with_subject_qa_session):
    """Test that the chosen question number is within the range of available questions."""
    cardset_with_subject_qa_session._Flashcard__choose_random_question_number()
    assert cardset_with_subject_qa_session._Flashcard__random_question_number \
        in range(len(cardset_with_subject_qa_session._Flashcard__subject_questions))


def test_build_random_qa_session_questions(cardset):
    """Test that the random Q&A session gets created with the correct number of questions."""
    cardset._Flashcard__build_random_qa_session()
    assert len(cardset._Flashcard__subject_questions) == cardset._Flashcard__total_random_questions


def test_build_random_qa_session_answers(cardset):
    """Test that the random Q&A session gets created with the correct number of answers."""
    cardset._Flashcard__build_random_qa_session()
    assert len(cardset._Flashcard__subject_answers) == cardset._Flashcard__total_random_questions


@pytest.mark.parametrize("mock_answer, expected_result",
                         [("type(num)", "correct"), ('q', "quit"), ('a', "incorrect")])
def test_check_answer(cardset_with_subject_qa_session, monkeypatch, mock_answer, expected_result):
    monkeypatch.setattr("builtins.input", lambda: mock_answer)
    assert cardset_with_subject_qa_session._Flashcard__check_answer(0) == expected_result


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
