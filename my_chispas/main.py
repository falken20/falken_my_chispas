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
        await client.session.login(settings.RENAULT_USER, settings.RENAULT_PASSWORD)
        print(f"Accounts: {await client.get_person()}") # List available accounts, make a note of kamereon account id

        account_id = 'feff2743-65f5-4092-9927-d99da84f6b67'
        account = await client.get_api_account(account_id)
        print(f"Vehicles: {await account.get_vehicles()}") # List available vehicles, make a note of vehicle VIN


        vin = "VF1AG000764785472"
        try:
            vehicle = await account.get_api_vehicle(vin)
            print(f"Cockpit information: {await vehicle.get_cockpit()}")
            print(f"Battery status information: {await vehicle.get_battery_status()}")
        except Exception as err:
            print(f"ERROR:\n {err}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())