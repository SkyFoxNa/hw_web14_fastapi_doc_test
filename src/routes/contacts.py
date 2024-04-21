from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactSchema, ContactUpdateSchema, ContactResponse
from src.services.auth import auth_service
from src.entity.models import User, Role
from src.services.roles import RoleAccess

router = APIRouter(prefix = '/contracts', tags = ['contracts'])

access_to_route_all = RoleAccess([Role.admin, Role.moderator])


@router.get("/", response_model = list[ContactResponse])
async def get_contracts(limit: int = Query(10, ge = 10, le = 200), offset: int = Query(0, ge = 0),
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)) :
    """
    The get_contracts function returns a list of contacts.

    :param limit: int: Limit the number of contracts that are returned
    :param ge: Specify that the limit must be greater than or equal to 10
    :param le: Limit the number of results to 200
    :param offset: int: Specify the number of items to skip before starting to collect the result set
    :param ge: Specify a minimum value for the limit parameter
    :param db: AsyncSession: Get the database session
    :param current_user: User: Get the user that is currently logged in
    :return: A list of contacts
    :doc-author: Naboka Artem
    """
    contacts = await repositories_contacts.get_contacts(limit, offset, db, current_user)
    return contacts


@router.get("/all", response_model = list[ContactResponse], dependencies = [Depends(access_to_route_all)])
async def get_all_contracts(limit: int = Query(10, ge = 10, le = 200), offset: int = Query(0, ge = 0),
                            db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)) :
    """
    The get_all_contracts function returns a list of all contacts in the database.

    :param limit: int: Limit the number of contacts returned
    :param ge: Specify the minimum value of the limit parameter
    :param le: Limit the number of contacts returned to 200
    :param offset: int: Skip the first offset number of rows
    :param ge: Specify a minimum value for the limit parameter
    :param db: AsyncSession: Pass the database connection to the function
    :param current_user: User: Get the user id of the current logged in user
    :return: A list of dictionaries
    :doc-author: Naboka Artem
    """
    contacts = await repositories_contacts.get_all_contacts(limit, offset, db, current_user)
    return contacts


@router.get("/{contact_id}", response_model = ContactResponse)
async def get_contact(contact_id: int = Path(ge = 1), db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)) :
    """
    The get_contact function returns a contact by its id.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param db: AsyncSession: Pass the database connection to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Naboka Artem
    """
    contact = await repositories_contacts.get_contact(contact_id, db, current_user)
    if contact is None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "NOT FOUND")
    return contact


@router.post("/", response_model = ContactResponse, status_code = status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)) :
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: A contactschema object
    :doc-author: Naboka Artem
    """
    contact = await repositories_contacts.create_contact(body, db, current_user)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge = 1),
                         db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)) :
    """
    The update_contact function updates a contact in the database.
        The function takes an id of the contact to be updated, and a body containing all fields that need to be updated.
        If no fields are provided, then nothing is changed in the database.

    :param body: ContactUpdateSchema: Validate the body of the request
    :param contact_id: int: Get the contact id from the url
    :param db: AsyncSession: Pass the database session to the repository
    :param current_user: User: Get the user from the database
    :return: The updated contact
    :doc-author: Naboka Artem
    """
    contact = await repositories_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge = 1), db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)) :
    """
    The delete_contact function deletes a contact from the database.
        The function takes in an integer representing the id of the contact to be deleted,
        and returns a dictionary containing information about that contact.

    :param contact_id: int: Specify the contact id of the contact to be deleted
    :param db: AsyncSession: Pass the database connection to the function
    :param current_user: User: Get the user from the database
    :return: A contact object
    :doc-author: Naboka Artem
    """
    contact = await repositories_contacts.delete_contact(contact_id, db, current_user)
    return contact


@router.delete("/all/{contact_id}", status_code = status.HTTP_204_NO_CONTENT,
               dependencies = [Depends(access_to_route_all)])
async def delete_all_contact(contact_id: int = Path(ge = 1), db: AsyncSession = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)) :
    """
    The delete_all_contact function deletes all contacts from the database.
        Parameters:
            contact_id (int): The id of the contact to delete.
            db (AsyncSession): A database connection object. Defaults to Depends(get_db).
            current_user (User): The user currently logged in, as determined by auth_service's get_current_user function. Defaults to Depends(auth-service's get-current-user).

    :param contact_id: int: Specify the contact id of the contact to be deleted
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Naboka Artem
    """
    contact = await repositories_contacts.delete_all_contact(contact_id, db, current_user)
    return contact
