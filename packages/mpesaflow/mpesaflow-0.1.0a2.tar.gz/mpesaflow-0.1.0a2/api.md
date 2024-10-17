# Mpesaflow

Types:

```python
from mpesaflow.types import HealthResponse
```

Methods:

- <code title="get /health">client.<a href="./src/mpesaflow/_client.py">health</a>() -> str</code>

# Apps

Types:

```python
from mpesaflow.types import Application, AppCreateResponse, AppListResponse, AppDeleteResponse
```

Methods:

- <code title="post /apps/create">client.apps.<a href="./src/mpesaflow/resources/apps/apps.py">create</a>(\*\*<a href="src/mpesaflow/types/app_create_params.py">params</a>) -> <a href="./src/mpesaflow/types/app_create_response.py">AppCreateResponse</a></code>
- <code title="get /apps/list">client.apps.<a href="./src/mpesaflow/resources/apps/apps.py">list</a>(\*\*<a href="src/mpesaflow/types/app_list_params.py">params</a>) -> <a href="./src/mpesaflow/types/app_list_response.py">AppListResponse</a></code>
- <code title="delete /apps/{appId}">client.apps.<a href="./src/mpesaflow/resources/apps/apps.py">delete</a>(app_id) -> <a href="./src/mpesaflow/types/app_delete_response.py">AppDeleteResponse</a></code>

## APIKeys

Types:

```python
from mpesaflow.types.apps import APIKeyCreateResponse, APIKeyListResponse, APIKeyDeleteResponse
```

Methods:

- <code title="post /apps/{appId}/api-keys/create">client.apps.api_keys.<a href="./src/mpesaflow/resources/apps/api_keys.py">create</a>(app_id, \*\*<a href="src/mpesaflow/types/apps/api_key_create_params.py">params</a>) -> <a href="./src/mpesaflow/types/apps/api_key_create_response.py">APIKeyCreateResponse</a></code>
- <code title="get /apps/{appId}/api-keys/list">client.apps.api_keys.<a href="./src/mpesaflow/resources/apps/api_keys.py">list</a>(app_id, \*\*<a href="src/mpesaflow/types/apps/api_key_list_params.py">params</a>) -> <a href="./src/mpesaflow/types/apps/api_key_list_response.py">APIKeyListResponse</a></code>
- <code title="delete /apps/{appId}/api-keys/{apiKeyId}">client.apps.api_keys.<a href="./src/mpesaflow/resources/apps/api_keys.py">delete</a>(api_key_id, \*, app_id) -> <a href="./src/mpesaflow/types/apps/api_key_delete_response.py">APIKeyDeleteResponse</a></code>

# Transactions

Types:

```python
from mpesaflow.types import Transaction, TransactionCreateResponse, TransactionListResponse
```

Methods:

- <code title="post /transactions/create">client.transactions.<a href="./src/mpesaflow/resources/transactions.py">create</a>(\*\*<a href="src/mpesaflow/types/transaction_create_params.py">params</a>) -> <a href="./src/mpesaflow/types/transaction_create_response.py">TransactionCreateResponse</a></code>
- <code title="get /transactions/{transactionId}">client.transactions.<a href="./src/mpesaflow/resources/transactions.py">retrieve</a>(transaction_id) -> <a href="./src/mpesaflow/types/transaction.py">Transaction</a></code>
- <code title="get /transactions/list">client.transactions.<a href="./src/mpesaflow/resources/transactions.py">list</a>(\*\*<a href="src/mpesaflow/types/transaction_list_params.py">params</a>) -> <a href="./src/mpesaflow/types/transaction_list_response.py">TransactionListResponse</a></code>
