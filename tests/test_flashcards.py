import pytest
from flashcards import Flashcard


@pytest.fixture()
def flashcard():
    return Flashcard()


def test_start(flashcard, mocker):
    mock_display_intro = mocker.patch.object(flashcard, '_display_intro')
    mock_display_subjects = mocker.patch.object(flashcard, '_display_subjects')
    mock_choose_subject = mocker.patch.object(flashcard, '_choose_subject')
    mock_parse_address = mocker.patch.object(flashcard, '_parse_address')
    mock_build_qa_session = mocker.patch.object(flashcard, '_build_qa_session')
    mock_display_subject_title = mocker.patch.object(flashcard, '_display_subject_title')
    mock_ask_questions = mocker.patch.object(flashcard, '_ask_questions')
    mock_print_results = mocker.patch.object(flashcard._scorecard, 'print_results')
    mock_ask_to_continue = mocker.patch.object(flashcard, '_ask_to_continue',
                                               side_effect=lambda: setattr(flashcard, '_active_session', False))
    flashcard.start()
    assert mock_display_intro.call_count == 1
    assert mock_display_subjects.call_count == 1
    assert mock_choose_subject.call_count == 1
    assert mock_parse_address.call_count == 1
    assert mock_build_qa_session.call_count == 1
    assert mock_display_subject_title.call_count == 1
    assert mock_ask_questions.call_count == 1
    mock_print_results.assert_called_once_with(flashcard._chosen_subject)
    assert mock_ask_to_continue.call_count == 1


def test_display_intro(flashcard):
    flashcard._display_intro()
    assert flashcard._intro_displayed


def test_display_subjects(flashcard, capsys):
    flashcard._subjects = ["Test Subject", "Random Questions"]
    flashcard._display_subjects()
    stdout, stderr = capsys.readouterr()
    assert stdout == ("Choose your subject:\n"
                      " 1. Test Subject\n"
                      " 2. Random Questions\n"
                      "On any question, input 'q' to quit.\n")


def test_choose_subject_with_valid_subject(flashcard, mocker):
    mock_chosen_subject = 1
    mock_input = mocker.patch("builtins.input", side_effect=[mock_chosen_subject])
    mock_check_valid_subject = \
        mocker.patch.object(flashcard, '_check_valid_subject',
                            side_effect=lambda _: setattr(flashcard, '_chosen_subject', mock_chosen_subject))
    mock_check_quit_session = mocker.patch.object(flashcard, '_check_quit_session')
    flashcard._choose_subject()
    assert mock_input.call_count == 1
    assert mock_check_valid_subject.call_count == 1
    assert mock_check_quit_session.call_count == 0


def test_choose_subject_with_quit(flashcard, mocker):
    mock_chosen_subject = 'q'
    mock_input = mocker.patch("builtins.input", side_effect=[mock_chosen_subject])
    mock_check_valid_subject = mocker.patch.object(flashcard, '_check_valid_subject', side_effect=ValueError)
    mock_check_quit_session = \
        mocker.patch.object(flashcard, '_check_quit_session',
                            side_effect=lambda _: setattr(flashcard, '_active_session', False))
    flashcard._choose_subject()
    assert mock_input.call_count == 1
    assert mock_check_valid_subject.call_count == 1
    assert mock_check_quit_session.call_count == 1


def test_choose_subject_with_invalid_choice(flashcard, mocker):
    mock_chosen_subject = ["invalid choice", "valid choice"]
    mock_input = mocker.patch("builtins.input", side_effect=mock_chosen_subject)
    mock_check_valid_subject = \
        mocker.patch.object(flashcard, '_check_valid_subject', side_effect=[None, ValueError])
    mock_check_quit_session = \
        mocker.patch.object(flashcard, '_check_quit_session',
                            side_effect=lambda _: setattr(flashcard, '_active_session', False))
    mock_print = mocker.patch("builtins.print")
    flashcard._choose_subject()
    mock_print.assert_called_once_with("Invalid option. Please choose again.")
    assert mock_input.call_count == 2
    assert mock_check_valid_subject.call_count == 2
    assert mock_check_quit_session.call_count == 1


def test_check_valid_subject(flashcard):
    flashcard._subjects = ["Test Subject", "Random Questions"]
    flashcard._check_valid_subject(2)
    assert flashcard._chosen_subject == "Random Questions"


def test_check_quit_session(flashcard, mocker):
    mock_print_results = mocker.patch.object(flashcard._scorecard, 'print_results')
    flashcard._check_quit_session('q')
    mock_print_results.assert_called_once_with(flashcard._chosen_subject)
    assert not flashcard._active_session


@pytest.mark.parametrize("chosen_subject, expected_address",
                         [("Test Subject", "../subjects/test_subject"),
                          ("Random Questions", ["../subjects/test_subject"])])
def test_parse_address(flashcard, chosen_subject, expected_address):
    flashcard._subjects = ["Test Subject", "Random Questions"]
    flashcard._chosen_subject = chosen_subject
    flashcard._parse_address()
    assert flashcard._chosen_subject_address == expected_address


def test_build_qa_session_with_subject(flashcard, mocker):
    mock_subject = mocker.MagicMock()
    mock_subject.questions = ["question 1\n", "question 2\n", "question 3\n"]
    mock_subject.answers = ["answer 1\n", "answer 2\n", "answer 3\n"]
    mocker.patch("flashcards.Subject", return_value=mock_subject)
    flashcard._build_qa_session()
    assert flashcard._questions == mock_subject.questions
    assert flashcard._answers == mock_subject.answers


def test_build_qa_session_with_random_subject(flashcard, mocker):
    mock_random_subject = mocker.MagicMock()
    mock_random_subject.questions = ["question 1\n", "question 2\n", "question 3\n"]
    mock_random_subject.answers = ["answer 1\n", "answer 2\n", "answer 3\n"]
    mocker.patch("flashcards.RandomSubject", return_value=mock_random_subject)
    flashcard._chosen_subject = "Random Questions"
    flashcard._build_qa_session()
    assert flashcard._questions == mock_random_subject.questions
    assert flashcard._answers == mock_random_subject.answers


def test_display_subject_title(flashcard, capsys):
    flashcard._chosen_subject = "Test Subject"
    flashcard._display_subject_title()
    stdout, stderr = capsys.readouterr()
    assert stdout == "\n--- Test Subject: 0 questions ---\n"


@pytest.mark.parametrize("mock_response",
                         ["correct", "incorrect"])
def test_ask_questions(flashcard, mocker, mock_response):
    flashcard._chosen_subject = "Test Subject"
    flashcard._questions = ["question 1\n", "question 2\n", "question 3\n"]
    first_response = mock_response
    second_response = "quit"
    mock_print = mocker.patch("builtins.print")
    mock_check_answer = mocker.patch.object(flashcard, '_check_answer', side_effect=[first_response, second_response])
    mock_log_score = mocker.patch.object(flashcard._scorecard, 'log_score')
    flashcard._ask_questions()
    mock_print.assert_has_calls([mocker.call("Q1. question 1"), mocker.call("Q2. question 2")])
    assert mock_check_answer.call_count == 2
    mock_log_score.assert_called_once_with(first_response, flashcard._chosen_subject)
    if mock_response == "incorrect":
        assert flashcard._questions == ["question 3\n", "question 1\n"]


@pytest.mark.parametrize("mock_answer, expected_return, expected_print",
                         [("answer1", "correct", "Correct!\n"),
                          ('q', "quit", None),
                          ('a', "incorrect", "Incorrect. The correct answer is:\nanswer 1\n")])
def test_check_answer(flashcard, mocker, mock_answer, expected_return, expected_print):
    mock_input = mocker.patch("builtins.input", return_value=mock_answer)
    mock_parse_answer = mocker.patch.object(flashcard, '_parse_answer',
                                            side_effect=[mock_answer, "answer1"])
    flashcard._answers = ["answer 1\n", "answer 2\n", "answer 3\n"]
    mock_print = mocker.patch("builtins.print")
    assert flashcard._check_answer() == expected_return
    assert mock_input.call_count == 1
    assert mock_parse_answer.call_count == 2
    if expected_print is not None:
        mock_print.assert_called_once_with(expected_print)
    if expected_return == "incorrect":
        assert flashcard._answers == ["answer 2\n", "answer 3\n", "answer 1\n"]


def test_parse_answer(flashcard):
    answer = "a, 'b', c"
    parsed_answer = flashcard._parse_answer(answer)
    assert parsed_answer == "a,\"b\",c"


@pytest.mark.parametrize("mock_input, expected_chosen_subject, expected_active_session",
                         [('y', None, True), ('n', "Test Subject", False)])
def test_ask_to_continue(flashcard, monkeypatch, mock_input, expected_chosen_subject, expected_active_session):
    monkeypatch.setattr("builtins.input", lambda: mock_input)
    flashcard._chosen_subject = "Test Subject"
    flashcard._ask_to_continue()
    assert flashcard._chosen_subject == expected_chosen_subject
    assert flashcard._active_session == expected_active_session
