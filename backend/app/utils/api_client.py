import asyncio

import httpx
from aiolimiter import AsyncLimiter


class ApiClient:
    def __init__(
        self,
        max_rate,
        time_period,
        *,
        max_retries=3,
        backoff_factor=0.5,
        retry_statuses=(429, 500, 502, 503, 504),
        timeout=10.0,
    ):
        self.rate_limiter = AsyncLimiter(max_rate, time_period)
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.retry_statuses = retry_statuses

        self.client = httpx.AsyncClient(
            timeout=timeout,
            event_hooks={"request": [self.rate_limiting_event_hook]},
        )

    async def rate_limiting_event_hook(self, request):
        # Pause before sending if rate limit is hit
        async with self.rate_limiter:
            pass

    async def get(self, url, headers=None):
        last_exc = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = await self.client.get(url, headers=headers)

                # Retry on specific HTTP status codes
                if response.status_code in self.retry_statuses:
                    raise httpx.HTTPStatusError(
                        f"Retryable status code: {response.status_code}",
                        request=response.request,
                        response=response,
                    )

                return response

            except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                last_exc = exc

                if attempt >= self.max_retries:
                    break

                # Exponential backoff
                sleep_time = self.backoff_factor * (2 ** (attempt - 1))
                await asyncio.sleep(sleep_time)

        # All retries failed
        print(f"Request failed after {self.max_retries} attempts: {last_exc}")
        return httpx.Response(status_code=500)

    async def close(self):
        await self.client.aclose()
