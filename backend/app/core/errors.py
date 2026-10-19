from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ApplicationError(Exception):
    def __init__(self, *, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


def error_response(
    *, status_code: int, code: str, message: str, details: object | None = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "details": details}},
    )


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationError)
    async def application_error_handler(
        _request: Request, exception: ApplicationError
    ) -> JSONResponse:
        return error_response(
            status_code=exception.status_code,
            code=exception.code,
            message=exception.message,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request, exception: RequestValidationError
    ) -> JSONResponse:
        return error_response(
            status_code=422,
            code="validation_error",
            message="The request did not pass validation.",
            details=jsonable_encoder(exception.errors()),
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(_request: Request, _exception: Exception) -> JSONResponse:
        return error_response(
            status_code=500,
            code="internal_error",
            message="An unexpected error occurred.",
        )
