import asyncio
import logging
from concurrent import futures

import grpc
from fastapi import HTTPException
from tortoise import run_async

import protobuf.get_user_info_pb2 as pb2
import protobuf.get_user_info_pb2_grpc as pb2_grpc
from src.config.db_connect import init
from src.schemas.auth_schema import TokenIn
from src.services.auth_services import AuthJWTServices
from src.services.user_services import UserServices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnaryServicer(pb2_grpc.UnaryServicer):
    """Сервер для получения access и refresh токенов"""

    async def GetServerResponse(self, request, context):
        # Получаем строку из входного запроса
        message = request.message
        data = TokenIn.parse_raw(message)

        try:
            user = await UserServices.valid_user(data)
            token = await AuthJWTServices.gen_access_refresh_tokens(user)

            message_response = pb2.MessageResponse(access_token=token.access_token, refresh_token=token.refresh_token)
            return message_response
        except HTTPException as e:
            # Если возникает HTTPException, отправляем статус ошибки клиенту
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)  # Устанавливаем статус ошибки
            context.set_details(str(e))  # Устанавливаем детали ошибки


async def serve():
    """Асинхронная функция запуска gRPC сервера"""
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UnaryServicer_to_server(UnaryServicer(), server)
    server.add_insecure_port('localhost:50051')
    await server.start()
    logger.info('gRPC сервер запущен...\n')
    await server.wait_for_termination()


if __name__ == '__main__':
    run_async(init())
    asyncio.run(serve())
