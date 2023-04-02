import pytest
from scorecard import Scorecard


@pytest.fixture()
def scorecard():
    return Scorecard(["Test Subject 1", "Test Subject 2", "Test Subject 3"])


def test_init(scorecard):
    assert scorecard._subjects == ["Test Subject 1", "Test Subject 2", "Test Subject 3"]
    assert scorecard._correct_answers == [0, 0, 0]
    assert scorecard._incorrect_answers == [0, 0, 0]
    assert scorecard._accuracy_rates == [0.0, 0.0, 0.0]
    assert scorecard._total_results == [0, 0, 0.0]


def test_print_current_session(scorecard, capsys):
    scorecard._print_current_session("Test Subject 1")
    stdout, stderr = capsys.readouterr()
    assert stdout == ("--- Current Session ---\n"
                      "Subject:   Test Subject 1\n"
                      "Correct:   0\n"
                      "Incorrect: 0\n"
                      "Accuracy:  0.00%\n")


def test_print_all_sessions_with_no_answers(scorecard, capsys):
    scorecard._print_all_sessions()
    stdout, stderr = capsys.readouterr()
    assert stdout == ("\n--- All Sessions ---\n"
                      "Subject       \tCor Inc Acc\n"
                      "Test Subject 1\t0   0   0.00%\n"
                      "Test Subject 2\t0   0   0.00%\n"
                      "Test Subject 3\t0   0   0.00%\n"
                      "--------------\n"
                      "Total         \t0   0   0.00%\n")


def test_print_all_sessions_with_answers(scorecard, capsys):
    scorecard._correct_answers = [1, 1, 0]
    scorecard._incorrect_answers = [0, 1, 1]
    scorecard._accuracy_rates = [1.0, 0.5, 0.0]
    scorecard._total_results = [2, 2, 0.5]
    scorecard._print_all_sessions()
    stdout, stderr = capsys.readouterr()
    assert stdout == ("\n--- All Sessions ---\n"
                      "Subject       \tCor Inc Acc\n"
                      "Test Subject 1\t1   0   100.00%\n"
                      "Test Subject 2\t1   1   50.00%\n"
                      "Test Subject 3\t0   1   0.00%\n"
                      "--------------\n"
                      "Total         \t2   2   50.00%\n")


def test_compute_accuracy(scorecard):
    scorecard._correct_answers = [1, 1, 0]
    scorecard._incorrect_answers = [0, 1, 0]
    scorecard._compute_accuracy()
    assert scorecard._accuracy_rates == [1.0, 0.5, 0.0]


@pytest.mark.parametrize("correct_answers, incorrect_answers, expected_total_results",
                         [([1, 1, 0], [0, 1, 1], [2, 2, 0.5]),
                          ([0, 0, 0], [0, 0, 0], [0, 0, 0.0])])
def test_compute_total(scorecard, correct_answers, incorrect_answers, expected_total_results):
    scorecard._correct_answers = correct_answers
    scorecard._incorrect_answers = incorrect_answers
    scorecard._compute_total()
    assert scorecard._total_results == expected_total_results


@pytest.mark.parametrize("answer, subject, expected_correct_answers, expected_incorrect_answers",
                         [("correct", "Test Subject 1", [1, 0, 0], [0, 0, 0]),
                          ("incorrect", "Test Subject 2", [0, 0, 0], [0, 1, 0])])
def test_log_score(scorecard, mocker, answer, subject, expected_correct_answers, expected_incorrect_answers):
    mock_compute_accuracy = mocker.patch.object(scorecard, '_compute_accuracy')
    mock_compute_total = mocker.patch.object(scorecard, '_compute_total')
    scorecard.log_score(answer, subject)
    assert scorecard._correct_answers == expected_correct_answers
    assert scorecard._incorrect_answers == expected_incorrect_answers
    assert mock_compute_accuracy.call_count == 1
    assert mock_compute_total.call_count == 1


@pytest.mark.parametrize("subject, expected_print_current_session_call_count",
                         [("Test Subject 1", 1),
                          (None, 0)])
def test_print_results(scorecard, mocker, subject, expected_print_current_session_call_count):
    mock_print_current_session = mocker.patch.object(scorecard, '_print_current_session')
    mock_print_all_sessions = mocker.patch.object(scorecard, '_print_all_sessions')
    scorecard.print_results(subject)
    assert mock_print_current_session.call_count == expected_print_current_session_call_count
    assert mock_print_all_sessions.call_count == 1
