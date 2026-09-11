import httpx


STUDY_TIP_API_URL = "https://dummyjson.com/quotes/random"


class StudyTipServiceError(Exception):
    """Raised when the study tip service cannot provide a response."""


async def get_study_tip() -> str:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(STUDY_TIP_API_URL)

        response.raise_for_status()

        data = response.json()
        quote = data.get("quote")

        if not quote:
            raise StudyTipServiceError(
                "Study tip service returned an invalid response"
            )

        return quote

    except httpx.TimeoutException as error:
        raise StudyTipServiceError(
            "Study tip service timed out"
        ) from error

    except httpx.HTTPError as error:
        raise StudyTipServiceError(
            "Study tip service is currently unavailable"
        ) from error

    except (ValueError, TypeError) as error:
        raise StudyTipServiceError(
            "Study tip service returned invalid data"
        ) from error