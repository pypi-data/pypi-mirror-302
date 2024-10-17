from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import aiohttp

def retry_on_client_error():
    return retry(
        retry=retry_if_exception_type(aiohttp.ClientError),
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=1, max=20),
        reraise=True
    )
