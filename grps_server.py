import asyncio
import logging
from concurrent import futures

import grpc
from tortoise import run_async

import protobuf.get_user_info_pb2_grpc as get_user_info_pb2_grpc
import protobuf.update_token.update_token_pb2_grpc as update_token_pb2_grpc
from grps_serviser.auth_grpc_servicer import UnaryServicer, ValidTokenServicer
from src.config.db_connect import init

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def serve():
    """Асинхронная функция запуска gRPC сервера"""
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    get_user_info_pb2_grpc.add_UnaryServicer_to_server(UnaryServicer(), server)
    update_token_pb2_grpc.add_ValidTokenServicer_to_server(ValidTokenServicer(), server)

    server.add_insecure_port('localhost:50051')
    await server.start()
    logger.info('gRPC сервер запущен...\n')
    await server.wait_for_termination()


if __name__ == '__main__':
    run_async(init())
    asyncio.run(serve())
