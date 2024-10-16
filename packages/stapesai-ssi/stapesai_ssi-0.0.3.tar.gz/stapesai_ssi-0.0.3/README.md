# SSI (Speech Super Intelligence)

<!-- @mayank https://www.markepear.com/blog/github-search-engine-optimization
https://www.codemotion.com/magazine/dev-life/github-project/ -->

![SSI Demo Video](https://placehold.co/600x400?text=@shar-mayank+bhai+demo+video+:please-emoji:)

usecase 1 - use in existing reposall models will be loaded from the existing repo and then the server will be started

```bash
pip install ssi
```

```python
from fastapi import FastAPI
from stapesai_ssi.fastapi import StreamingWSRouter
from stapesai_ssi.types import StreamingDataChunk, NewClientConnected

app = FastAPI()

def asr_callback(data: StreamingDataChunk):
    print(data)

def new_client_callback(data: NewClientConnected):
    print(data)

streaming_ws_router = StreamingWSRouter(
    asr_callback=asr_callback,
    new_client_callback=new_client_callback,
    endpoint="/ws/transcribe"
)

app.include_router(streaming_ws_router)
```

usecase 2 - deploy as a docker server and then use in existing repos
here SSI server is deployed as a docker container and then ssi_client can be used in existing repos

```bash
pip install ssi[client]
```

```python
from fastapi import FastAPI
from stapesai_ssi.clients import StreamingClient
from stapesai_ssi.types import StreamingDataChunk

app = FastAPI()

def asr_callback(data: StreamingDataChunk):
    print(data)

def new_client_callback(data: NewClientConnected):
    print(data)

ssi_client = StreamingClient(
    server_host="<remote_server_ip>",
    server_port=<remote_server_port>,
    asr_callback=asr_callback,
    new_client_callback=new_client_callback,
)

app.include_router(ssi_client.fastapi_proxy_router)
```

usecase 3 - CLI (for local system as well as simple socket server)
bc dimak nhi chal rha abhi

python setup.py sdist bdist_wheel

twine upload dist/* --verbose
