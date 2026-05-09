from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "未授权"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class NotFoundException(AppException):
    def __init__(self, detail: str = "资源不存在"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class BadRequestException(AppException):
    def __init__(self, detail: str = "请求参数错误"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)
