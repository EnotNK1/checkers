from schemas.users import Creds, Reg
from database.database import database_service
from services.auth import send_email
from services.auth import generate_token, verify_token
import uuid
from starlette.responses import JSONResponse, Response
from smtplib import SMTPRecipientsRefused
from psycopg2 import Error


class UserServise:

    def get_users(self, access_token) -> list or str:
        if not access_token:
            return "not token"
        token_data = verify_token(access_token)

        if token_data == 'Token has expired':
            return "Token has expired"
        elif token_data == 'Invalid token':
            return "Invalid token"

        role = database_service.check_role(uuid.UUID(token_data['user_id']))

        if role == 0:
            items = database_service.get_all_users()
            return items
        else:
            return "access denied"

    def authorization(self, payload: Creds, response: Response):

        if database_service.check_user(payload.email, payload.password) == 0:
            user_id = database_service.get_id_user(payload.email)

            token = generate_token(user_id)
            response.set_cookie(key="access_token", value=token, httponly=True)
            return token
        else:
            return "error"

    def register(self, payload: Reg) -> str:

        if payload.password == payload.confirm_password:
            if database_service.register_user(uuid.uuid4(), payload.username, payload.email, payload.password) == 0:
                return "Successfully"
            else:
                return "A user with this email address has already been registered"
        else:
            return "Password mismatch"


user_service: UserServise = UserServise()
