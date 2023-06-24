# by Richi Rod AKA @richionline / falken20
# ./my_chispas/main.py

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
        for i in person.accounts:
            Log.debug(f"Account ID: {i.accountId} - Status: {i.accountStatus}")

        Log.info("Getting account vehicles")
        account_id = 'feff2743-65f5-4092-9927-d99da84f6b67' # TODO
        account_id = 'c7d670b2-2a7a-46e6-bc0d-c6ecb60f2d8f' # TODO
        account_data = await client.get_api_account(account_id)

        # List available vehicles, make a note of vehicle VIN
        vehicles = await account_data.get_vehicles()
        Log.debug(type(vehicles))
        Log.debug(type(vehicles.vehicleLinks))
        for i in vehicles.vehicleLinks:
            #Log.debug(i.raw_data)
            Log.debug(f"Model: {i.raw_data['brand']} {i.raw_data['vehicleDetails']['modelSCR']}")
            Log.debug(f"Mileage: {i.raw_data['mileage']}{i.raw_data['mileageUnit']} ({i.raw_data['mileageDate']})")
            Log.debug(f"Delivery date: {i.raw_data['vehicleDetails']['deliveryDate']}")
            Log.debug(f"Buy date: {i.raw_data['ownershipStartDate']}")
            Log.debug(f"Battery: {i.raw_data['vehicleDetails']['battery']}")
            Log.debug(f"Radio: {i.raw_data['vehicleDetails']['radioType']}")
            Log.debug(f"Years of maintenance: {i.raw_data['vehicleDetails']['yearsOfMaintenance']}")
            Log.debug(f"Connectivity: {i.raw_data['vehicleDetails']['connectivityTechnology']}")
    
        vin = settings.RENAULT_VIN
        try:
            vehicle = await account_data.get_api_vehicle(vin)

            Log.debug(await vehicle.get_location())
            Log.debug(f"Battery status: {vehicle.get_battery_status()}")
            #Log.debug(f"Cockpit information: {await vehicle.get_cockpit()}")
            #Log.info(f"Battery status information: {await vehicle.get_battery_status()}")
        except Exception as err:
            Log.error(f"Error in get info vehicle:\n {err}", err=err)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
