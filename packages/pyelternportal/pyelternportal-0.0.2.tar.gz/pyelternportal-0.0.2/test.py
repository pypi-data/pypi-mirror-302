import asyncio

import importlib.util
import sys
spec = importlib.util.spec_from_file_location("pyelternportal", r"C:\GitHub\michull\pyelternportal\src\pyelternportal\__init__.py")
pyelternportal = importlib.util.module_from_spec(spec)
sys.modules["pyelternportal"] = pyelternportal
spec.loader.exec_module(pyelternportal)

async def test_api():
    api = pyelternportal.ElternPortalAPI()
    print(f"timezone:\t{api.timezone.zone}")

    api.set_config("nfgymuc", r"michael@ullrich.bayern", r"chHs8QjMA&#tTMN5$HI0")
    print(f"school:\t\t{api.school}")
    print(f"username:\t{api.username}")
    print(f"password:\t{api.password}")
    print(f"base_url:\t{api.base_url}")

    await api.async_validate_config()
    print(f"ip:\t\t{api.ip}")
    print(f"csrf:\t\t{api.csrf}")
    print(f"school_name:\t{api.school_name}")

    # await api.async_update()
    

asyncio.run(test_api())