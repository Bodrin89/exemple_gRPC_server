import logging

import grpc
from fastapi import HTTPException

import protobuf.get_user_info_pb2 as get_user_info_pb2
import protobuf.get_user_info_pb2_grpc as get_user_info_pb2_grpc
import protobuf.update_token.update_token_pb2 as update_token_pb2
import protobuf.update_token.update_token_pb2_grpc as update_token_pb2_grpc
from src.schemas.auth_schema import TokenIn, UpdateTokenIn
from src.services.auth_services import AuthJWTServices
from src.services.user_services import UserServices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidTokenServicer(update_token_pb2_grpc.ValidTokenServicer):
    """Servicer для обмена refresh_token на новый access_token и refresh_token"""

    async def GetServerResponse(self, request, context):
        massage = request.message
        data = UpdateTokenIn.parse_raw(massage)

        jwt_data = await AuthJWTServices.decode_jwt(data.refresh_token)

        tokens = await AuthJWTServices.gen_access_refresh_tokens(jwt_data)
        return update_token_pb2.MessageResponse(refresh_token=tokens.refresh_token, access_token=tokens.access_token)


class UnaryServicer(get_user_info_pb2_grpc.UnaryServicer):
    """Сервер для получения access и refresh токенов"""

    async def GetServerResponse(self, request, context):
        # Получаем строку из входного запроса
        message = request.message
        data = TokenIn.parse_raw(message)

        try:
            user = await UserServices.valid_user(data)
            token = await AuthJWTServices.gen_access_refresh_tokens(user)

            message_response = get_user_info_pb2.MessageResponse(
                access_token=token.access_token, refresh_token=token.refresh_token
            )
            return message_response
        except HTTPException as e:
            # Если возникает HTTPException, отправляем статус ошибки клиенту
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)  # Устанавливаем статус ошибки
            context.set_details(str(e))  # Устанавливаем детали ошибки
