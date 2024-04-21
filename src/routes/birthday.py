from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import birthday as repositories_contacts
from src.schemas.birthday import BirthdayResponse
from src.services.auth import auth_service
from src.entity.models import User


router = APIRouter(prefix = '/birthday', tags = ['birthdays'])


@router.get("/", response_model=list[BirthdayResponse])
async def get_contact_with_upcoming_birthday(
    upcoming_days: int = Query(default=7, ge=1, le=365),
    limit: int = Query(10, ge=10, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    The get_contact_with_upcoming_birthday function returns a list of contacts with upcoming birthdays.

    :param upcoming_days: int: Specify the number of days in advance to look for upcoming birthdays
    :param ge: Specify the minimum value of the parameter
    :param le: Set a maximum value for the parameter
    :param limit: int: Limit the number of results returned
    :param ge: Indicate that the value of the parameter must be greater than or equal to a given number
    :param le: Limit the number of days in advance to search for upcoming birthdays
    :param offset: int: Skip the first offset number of contacts
    :param ge: Specify the minimum value of the parameter
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the current user from the auth_service
    :return: A list of contacts with upcoming birthdays
    :doc-author: Naboka Artem
    """
    contacts = await repositories_contacts.get_contact_with_upcoming_birthday(
        upcoming_days, limit, offset, db, current_user
    )
    return contacts
