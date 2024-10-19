# mj_aws

## Minimal testing for gRPC latency testing! 

### 1. Install

```bash
pip install -e . -v
```

you also need to make sure `unzip` command line tool is installed on your system.


### 2. Launch gRPC server on AWS. 
```bash
python avp_stream2/grpc_aws_server.py
```

### 3. Launch gRPC client (this emulates Apple Vision Pro)

```bash
python avp_stream2/grpc_avp_client.py
```

Note that actually, things are running this way: 

1. `python listener.py`  is always running, serving as an HTTP server receiving user's request. 
2. Upon user's request, it launches the simulation instance `python runs/dual_panda.py` via `subprocess`. 
3. Inside the simulation instance, `HandTrackingServer` is running like this: 
    ```python
    from avp_stream2 import HandTrackingServer 
    streamer = HandTrackingServer()
    streamer.start()
    ```


## Testing out MuJoCo sim  

```bash
python runs/dual_panda.py --task mug_hang --robot dual_panda
```

If you're running things on MacOS, replace `python` with `mjpython`. 

