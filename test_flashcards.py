import pytest
from flashcards import Flashcard


@pytest.fixture()
def cardset():
    cardset = Flashcard()
    cardset._subjects = ["Test Subject", "Random Questions"]
    cardset._chosen_subject = "Test Subject"
    cardset._chosen_subject_address = "subjects/test_subject"
    return cardset


def test_display_intro(cardset):
    cardset._display_intro()
    assert cardset._intro_displayed


def test_display_subjects(cardset, capsys):
    cardset._display_subjects()
    stdout, stderr = capsys.readouterr()
    assert stdout == ("Choose your subject:\n"
                      " 1. Test Subject\n"
                      " 2. Random Questions\n"
                      "On any question, input 'q' to quit.\n")


@pytest.mark.parametrize("mock_input, chosen_subject, quit_session",
                         [(1, "Test Subject", False),
                          (2, "Random Questions", False),
                          ('q', "Test Subject", True)])
def test_choose_subject(cardset, monkeypatch, mock_input, chosen_subject, quit_session):
    monkeypatch.setattr("builtins.input", lambda: mock_input)
    cardset._choose_subject()
    assert cardset._chosen_subject == chosen_subject
    assert cardset._quit_session == quit_session


def test_check_valid_subject(cardset):
    cardset._check_valid_subject(2)
    assert cardset._chosen_subject == "Random Questions"


def test_check_quit_session(cardset):
    cardset._check_quit_session('q')
    assert cardset._quit_session


@pytest.mark.parametrize("chosen_subject, chosen_subject_address",
                         [("Test Subject", "subjects/test_subject"),
                          ("Random Questions", ["subjects/test_subject"])])
def test_parse_address(cardset, chosen_subject, chosen_subject_address):
    cardset._chosen_subject = chosen_subject
    cardset._parse_address()
    assert cardset._chosen_subject_address == chosen_subject_address


def test_build_qa_session(cardset):
    cardset._build_qa_session()
    assert cardset._questions == ["question 1\n", "question 2\n", "question 3\n"]
    assert cardset._answers == ["answer 1\n", "answer 2\n", "answer 3\n"]


def test_display_subject_title(cardset, capsys):
    cardset._display_subject_title()
    stdout, stderr = capsys.readouterr()
    assert stdout == f"\n--- Test Subject: 0 questions ---\n"


def test_ask_questions(cardset, monkeypatch, capsys):
    cardset._build_qa_session()
    monkeypatch.setattr("builtins.input", lambda: 'q')
    cardset._ask_questions()
    stdout, stderr = capsys.readouterr()
    assert stdout == f"Q1. question 1\n"
    assert cardset._quit_session


@pytest.mark.parametrize("mock_answer, expected_result",
                         [("answer 1", "correct"), ("answer1", "correct"), ('q', "quit"), ('a', "incorrect")])
def test_check_answer(cardset, monkeypatch, mock_answer, expected_result):
    cardset._build_qa_session()
    question_number = 0
    monkeypatch.setattr("builtins.input", lambda: mock_answer)
    assert cardset._check_answer(question_number) == expected_result


def test_remove_whitespaces(cardset):
    answer = "(a, b, c)"
    answer_without_whitespaces = cardset._remove_whitespaces(answer)
    assert answer_without_whitespaces == "(a,b,c)"


@pytest.mark.parametrize("answer, correct_answers, incorrect_answers",
                         [("correct", 1, 0), ("incorrect", 0, 1)])
def test_compute_score(cardset, answer, correct_answers, incorrect_answers):
    cardset._compute_score(answer)
    assert cardset._correct_answers == correct_answers
    assert cardset._incorrect_answers == incorrect_answers


def test_display_score(cardset, capsys):
    cardset._correct_answers = 1
    cardset._incorrect_answers = 1
    cardset._display_score()
    stdout, stderr = capsys.readouterr()
    assert stdout == "\n--- Results ---\nCorrect answers: 1\nIncorrect answers: 1\nAccuracy rate: 50.00%\n"


@pytest.mark.parametrize("mock_input, expected_result",
                         [('y', False), ('n', True)])
def test_ask_to_continue(cardset, monkeypatch, mock_input, expected_result):
    monkeypatch.setattr("builtins.input", lambda: mock_input)
    cardset._ask_to_continue()
    assert cardset._quit_session == expected_result
