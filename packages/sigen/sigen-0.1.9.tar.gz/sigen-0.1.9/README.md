## Sigen
_Unofficial package for reading and writing data to and from Sigenergy inverters via cloud APIs._

> [!IMPORTANT]  
> This repository is only sporadically maintained.  Breaking API changes will be maintained on a best efforts basis.
>
> Collaborators are welcome, as are PRs for enhancements.
>
> Bug reports unrelated to API changes may not get the attention you want. 


### Installation
```bash
pip install sigen
```

### Usage

```python
from sigen import Sigen

# username and password you use in the mySigen app.
# Region is Europe (eu) / Asia-Pacific (apac) /
# Middle East & Africa (eu) / Chinese Mainland (cn) / Unitest States (us)
sigen = Sigen(username="your_username", password="your_password", region="eu")

# Initialize the Sigen instance
await sigen.async_initialize()

# Read data
print(await sigen.fetch_station_info())
print(await sigen.get_energy_flow())
print(await sigen.get_operational_mode())

# Set modes
print(await sigen.set_operational_mode_sigen_ai_mode())
print(await sigen.set_operational_mode_maximum_self_powered())
print(await sigen.set_operational_mode_tou())
print(await sigen.set_operational_fully_fed_to_grid())

```

Full example:
```python
import logging
import os
import asyncio
from sigen import Sigen

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    # Read username and password from environment variables
    username = os.getenv('SIGEN_USERNAME')
    password = os.getenv('SIGEN_PASSWORD')

    if not username or not password:
        logging.error("Environment variables SIGEN_USERNAME and SIGEN_PASSWORD must be set")
        return

    sigen = Sigen(username=username, password=password)

    # Initialize the Sigen instance
    await sigen.async_initialize()

    # Fetch and log station info
    logger.info("Fetching station info...")
    station_info = await sigen.fetch_station_info()
    logger.info("Station Info:")
    logger.info(f"Station ID: {station_info['stationId']}")
    logger.info(f"Has PV: {station_info['hasPv']}")
    logger.info(f"Has EV: {station_info['hasEv']}")
    logger.info(f"On Grid: {station_info['onGrid']}")
    logger.info(f"PV Capacity: {station_info['pvCapacity']} kW")
    logger.info(f"Battery Capacity: {station_info['batteryCapacity']} kWh")

    # Fetch and log energy flow info
    logger.info("\nFetching energy flow info...")
    energy_flow = await sigen.get_energy_flow()
    logger.info("Energy Flow Info:")
    logger.info(f"PV Day Energy: {energy_flow['pvDayNrg']} kWh")
    logger.info(f"PV Power: {energy_flow['pvPower']} kW")
    logger.info(f"Buy/Sell Power: {energy_flow['buySellPower']} kW")
    logger.info(f"EV Power: {energy_flow['evPower']} kW")
    logger.info(f"AC Power: {energy_flow['acPower']} kW")
    logger.info(f"Load Power: {energy_flow['loadPower']} kW")
    logger.info(f"Battery Power: {energy_flow['batteryPower']} kW")
    logger.info(f"Battery SOC: {energy_flow['batterySoc']}%")

    # Fetch and log current operational mode
    logger.info("\nFetching current operational mode...")
    current_mode = await sigen.get_operational_mode()
    logger.info(f"Current Operational Mode: {current_mode}")

    # Change operational mode (example: setting mode to 'Fully Fed to Grid')
    # logger.info("\nSetting operational mode to 'Fully Fed to Grid'...")
    # response = await sigen.set_operational_mode(5)

    # Or set by label
    # response = await sigen.set_operational_mode_sigen_ai_mode()
    # response = await sigen.set_operational_mode_tou()
    # response = await sigen.set_operational_mode_fully_fed_to_grid()
    # response = await sigen.set_operational_mode_maximum_self_powered()
    # logger.info(f"Response: {response}")

    # logger.info("\nFetching current operational mode...")
    # current_mode = await sigen.get_operational_mode()
    # logger.info(f"Current Operational Mode: {current_mode}")


if __name__ == "__main__":
    asyncio.run(main())
```

Example output of the above code:
```bash

2024-06-07 06:09:29 INFO Fetching station info...
2024-06-07 06:09:29 INFO Station ID: 20241231231231
2024-06-07 06:09:29 INFO Has PV: True
2024-06-07 06:09:29 INFO Has EV: False
2024-06-07 06:09:29 INFO On Grid: True
2024-06-07 06:09:29 INFO PV Capacity: 10.3 kW
2024-06-07 06:09:29 INFO Battery Capacity: 8.06 kWh

Fetching energy flow info...
2024-06-07 06:09:29 INFO PV Day Energy: 35.25 kWh
2024-06-07 06:09:29 INFO PV Power: 5.232 kW
2024-06-07 06:09:29 INFO Buy/Sell Power: 3.8 kW
2024-06-07 06:09:29 INFO EV Power: 0.0 kW
2024-06-07 06:09:29 INFO AC Power: 0.0 kW
2024-06-07 06:09:29 INFO Load Power: 0.5 kW
2024-06-07 06:09:29 INFO Battery Power: 0.932 kW
2024-06-07 06:09:29 INFO Battery SOC: 48.4%

Fetching current operational mode...
2024-06-07 06:09:29 INFO Current Operational Mode: TOU
```
