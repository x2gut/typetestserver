from typing import List, Dict

from src.domain.result.dto.result import Result as ResultDTO, ResultStatisticsOutput, \
    BestResult as BestResultDTO, StatisticTime, StatisticWords
from src.domain.result.use_cases.result import ResultUseCase


class AddResult(ResultUseCase):
    async def __call__(self, result: ResultDTO):
        return await self.repository.save_result(result)


class AllResults(ResultUseCase):
    async def __call__(self) -> List[ResultDTO]:
        return await self.repository.get_all_result()


class BestResults(ResultUseCase):
    async def __call__(self, limit: int, time: int, mode: str, words: int) -> List[BestResultDTO]:
        best_results = await self.repository.get_best_results(limit=limit, time=time, mode=mode, words=words)

        return [
            BestResultDTO(
                username=row.username,
                user_id=row.user_id,
                wpm=row.wpm,
                accuracy=row.accuracy,
                time=row.time,
                words=row.words,
                created_at=row.created_at,
            )
            for row in best_results
        ]


class ResultById(ResultUseCase):
    async def __call__(self, user_id: int) -> ResultDTO:
        return await self.repository.get_by_id(id_=user_id)


class AverageResultStatistic(ResultUseCase):
    @staticmethod
    def _average(values: List[int]) -> float:
        return sum(values) / len(values) if values else 0

    @staticmethod
    def _best(values: List[int]) -> int:
        return values[-1] if values else 0

    async def get_sorted_wpm(self, results: List, mode: str, value: int) -> List[int]:
        return sorted(
            result.wpm for result in results
            if result.mode == mode and (
                result.time == value if mode == "time" else result.words == value
            )
        )

    async def __call__(self, user_id: int) -> ResultStatisticsOutput:
        results = await self.repository.get_all_results_by_user_id(user_id, limit=500)

        time_results_15 = await self.get_sorted_wpm(results, "time", 15)
        time_results_30 = await self.get_sorted_wpm(results, "time", 30)
        time_results_60 = await self.get_sorted_wpm(results, "time", 60)

        words_results_25 = await self.get_sorted_wpm(results, "words", 25)
        words_results_50 = await self.get_sorted_wpm(results, "words", 50)
        words_results_100 = await self.get_sorted_wpm(results, "words", 100)

        return ResultStatisticsOutput(
            time=StatisticTime(
                time_avg_15=self._average(time_results_15),
                time_avg_30=self._average(time_results_30),
                time_avg_60=self._average(time_results_60),

                time_best_15=self._best(time_results_15),
                time_best_30=self._best(time_results_30),
                time_best_60=self._best(time_results_60),
            ),
            words=StatisticWords(
                words_avg_25=self._average(words_results_25),
                words_avg_50=self._average(words_results_50),
                words_avg_100=self._average(words_results_100),

                words_best_25=self._best(words_results_25),
                words_best_50=self._best(words_results_50),
                words_best_100=self._best(words_results_100),
            )
        )


class ResultHistory(ResultUseCase):
    async def __call__(self, user_id: int, limit: int) -> List[ResultDTO]:
        return await self.repository.get_all_results_by_user_id(user_id, limit=limit)


class ResultService:
    def __init__(self, result_repository):
        self.repository = result_repository

    async def save_result(self, result: ResultDTO):
        return await AddResult(self.repository)(result)

    async def get_all_results(self) -> List[ResultDTO]:
        return await AllResults(self.repository)()

    async def get_result_by_user_id(self, user_id) -> ResultDTO:
        return await ResultById(self.repository)(user_id)

    async def get_average_result_statistics(self, user_id) -> Dict[str, Dict[str, int]]:
        return await AverageResultStatistic(self.repository)(user_id)

    async def get_best_results(self, limit: int, time: int, mode: str, words: int) -> List[ResultDTO]:
        return await BestResults(self.repository)(limit, time, mode, words)

    async def get_user_result_history(self, user_id, limit):
        return await ResultHistory(self.repository)(user_id, limit)
