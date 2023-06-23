# by Richi Rod AKA @richionline / falken20
# ./my_chispas/main.py

from renault.renault import RenaultVehicleClient
from renault_api.renault_client import RenaultClient
import aiohttp
import asyncio

from .logger import Log
from . import settings


Log.info(f"Some values from .env: {settings.ENV_PRO}")


async def main():
    async with aiohttp.ClientSession() as websession:
        client = RenaultClient(websession=websession, locale="es_ES")
        Log.info("Login in Renault")
        await client.session.login(settings.RENAULT_USER, settings.RENAULT_PASSWORD)

        # List available accounts, make a note of kamereon account id
        Log.info("Getting accounts")
        person = await client.get_person()
        Log.debug(f"Accounts: {person.accounts}")

        Log.info("Getting account data")
        account_id = 'feff2743-65f5-4092-9927-d99da84f6b67' # TODO
        account_id = 'c7d670b2-2a7a-46e6-bc0d-c6ecb60f2d8f' # TODO
        account = await client.get_api_account(account_id)

        # List available vehicles, make a note of vehicle VIN
        Log.debug(f"Vehicles: {await account.get_vehicles()}")

        vin = settings.RENAULT_VIN
        try:
            vehicle = await account.get_api_vehicle(vin)
            Log.debug(f"Object Vehicle: {format(vehicle)}")
            Log.debug(f"Cockpit information: {await vehicle.get_cockpit()}")
            Log.info(f"Battery status information: {await vehicle.get_battery_status()}")
        except Exception as err:
            Log.error(f"Error in get info vehicle:\n {err}", err=err)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
