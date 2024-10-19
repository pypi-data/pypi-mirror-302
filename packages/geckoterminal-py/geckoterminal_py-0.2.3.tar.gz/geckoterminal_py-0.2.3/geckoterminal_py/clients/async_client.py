from typing import Optional, List, Callable, Any
import asyncio

import httpx
import pandas as pd
from glom import glom

from geckoterminal_py.base_client import GeckoTerminalClientBase
import geckoterminal_py.constants as CONSTANTS


class GeckoTerminalAsyncClient(GeckoTerminalClientBase):
    def __init__(self, transport: Optional[httpx.MockTransport] = None):
        if transport:
            self.client = httpx.AsyncClient(headers=self.headers, transport=transport)
        else:
            self.client = httpx.AsyncClient(headers=self.headers)

    async def api_request(self, method: str, path: str, params: Optional[dict] = None) -> dict:
        url = f"{self.base_url}/{path}"
        response = await self.client.request(method, url, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()

    async def get_networks(self) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_NETWORKS_PATH)
        networks = glom(response, CONSTANTS.NETWORK_SPEC)
        return pd.DataFrame(networks)

    async def get_dexes_by_network(self, network_id: str) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_DEXES_BY_NETWORK_PATH.format(network_id))
        dexes_by_network = glom(response, CONSTANTS.DEXES_BY_NETWORK_SPEC)
        return pd.DataFrame(dexes_by_network)

    async def get_trending_pools(self) -> pd.DataFrame:
        all_pools = await self.paginate(self.api_request, CONSTANTS.GET_TRENDING_POOLS_PATH)
        return self.process_pools_list(all_pools)

    async def get_trending_pools_by_network(self, network_id: str) -> pd.DataFrame:
        path = CONSTANTS.GET_TRENDING_POOLS_BY_NETWORK_PATH.format(network_id)
        all_pools = await self.paginate(self.api_request, path)
        return self.process_pools_list(all_pools)

    async def get_top_pools_by_network(self, network_id: str) -> pd.DataFrame:
        path = CONSTANTS.GET_TOP_POOLS_BY_NETWORK_PATH.format(network_id)
        all_pools = await self.paginate(self.api_request, path)
        return self.process_pools_list(all_pools)

    async def get_top_pools_by_network_dex(self, network_id: str, dex_id: str, sort_by: str = "h24_volume_usd_desc") -> pd.DataFrame:
        path = CONSTANTS.GET_TOP_POOLS_BY_NETWORK_DEX_PATH.format(network_id, dex_id)
        params = {"sort_by": sort_by}
        all_pools = await self.paginate(self.api_request, path, params)
        return pd.DataFrame(all_pools).drop_duplicates()

    async def get_pool_by_network_address(self, network_id: str, pool_address: str) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_POOL_BY_NETWORK_AND_ADDRESS_PATH.format(network_id, pool_address))
        response["data"] = [response["data"]]
        pool = glom(response, CONSTANTS.POOL_SPEC)
        return pd.DataFrame(pool)

    async def get_multiple_pools_by_network(self, network_id: str, pool_addresses: list) -> pd.DataFrame:
        pools_str = ",".join(pool_addresses)
        response = await self.api_request("GET", CONSTANTS.GET_MULTIPLE_POOLS_BY_NETWORK_PATH.format(network_id, pools_str))
        pools = glom(response, CONSTANTS.POOL_SPEC)
        return pd.DataFrame(pools)

    async def get_new_pools_by_network(self, network_id: str) -> pd.DataFrame:
        path = CONSTANTS.GET_NEW_POOLS_BY_NETWORK_PATH.format(network_id)
        all_pools = await self.paginate(self.api_request, path)
        return self.process_pools_list(all_pools)

    async def get_new_pools_all_networks(self) -> pd.DataFrame:
        all_pools = await self.paginate(self.api_request, CONSTANTS.GET_NEW_POOLS_ALL_NETWORKS_PATH)
        return self.process_pools_list(all_pools)

    async def get_top_pools_by_network_token(self, network_id: str, token_id: str) -> pd.DataFrame:
        path = CONSTANTS.GET_TOP_POOLS_BY_NETWORK_TOKEN_PATH.format(network_id, token_id)
        all_pools = await self.paginate(self.api_request, path)
        return self.process_pools_list(all_pools)

    async def get_specific_token_on_network(self, network_id: str, token_id: str) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_SPECIFIC_TOKEN_ON_NETWORK_PATH.format(network_id, token_id))
        return response["data"]

    async def get_ohlcv(self, network_id: str, pool_address: str, timeframe: str, before_timestamp: int = None,
                        currency: str = "usd", token: str = "base", limit: int = 1000) -> pd.DataFrame:
        if timeframe not in self.ohlcv_timeframes:
            raise ValueError(f"Timeframe {timeframe} is not supported. Please select one timeframe of the following"
                             f"list {self.ohlcv_timeframes}")
        timeframe, period = self.get_timeframe_and_period(timeframe)
        params = {
            "aggregate": period,
            "limit": limit,
            "currency": currency,
            "token": token,
        }
        if before_timestamp:
            params["before_timestamp"] = before_timestamp
        response = await self.api_request("GET",
                                          CONSTANTS.GET_OHLCV_DATA_PATH.format(network_id, pool_address, timeframe),
                                          params=params)

        df = pd.DataFrame(response["data"]["attributes"]["ohlcv_list"],
                          columns=["timestamp", "open", "high", "low", "close", "volume_usd"])
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
        return df.drop_duplicates(subset="timestamp").sort_values("datetime").reset_index(drop=True)

    async def get_trades(self, network: str, pool_address: str, trade_volume_filter: Optional[float]) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_TRADES_BY_NETWORK_POOL_PATH.format(network, pool_address),
                                          params={"trade_volume_in_usd_greater_than": trade_volume_filter})
        trades = glom(response, CONSTANTS.TRADES_SPEC)
        return pd.DataFrame(trades)

    async def paginate(self, 
                       request_func: Callable, 
                       path: str, 
                       params: Optional[dict] = None, 
                       max_pages: int = 10) -> List[Any]:
        all_items = []
        params = params or {}
        
        for page in range(1, max_pages + 1):
            try:
                params['page'] = page
                response = await request_func("GET", path, params=params)
                items = glom(response, CONSTANTS.POOL_SPEC)
                if not items:
                    break
                all_items.extend(items)
                
                # Check if we've reached the last page
                if len(items) == 0:
                    break
            except Exception as e:
                print(f"Error fetching items from page {page}: {e}")
                break
        
        return all_items
