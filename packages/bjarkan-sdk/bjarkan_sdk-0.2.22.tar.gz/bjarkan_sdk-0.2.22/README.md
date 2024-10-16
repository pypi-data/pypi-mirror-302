# Bjarkan SDK

A Python SDK for accessing both the Smart Order Router (SOR) API and Historical Market Data services of Bjarkan.

## Installation

You can install the Bjarkan SDK using pip:

```
pip install bjarkan-sdk
```

## Usage

The SDK provides two main client classes:

1. `BjarkanDataClient`: For interacting with the Historical Market Data API (data.bjarkan.io)
2. `BjarkanSORClient`: For interacting with the Smart Order Router API (api.bjarkan.io)

Here's a quick example of how to use both clients:

```python
from bjarkan_sdk import BjarkanDataClient, BjarkanSORClient
from datetime import datetime, timedelta

# Initialize the clients
data_client = BjarkanDataClient()
sor_client = BjarkanSORClient()

# Authenticate
data_client.authenticate("your_username", "your_password")
sor_client.authenticate("your_username", "your_password")

# Using the SOR API
orderbook_config = {
    "aggregated": True,
    "exchanges": ["binance", "okx", "htx"],
    "symbols": ["BTC/USDT", "ETH/USDT"],
    "depth": 10
}
result = sor_client.set_orderbook_config(orderbook_config)
print("Orderbook config set:", result)

latest_orderbook = sor_client.get_latest_orderbook()
print("Latest orderbook:", latest_orderbook)

# Using the Data API
tables = data_client.get_tables()
print("Available tables:", tables)

result = data_client.get_history(
    table_name="example_table",
    start_time=datetime.now() - timedelta(hours=1),
    end_time=datetime.now(),
    exchange='binance',
    symbol="BTC/USDT",
    bucket_period="1 minute",
    sort_descending=False,
    limit=100
)
print("Historical data:", result['data'][:5])  # Print first 5 entries
print(f"Query performance: {result['query_performance_seconds']:.4f} seconds")
```

## API Reference

### `BjarkanDataClient`

The `BjarkanDataClient` class is used for interacting with the Bjarkan Historical Market Data service.

#### `__init__(base_url: str = 'https://data.bjarkan.io')`
Initialize the client with the base URL of the Bjarkan Data service.

#### `authenticate(username: str, password: str)`
Authenticate with the Data service using your username and password. This method must be called before making any other API calls.

#### Methods

- `get_tables() -> List[Dict[str, any]]`
- `get_history(table_name: str, start_time: datetime, end_time: datetime, ...) -> Dict[str, any]`
- `get_paginated_history(table_name: str, start_time: datetime, end_time: datetime, ...) -> Iterator[Dict[str, any]]`
- `validate_bucket_period(bucket_period: str) -> bool`

### `BjarkanSORClient`

The `BjarkanSORClient` class is used for interacting with the Bjarkan Smart Order Router API.

#### `__init__(base_url: str = 'https://api.bjarkan.io')`
Initialize the client with the base URL of the Bjarkan SOR API service.

#### `authenticate(username: str, password: str)`
Authenticate with the SOR API service using your username and password. This method must be called before making any other API calls.

#### Methods

- `set_orderbook_config(config: Dict) -> Dict`
- `get_orderbook_config() -> Dict`
- `set_trades_config(config: Dict) -> Dict`
- `get_trades_config() -> Dict`
- `set_api_keys(api_configs: List[Dict]) -> Dict`
- `get_api_keys() -> Dict`
- `get_latest_orderbook() -> Dict`
- `execute_order(order: Dict) -> Dict`
- `get_balances() -> Dict`

For detailed information on each method, please refer to the docstrings in the source code.

## Examples

### Setting Orderbook Configuration (SOR API)

```python
sor_client = BjarkanSORClient()
sor_client.authenticate("your_username", "your_password")

orderbook_config = {
    "aggregated": True,
    "exchanges": ["binance", "okx", "htx"],
    "symbols": ["BTC/USDT", "ETH/USDT"],
    "depth": 10
}
result = sor_client.set_orderbook_config(orderbook_config)
print("Orderbook config set:", result)
```

### Fetching Historical Data with Pagination (Data API)

```python
from datetime import datetime, timedelta

data_client = BjarkanDataClient()
data_client.authenticate("your_username", "your_password")

start_time = datetime.now() - timedelta(days=1)
end_time = datetime.now()

for page in data_client.get_paginated_history(
    table_name="example_table",
    start_time=start_time,
    end_time=end_time,
    exchange="binance",
    symbol="BTC/USDT",
    bucket_period="5 minutes",
    page_size=500
):
    print(f"Retrieved {len(page['data'])} records")
    print(f"Query performance: {page['query_performance_seconds']:.4f} seconds")
    # Process the data in the current page
    for record in page['data']:
        # Do something with each record
        pass
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.