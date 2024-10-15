from tgdeal.client import ApiClient
import asyncio

from tgdeal.lib.helpers import find_and_convert_session_files

API_KEY = "kh8Kpp1vwEzu6Mi6zaBH2vbIYfK1Fv"

tgdeal_api = ApiClient()
tgdeal_api.initialize()


async def main():
    sessions = await find_and_convert_session_files("sessions")
    print(sessions)
    # res = await tgdeal_api.endpoints.users.get_profile(
    #     query_user_api_key=API_KEY
    # )  # tgdeal_api.endpoints.users.ProfileRead
    #
    # print(res)


asyncio.run(main())
