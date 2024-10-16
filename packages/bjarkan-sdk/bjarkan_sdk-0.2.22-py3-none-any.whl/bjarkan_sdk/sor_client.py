import asyncio
import websockets
import json
from .base_client import BaseClient
from .models import OrderbookConfig, TradesConfig, OrderConfig, APIConfig
from typing import Dict, List, AsyncIterator
from urllib.parse import urlparse


class BjarkanSORClient(BaseClient):
    def __init__(self, base_url: str = 'http://localhost:8000'):  # https://api.bjarkan.io OR http://localhost:8000
        super().__init__(base_url)
        parsed_url = urlparse(base_url)
        ws_scheme = 'wss' if parsed_url.scheme == 'https' else 'ws'
        self.ws_base_url = f"{ws_scheme}://{parsed_url.netloc}"

    def set_orderbook_config(self, config: OrderbookConfig) -> Dict:
        return self._make_request('POST', 'orderbook_config/set', json=config.dict())

    def get_orderbook_config(self) -> OrderbookConfig:
        data = self._make_request('GET', 'orderbook_config/get')
        return OrderbookConfig(**data)

    def set_trades_config(self, config: TradesConfig) -> Dict:
        return self._make_request('POST', 'trades_config/set', json=config.dict())

    def get_trades_config(self) -> TradesConfig:
        data = self._make_request('GET', 'trades_config/get')
        return TradesConfig(**data)

    def set_api_keys(self, api_configs: List[APIConfig]) -> Dict:
        return self._make_request('POST', 'api_keys/set', json=[config.dict() for config in api_configs])

    def get_api_keys(self) -> List[APIConfig]:
        data = self._make_request('GET', 'api_keys/get')
        return [APIConfig(**config) for config in data]

    def get_latest_orderbook(self) -> Dict:
        return self._make_request('GET', 'get_latest_orderbook')

    def execute_order(self, order: OrderConfig) -> Dict:
        return self._make_request('POST', 'execute_order', json=order.dict())

    def get_balances(self) -> Dict:
        return self._make_request('GET', 'get_balances')

    def start_stream(self, stream_type: str) -> Dict:
        return self._make_request('POST', f'start_stream?stream_type={stream_type}')

    def stop_stream(self, stream_type: str) -> Dict:
        return self._make_request('POST', f'stop_stream?stream_type={stream_type}')

    async def connect_stream(self, stream_type: str) -> AsyncIterator[Dict]:
        uri = f"{self.ws_base_url}/connect_stream?token={self.token}&type={stream_type}"
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    try:
                        message = await websocket.recv()
                        yield json.loads(message)
                    except websockets.exceptions.ConnectionClosed:
                        print(f"{stream_type} WebSocket connection closed. Attempting to reconnect...")
                        break
        except websockets.exceptions.WebSocketException as e:
            print(f"WebSocket error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
