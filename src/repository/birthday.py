from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.entity.models import Contact, User


async def get_contact_with_upcoming_birthday(upcoming_days: int, limit: int, offset: int, db: AsyncSession,
                                             current_user: User, future_date=None) :
    """
    The get_contact_with_upcoming_birthday function returns a list of contacts with upcoming birthdays.
        The function takes in the following parameters:
            - upcoming_days: An integer representing the number of days from now to look for birthdays.
            - limit: An integer representing how many contacts to return at most.
            - offset: An integer representing how many contacts to skip before returning results (for pagination).

    :param upcoming_days: int: Set the number of days in the future that we want to search for birthdays
    :param limit: int: Limit the number of contacts that are returned
    :param offset: int: Skip the first n rows of the result set
    :param db: AsyncSession: Access the database
    :param current_user: User: Get the contacts of the current user
    :param future_date: Set the date to which we want to get contacts with upcoming birthdays
    :return: A list of contacts with upcoming birthdays
    :doc-author: Naboka Artem
    """
    current_date = datetime.now().date()
    future_date = current_date + timedelta(days = upcoming_days)

    data = select(Contact).filter(Contact.birthday.between(current_date, future_date)).filter_by(
        user = current_user).offset(offset).limit(limit)

    contacts = await db.execute(data)
    qqqq = contacts.scalars().all()
    return contacts.scalars().all()
