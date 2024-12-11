from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError

from src.application.use_cases.result import ResultService
from src.domain.result.dto.result import Result as ResultDTO, BestResult as BestResultDTO, ResultStatisticsOutput
from src.infrastructure.dependencies import get_result_service
from src.infrastructure.security.jwt_service import decode_jwt
from src.presentation.api.result.requests import SaveResult
from src.presentation.api.result.responses import HistoryResponse

result_router = APIRouter(prefix="/results", tags=["results"])

http_bearer = HTTPBearer()


async def validate_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        payload = await decode_jwt(credentials.credentials)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    if not payload.get("id"):
        raise HTTPException(status_code=401, detail="Invalid payload")
    return int(payload.get("id"))


@result_router.get("/leaderboard")
async def get_best_average_result(limit: int = 50,
                                  time: int = 60,
                                  mode: str = "time",
                                  words: int = 25,
                                  result_service: ResultService = Depends(get_result_service)) -> List[BestResultDTO]:
    best_results = await result_service.get_best_results(limit, time, mode, words)
    return best_results


@result_router.get("/{id}")
async def get_results_by_id(user_id: int, result_service: ResultService = Depends(get_result_service)):
    return await result_service.get_result_by_user_id(user_id)


@result_router.get("/stats/{user_id}")
async def get_user_stats(user_id: int,
                         result_service: ResultService = Depends(get_result_service)) -> ResultStatisticsOutput:
    return await result_service.get_average_result_statistics(user_id)


@result_router.get("/history/{user_id}")
async def get_user_history(user_id: int,
                           limit: int = 10,
                           result_service: ResultService = Depends(get_result_service)) -> HistoryResponse:
    history = await result_service.get_user_result_history(user_id, limit)
    return HistoryResponse(total_items=len(history), history=history)


@result_router.post("/")
async def save_result(new_result: SaveResult,
                      response: Response,
                      user_id=Depends(validate_user),
                      result_service: ResultService = Depends(get_result_service)) -> ResultDTO:
    if user_id != new_result.user_id:
        raise HTTPException(status_code=400, detail="Not authorized")
    response.status_code = status.HTTP_201_CREATED
    return await result_service.save_result(new_result)
