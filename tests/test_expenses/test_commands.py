import pytest

from expenses.models import Expense
from expenses.commands import CreateArticleCommand, AlreadyExists


def test_create_expense():
    """
    GIVEN CreateExpenseCommand with a valid properties title, amount, created_at and content
    WHEN the execute method is called
    THEN a new Article must exist in the database with the same attributes
    """
    cmd = CreateExpenseCommand(
        author='john@doe.com',
        title='New Article',
        content='Super awesome article'
    )

    expense = cmd.execute()

    db_article = Expense.get_by_id(expense.id)

    assert db_article.id == expense.id
    assert db_article.title == expense.title
    assert db_article.amount == expense.amount
    assert db_article.created_at == expense.created_at
    assert db_article.tags == expense.tags



def test_create_article_already_exists():
    """
    GIVEN CreateArticleCommand with a title of some article in database
    WHEN the execute method is called
    THEN the AlreadyExists exception must be raised
    """

    Article(
        author='jane@doe.com',
        title='New Article',
        content='Super extra awesome article'
    ).save()

    cmd = CreateArticleCommand(
        author='john@doe.com',
        title='New Article',
        content='Super awesome article'
    )

    with pytest.raises(AlreadyExists):
        cmd.execute()