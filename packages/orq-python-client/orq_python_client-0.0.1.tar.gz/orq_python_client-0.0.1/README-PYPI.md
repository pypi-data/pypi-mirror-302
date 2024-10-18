# orq-python-client

Developer-friendly & type-safe Python SDK specifically catered to leverage *orq-python-client* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=orq-python-client&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<br /><br />
> [!IMPORTANT]
> This SDK is not yet ready for production use. To complete setup please follow the steps outlined in your [workspace](https://app.speakeasy.com/org/orq/orq). Delete this section before > publishing to a package manager.

<!-- Start Summary [summary] -->
## Summary

[Dev] orq.ai API: The Orquesta API

For more information about the API: [orq.ai Documentation](https://docs.orq.ai)
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents

* [SDK Installation](#sdk-installation)
* [IDE Support](#ide-support)
* [SDK Example Usage](#sdk-example-usage)
* [Available Resources and Operations](#available-resources-and-operations)
* [Server-sent event streaming](#server-sent-event-streaming)
* [Retries](#retries)
* [Error Handling](#error-handling)
* [Server Selection](#server-selection)
* [Custom HTTP Client](#custom-http-client)
* [Authentication](#authentication)
* [Debugging](#debugging)
<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install git+<UNSET>.git
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add git+<UNSET>.git
```
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from orq_python_client import Orq
import os

s = Orq(
    bearer=os.getenv("ORQ_BEARER", ""),
)

res = s.contacts.post_contacts(request={
    "external_id": "<id>",
})

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from orq_python_client import Orq
import os

async def main():
    s = Orq(
        bearer=os.getenv("ORQ_BEARER", ""),
    )
    res = await s.contacts.post_contacts_async(request={
        "external_id": "<id>",
    })
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [contacts](docs/sdks/contacts/README.md)

* [post_contacts](docs/sdks/contacts/README.md#post_contacts) - Update user information

### [deployments](docs/sdks/deploymentssdk/README.md)

* [post_v2_deployments_get_config](docs/sdks/deploymentssdk/README.md#post_v2_deployments_get_config) - Get config
* [post_v2_deployments_invoke](docs/sdks/deploymentssdk/README.md#post_v2_deployments_invoke) - Invoke
* [post_v2_deployments_id_metrics](docs/sdks/deploymentssdk/README.md#post_v2_deployments_id_metrics) - Add metrics

### [feedback](docs/sdks/feedback/README.md)

* [post_feedback](docs/sdks/feedback/README.md#post_feedback) - Submit feedback

### [files](docs/sdks/files/README.md)

* [post_v2_files](docs/sdks/files/README.md#post_v2_files) - Upload file
* [post_v2_files_bulk](docs/sdks/files/README.md#post_v2_files_bulk) - Bulk upload file


### [public](docs/sdks/public/README.md)

* [post_v2_deployments_get_config](docs/sdks/public/README.md#post_v2_deployments_get_config) - Get config
* [post_v2_deployments_invoke](docs/sdks/public/README.md#post_v2_deployments_invoke) - Invoke
* [post_v2_deployments_id_metrics](docs/sdks/public/README.md#post_v2_deployments_id_metrics) - Add metrics
* [post_v2_files](docs/sdks/public/README.md#post_v2_files) - Upload file
* [post_v2_files_bulk](docs/sdks/public/README.md#post_v2_files_bulk) - Bulk upload file
* [post_v2_router_embeddings](docs/sdks/public/README.md#post_v2_router_embeddings) - Embeddings
* [post_v2_router_chat_completions](docs/sdks/public/README.md#post_v2_router_chat_completions) - Chat
* [post_v2_router_completions](docs/sdks/public/README.md#post_v2_router_completions) - legacy completions route
* [post_v2_router_rerank](docs/sdks/public/README.md#post_v2_router_rerank) - rerank route
* [post_v2_router_images_generations](docs/sdks/public/README.md#post_v2_router_images_generations)
* [post_v2_resources_datasets](docs/sdks/public/README.md#post_v2_resources_datasets) - Create a dataset
* [get_v2_resources_datasets](docs/sdks/public/README.md#get_v2_resources_datasets) - Get all datasets
* [delete_v2_resources_datasets_dataset_id_](docs/sdks/public/README.md#delete_v2_resources_datasets_dataset_id_) - Delete a dataset
* [get_v2_resources_datasets_dataset_id_](docs/sdks/public/README.md#get_v2_resources_datasets_dataset_id_) - Get one  dataset
* [patch_v2_resources_datasets_dataset_id_](docs/sdks/public/README.md#patch_v2_resources_datasets_dataset_id_) - Update a dataset
* [post_v2_resources_datasets_dataset_id_rows_bulk](docs/sdks/public/README.md#post_v2_resources_datasets_dataset_id_rows_bulk) - Create a list of dataset rows
* [delete_v2_resources_datasets_dataset_id_rows_bulk](docs/sdks/public/README.md#delete_v2_resources_datasets_dataset_id_rows_bulk) - Delete a list of dataset rows
* [post_v2_resources_datasets_dataset_id_rows](docs/sdks/public/README.md#post_v2_resources_datasets_dataset_id_rows) - Create a dataset row
* [get_v2_resources_datasets_dataset_id_rows](docs/sdks/public/README.md#get_v2_resources_datasets_dataset_id_rows) - Retrieve all dataset rows
* [delete_v2_resources_datasets_dataset_id_rows_row_id_](docs/sdks/public/README.md#delete_v2_resources_datasets_dataset_id_rows_row_id_) - Delete a dataset row
* [get_v2_resources_datasets_dataset_id_rows_row_id_](docs/sdks/public/README.md#get_v2_resources_datasets_dataset_id_rows_row_id_) - Get one dataset row
* [patch_v2_resources_datasets_dataset_id_rows_row_id_](docs/sdks/public/README.md#patch_v2_resources_datasets_dataset_id_rows_row_id_) - Update a dataset row

### [resources](docs/sdks/resources/README.md)

* [post_v2_resources_datasets](docs/sdks/resources/README.md#post_v2_resources_datasets) - Create a dataset
* [get_v2_resources_datasets](docs/sdks/resources/README.md#get_v2_resources_datasets) - Get all datasets
* [delete_v2_resources_datasets_dataset_id_](docs/sdks/resources/README.md#delete_v2_resources_datasets_dataset_id_) - Delete a dataset
* [get_v2_resources_datasets_dataset_id_](docs/sdks/resources/README.md#get_v2_resources_datasets_dataset_id_) - Get one  dataset
* [patch_v2_resources_datasets_dataset_id_](docs/sdks/resources/README.md#patch_v2_resources_datasets_dataset_id_) - Update a dataset
* [post_v2_resources_datasets_dataset_id_rows_bulk](docs/sdks/resources/README.md#post_v2_resources_datasets_dataset_id_rows_bulk) - Create a list of dataset rows
* [delete_v2_resources_datasets_dataset_id_rows_bulk](docs/sdks/resources/README.md#delete_v2_resources_datasets_dataset_id_rows_bulk) - Delete a list of dataset rows
* [post_v2_resources_datasets_dataset_id_rows](docs/sdks/resources/README.md#post_v2_resources_datasets_dataset_id_rows) - Create a dataset row
* [get_v2_resources_datasets_dataset_id_rows](docs/sdks/resources/README.md#get_v2_resources_datasets_dataset_id_rows) - Retrieve all dataset rows
* [delete_v2_resources_datasets_dataset_id_rows_row_id_](docs/sdks/resources/README.md#delete_v2_resources_datasets_dataset_id_rows_row_id_) - Delete a dataset row
* [get_v2_resources_datasets_dataset_id_rows_row_id_](docs/sdks/resources/README.md#get_v2_resources_datasets_dataset_id_rows_row_id_) - Get one dataset row
* [patch_v2_resources_datasets_dataset_id_rows_row_id_](docs/sdks/resources/README.md#patch_v2_resources_datasets_dataset_id_rows_row_id_) - Update a dataset row

### [router](docs/sdks/router/README.md)

* [post_v2_router_embeddings](docs/sdks/router/README.md#post_v2_router_embeddings) - Embeddings
* [post_v2_router_chat_completions](docs/sdks/router/README.md#post_v2_router_chat_completions) - Chat
* [post_v2_router_completions](docs/sdks/router/README.md#post_v2_router_completions) - legacy completions route
* [post_v2_router_rerank](docs/sdks/router/README.md#post_v2_router_rerank) - rerank route
* [post_v2_router_images_generations](docs/sdks/router/README.md#post_v2_router_images_generations)

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Server-sent event streaming [eventstream] -->
## Server-sent event streaming

[Server-sent events][mdn-sse] are used to stream content from certain
operations. These operations will expose the stream as [Generator][generator] that
can be consumed using a simple `for` loop. The loop will
terminate when the server no longer has any events to send and closes the
underlying connection.

```python
from orq_python_client import Orq
import os

s = Orq(
    bearer=os.getenv("ORQ_BEARER", ""),
)

res = s.deployments.post_v2_deployments_invoke(request={
    "key": "<key>",
})

if res is not None:
    for event in res:
        # handle event
        print(event, flush=True)

```

[mdn-sse]: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
[generator]: https://wiki.python.org/moin/Generators
<!-- End Server-sent event streaming [eventstream] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from orq.utils import BackoffStrategy, RetryConfig
from orq_python_client import Orq
import os

s = Orq(
    bearer=os.getenv("ORQ_BEARER", ""),
)

res = s.contacts.post_contacts(request={
    "external_id": "<id>",
},
    RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

if res is not None:
    # handle response
    pass

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from orq.utils import BackoffStrategy, RetryConfig
from orq_python_client import Orq
import os

s = Orq(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    bearer=os.getenv("ORQ_BEARER", ""),
)

res = s.contacts.post_contacts(request={
    "external_id": "<id>",
})

if res is not None:
    # handle response
    pass

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.SDKError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `get_v2_resources_datasets_dataset_id__async` method may raise the following exceptions:

| Error Type                                                  | Status Code                                                 | Content Type                                                |
| ----------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------- |
| models.GetV2ResourcesDatasetsDatasetIDResourcesResponseBody | 404                                                         | application/json                                            |
| models.SDKError                                             | 4XX, 5XX                                                    | \*/\*                                                       |

### Example

```python
from orq_python_client import Orq, models
import os

s = Orq(
    bearer=os.getenv("ORQ_BEARER", ""),
)

res = None
try:
    res = s.public.get_v2_resources_datasets_dataset_id_(dataset_id="<id>")

    if res is not None:
        # handle response
        pass

except models.GetV2ResourcesDatasetsDatasetIDResourcesResponseBody as e:
    # handle e.data: models.GetV2ResourcesDatasetsDatasetIDResourcesResponseBodyData
    raise(e)
except models.SDKError as e:
    # handle exception
    raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Index

You can override the default server globally by passing a server index to the `server_idx: int` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the indexes associated with the available servers:

| # | Server | Variables |
| - | ------ | --------- |
| 0 | `https://my.dev.orq.ai` | None |

#### Example

```python
from orq_python_client import Orq
import os

s = Orq(
    server_idx=0,
    bearer=os.getenv("ORQ_BEARER", ""),
)

res = s.contacts.post_contacts(request={
    "external_id": "<id>",
})

if res is not None:
    # handle response
    pass

```


### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from orq_python_client import Orq
import os

s = Orq(
    server_url="https://my.dev.orq.ai",
    bearer=os.getenv("ORQ_BEARER", ""),
)

res = s.contacts.post_contacts(request={
    "external_id": "<id>",
})

if res is not None:
    # handle response
    pass

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from orq_python_client import Orq
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Orq(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from orq_python_client import Orq
from orq_python_client.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Orq(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name                 | Type                 | Scheme               | Environment Variable |
| -------------------- | -------------------- | -------------------- | -------------------- |
| `bearer`             | http                 | HTTP Bearer          | `ORQ_BEARER`         |

To authenticate with the API the `bearer` parameter must be set when initializing the SDK client instance. For example:
```python
from orq_python_client import Orq
import os

s = Orq(
    bearer=os.getenv("ORQ_BEARER", ""),
)

res = s.contacts.post_contacts(request={
    "external_id": "<id>",
})

if res is not None:
    # handle response
    pass

```
<!-- End Authentication [security] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from orq_python_client import Orq
import logging

logging.basicConfig(level=logging.DEBUG)
s = Orq(debug_logger=logging.getLogger("orq_python_client"))
```

You can also enable a default debug logger by setting an environment variable `ORQ_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=orq-python-client&utm_campaign=python)
