# by Richi Rod AKA @richionline / falken20
# ./my_chispas/main.py

from renault_api.renault_client import RenaultClient
import aiohttp
import asyncio
import datetime

from .logger import Log
from . import settings


Log.info(f"Some values from .env: {settings.ENV_PRO}")


async def main():
    async with aiohttp.ClientSession() as websession:
        client = RenaultClient(websession=websession, locale="es_ES")
        Log.info("1. Login in Renault")
        await client.session.login(settings.RENAULT_USER, settings.RENAULT_PASSWORD)

        # List available accounts, make a note of kamereon account id
        Log.info("2. Getting accounts")
        person = await client.get_person()
        account_id = ""  # account_id = 'c7d670b2-2a7a-46e6-bc0d-c6ecb60f2d8f'
        for i in person.accounts:
            Log.info(
                f"Account ID: {i.accountId} - Status: {i.accountStatus} - Account Type: {i.accountType}")
            if i.accountType == "MYRENAULT":
                account_id = i.accountId

        Log.info(f"3. Getting vehicles for account id {account_id} with account type MYRENAULT")
        account_data = await client.get_api_account(account_id)

        # List available vehicles, make a note of vehicle VIN
        vehicles = await account_data.get_vehicles()
        for i in vehicles.vehicleLinks:
            # Log.debug(i.raw_data)
            Log.info(
                f"Model: {i.raw_data['brand']} {i.raw_data['vehicleDetails']['modelSCR']}")
            Log.info(f"VIN: {i.raw_data['vehicleDetails']['vin']}")
            Log.info(
                f"Mileage: {i.raw_data['mileage']}{i.raw_data['mileageUnit']} ({i.raw_data['mileageDate']})")
            Log.info(
                f"Delivery date: {i.raw_data['vehicleDetails']['deliveryDate']}")
            Log.info(f"Buy date: {i.raw_data['ownershipStartDate']}")
            Log.info(f"Battery: {i.raw_data['vehicleDetails']['battery']}")
            Log.info(f"Radio: {i.raw_data['vehicleDetails']['radioType']}")
            Log.info(
                f"Years of maintenance: {i.raw_data['vehicleDetails']['yearsOfMaintenance']}")
            Log.info(
                f"Connectivity: {i.raw_data['vehicleDetails']['connectivityTechnology']}")

            vin = i.raw_data['vehicleDetails']['vin'] if i.raw_data['vehicleDetails']['vin'] else settings.RENAULT_VIN

            Log.info(f"4. Getting vehicle data for VIN {vin}")
            try:
                vehicle = await account_data.get_api_vehicle(vin)
                Log.debug(await vehicle.get_notification_settings())
                # Log.debug(f"Cockpit information: {await vehicle.get_cockpit()}")
                # Log.info(f"Battery status information: {await vehicle.get_battery_status()}")
            except Exception as err:
                Log.error(f"Error in get info vehicle:\n {err}", err=err)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
