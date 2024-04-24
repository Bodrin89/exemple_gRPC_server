import asyncio
import logging
from concurrent import futures

import grpc
from tortoise import run_async

import protobuf.update_token.update_token_pb2 as pb2
import protobuf.update_token.update_token_pb2_grpc as pb2_grpc
from src.config.db_connect import init
from src.schemas.auth_schema import UpdateTokenIn
from src.services.auth_services import AuthJWTServices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidTokenServicer(pb2_grpc.ValidTokenServicer):
    async def GetServerResponse(self, request, context):
        massage = request.message
        data = UpdateTokenIn.parse_raw(massage)

        jwt_data = await AuthJWTServices.decode_jwt(data.refresh_token)

        tokens = await AuthJWTServices.gen_access_refresh_tokens(jwt_data)
        return pb2.MessageResponse(refresh_token=tokens.refresh_token, access_token=tokens.access_token)


async def serve():
    """Асинхронная функция запуска gRPC сервера"""
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ValidTokenServicer_to_server(ValidTokenServicer(), server)
    server.add_insecure_port('localhost:50052')
    await server.start()
    logger.info('gRPC_2 сервер запущен...\n')
    await server.wait_for_termination()


if __name__ == '__main__':
    run_async(init())
    asyncio.run(serve())
