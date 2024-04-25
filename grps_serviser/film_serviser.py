import protobuf.get_role_user.get_role_pb2 as get__role__pb2
import protobuf.get_role_user.get_role_pb2_grpc as get__role__pb2_grpc
from src.services.auth_services import AuthJWTServices


class GetUserRoleServicer(get__role__pb2_grpc.GetRoleServicer):
    async def GetServerResponse(self, request, context):
        token = request.access_token
        token_data = AuthJWTServices.decode_jwt(token)
        current_user = await AuthJWTServices.get_current_user(token_data)
        return get__role__pb2.MessageResponse(role=current_user.role)
