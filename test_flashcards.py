import pytest
from flashcards import Flashcard


@pytest.fixture()
def cardset():
    cardset = Flashcard()
    cardset._subjects = ["Test Subject"]
    cardset._random_subject_number = 2
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


@pytest.mark.parametrize("chosen_subject, subject_number, subject_address, quit_session",
                         [(1, 1, "subjects/test_subject", False),
                          (2, 2, ["subjects/test_subject"], False),
                          ('q', None, None, True)])
def test_choose_subject(cardset, monkeypatch, chosen_subject, subject_number, subject_address, quit_session):
    monkeypatch.setattr("builtins.input", lambda: chosen_subject)
    cardset._choose_subject()
    assert cardset._chosen_subject_number == subject_number
    assert cardset._chosen_subject_address == subject_address
    assert cardset._quit_session == quit_session


def test_check_valid_subject(cardset):
    cardset._check_valid_subject(1)
    assert cardset._chosen_subject_number == 1
    assert cardset._chosen_subject_address == "subjects/test_subject"


@pytest.mark.parametrize("subject_number, subject_address",
                         [(1, "subjects/test_subject"),
                          (2, ["subjects/test_subject"])])
def test_parse_address(cardset, subject_number, subject_address):
    cardset._chosen_subject_number = subject_number
    cardset._parse_address()
    assert cardset._chosen_subject_address == subject_address


def test_check_quit_session(cardset):
    cardset._check_quit_session('q')
    assert cardset._quit_session


def test_build_qa_session(cardset):
    cardset._chosen_subject_number = 1
    cardset._chosen_subject_address = "subjects/test_subject"
    cardset._build_qa_session()
    assert cardset._questions == ["question 1\n", "question 2\n", "question 3\n"]
    assert cardset._answers == ["answer 1\n", "answer 2\n", "answer 3\n"]


@pytest.mark.parametrize("subject_number, subject_title",
                         [(1, "Test Subject"),
                          (2, "Random Questions")])
def test_display_subject_title(cardset, capsys, subject_number, subject_title):
    cardset._chosen_subject_number = subject_number
    cardset._display_subject_title()
    stdout, stderr = capsys.readouterr()
    assert stdout == f"\n--- {subject_title}: 0 questions ---\n"


def test_ask_questions(cardset, monkeypatch, capsys):
    chosen_subject = 1
    cardset._check_valid_subject(chosen_subject)
    cardset._build_qa_session()
    monkeypatch.setattr("builtins.input", lambda: 'q')
    cardset._ask_questions()
    stdout, stderr = capsys.readouterr()
    assert stdout == f"Q1. question 1\n"
    assert cardset._quit_session


@pytest.mark.parametrize("mock_answer, expected_result",
                         [("answer 1", "correct"), ("answer1", "correct"), ('q', "quit"), ('a', "incorrect")])
def test_check_answer(cardset, monkeypatch, mock_answer, expected_result):
    chosen_subject = 1
    cardset._check_valid_subject(chosen_subject)
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
    response = answer
    cardset._compute_score(response)
    assert cardset._correct_answers == correct_answers
    assert cardset._incorrect_answers == incorrect_answers


def test_display_score(cardset, capsys):
    cardset._correct_answers = 1
    cardset._incorrect_answers = 1
    cardset._display_score()
    stdout, stderr = capsys.readouterr()
    assert stdout == "\n--- Results ---\nCorrect answers: 1\nIncorrect answers: 1\nAccuracy rate: 50.00%\n"


@pytest.mark.parametrize("mock_answer, expected_result",
                         [('y', False), ('n', True)])
def test_ask_to_continue(cardset, monkeypatch, mock_answer, expected_result):
    monkeypatch.setattr("builtins.input", lambda: mock_answer)
    cardset._ask_to_continue()
    assert cardset._quit_session == expected_result
