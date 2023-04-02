import pytest
from subject import Subject


@pytest.fixture()
def subject():
    return Subject("subjects/test_subject")


def test_init(mocker):
    chosen_subject = "subjects/test_subject"
    mock_set_questions = mocker.patch.object(Subject, '_set_questions', autospec=True)
    mock_set_answers = mocker.patch.object(Subject, '_set_answers', autospec=True)
    subject = Subject(chosen_subject)
    assert subject.questions == []
    assert subject.answers == []
    mock_set_questions.assert_called_once_with(subject, chosen_subject)
    mock_set_answers.assert_called_once_with(subject, chosen_subject)


def test_set_questions(subject):
    assert subject.questions == ["question 1\n", "question 2\n", "question 3\n"]


def test_set_answers(subject):
    assert subject.answers == ["answer 1\n", "answer 2\n", "answer 3\n"]
