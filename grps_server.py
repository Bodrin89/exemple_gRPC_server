import asyncio
import logging
from concurrent import futures

import grpc
from tortoise import run_async

import protobuf.get_role_user.get_role_pb2_grpc as get_role_pb2_grpc
import protobuf.get_user_info_pb2_grpc as get_user_info_pb2_grpc
import protobuf.update_token.update_token_pb2_grpc as update_token_pb2_grpc
from grps_serviser.auth_grpc_servicer import UnaryServicer, ValidTokenServicer
from grps_serviser.film_serviser import GetUserRoleServicer
from src.config.db_connect import init
from src.config.settings import GRPC_HOST, GRPC_PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def serve():
    """Асинхронная функция запуска gRPC сервера"""
    # # Защищенное соединение
    # key = open('ssl/key.pem', 'rb').read()
    # cert = open('ssl/cert.pem', 'rb').read()
    # server_credentials = grpc.ssl_server_credentials([(key, cert)])
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    get_user_info_pb2_grpc.add_UnaryServicer_to_server(UnaryServicer(), server)
    update_token_pb2_grpc.add_ValidTokenServicer_to_server(ValidTokenServicer(), server)
    get_role_pb2_grpc.add_GetRoleServicer_to_server(GetUserRoleServicer(), server)

    server.add_insecure_port(f'{GRPC_HOST}:{GRPC_PORT}')

    # # Защищенное соединение
    # server.add_secure_port(f'{GRPC_HOST}:{GRPC_PORT}', server_credentials)
    await server.start()
    logger.info('\n\ngRPC сервер запущен...\n')
    await server.wait_for_termination()


if __name__ == '__main__':
    run_async(init())
    asyncio.run(serve())
