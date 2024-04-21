from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, current_user: User):
    """
    The get_contacts function returns a list of contacts for the current user.
        ---
        get:
            description: Get all contacts for the current user.
            responses: # The possible responses that can be returned by this endpoint. Each response is defined
            in detail below its name, and contains an example of what that response would look like if it were
            to be returned from this endpoint. This is helpful because you can see exactly what data will be returned
            when you make a request to this endpoint, and how you should handle each type of response in your code
            (e.g., if there are no contacts found, then return an

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip before starting to return rows
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Filter the contacts by user
    :return: A list of dictionaries
    :doc-author: Naboka Artem
    """
    data = select(Contact).filter_by(user = current_user).offset(offset).limit(limit)
    contacts = await db.execute(data)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession, current_user: User):
    """
    The get_all_contacts function returns a list of all contacts in the database.
        ---
        description: Get all contacts from the database.
        tags: [contacts]
        parameters:  # Parameters to be passed into this function, as well as their types and descriptions.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Determine how many contacts to skip over
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Naboka Artem
    """
    data = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(data)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, current_user: User):
    """
    The get_contact function is used to retrieve a single contact from the database.
    It takes in an integer representing the id of the contact, and returns a Contact object.

    :param contact_id: int: Specify the id of the contact we want to get
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Ensure that the user is only able to access their own contacts
    :return: A contact object
    :doc-author: Naboka Artem
    """
    data = select(Contact).filter_by(id = contact_id, user = current_user)
    contact = await db.execute(data)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, current_user: User) :
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the request body and convert it to a contact object
    :param db: AsyncSession: Pass in a database session
    :param current_user: User: Get the user who is making the request
    :return: The contact object
    :doc-author: Naboka Artem
    """
    contact = Contact(**body.model_dump(exclude_unset = True), user = current_user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession, current_user: User) :
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactUpdateSchema): A schema containing all fields that can be updated for a given Contact object.
                This is used to validate and deserialize the request body into an object we can use in our function logic.
                See schemas/contact_update_schema for more information on what this schema looks like and how it works!

    :param contact_id: int: Identify the contact to be updated
    :param body: ContactUpdateSchema: Specify the schema of the body that will be passed into this function
    :param db: AsyncSession: Pass a database session to the function
    :param current_user: User: Ensure that the user is only updating their own contacts
    :return: A contact object
    :doc-author: Naboka Artem
    """
    data = select(Contact).filter_by(id = contact_id, user = current_user)
    result = await db.execute(data)
    contact = result.scalar_one_or_none()
    if contact :
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.address = body.address
        contact.notes = body.notes
        contact.interests = body.interests
        contact.is_active = body.is_active
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, current_user: User) :
    """
    The delete_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be deleted.
            db (AsyncSession): An async session object for interacting with the database.
            current_user (User): The user who is making this request, used to ensure that only they can delete their own contacts.

    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: AsyncSession: Pass the database session into the function
    :param current_user: User: Ensure that the user is only deleting their own contacts
    :return: The contact that was deleted
    :doc-author: Naboka Artem
    """
    data = select(Contact).filter_by(id = contact_id, user = current_user)
    contact = await db.execute(data)
    contact = contact.scalar_one_or_none()
    if contact :
        await db.delete(contact)
        await db.commit()
    return contact


async def delete_all_contact(contact_id: int, db: AsyncSession, current_user: User) :
    """
    The delete_all_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            db (AsyncSession): A database session object.
            current_user (User): The user who is making this request, used for authorization purposes only.

    :param contact_id: int: Specify the contact that will be deleted
    :param db: AsyncSession: Pass in the database session
    :param current_user: User: Check if the user is logged in
    :return: A contact object
    :doc-author: Naboka Artem
    """
    data = select(Contact).filter_by(id = contact_id)
    contact = await db.execute(data)
    contact = contact.scalar_one_or_none()
    if contact :
        await db.delete(contact)
        await db.commit()
    return contact
