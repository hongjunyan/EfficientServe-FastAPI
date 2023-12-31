# EfficientServe-FastAPI

<img src="imgs/docker_fastapi_nginx.png" alt="docker_fastapi_nginx" width="600px"/>

## Install nvidia-docker
```commandline
$> sudo apt-get update
$> sudo apt-get install -y nvidia-docker2
$> sudo systemctl restart docker
```

## Build Image
- app
    ```commandline
    $> cd dockers/app
    $> docker build -t demo_app .
    ```

## Run Service
- App: Chinese NER application (https://huggingface.co/JasonYan/bert-base-chinese-stock-ner)
    ```commandline
    $> cd dockers/app
    $> docker compose up -d
    ```

- Nginx: Load Balancer
    
    ```commandline
    $> cd dockers/nginx
    ```
  
    step1: edited upstream servers
    ```
    upstream ner_service {
        server <host>:<port>;  # <- change here
    }
    ```
  
    step2: run service
    ```commandline
    $> docker-compose up -d
    ```

    step3: set replicas and update serivce
    ```bash
    $> docker compose up -d --remove-orphans
    ```

- Dozzle: Monitor Container

  ```commandline
  $> cd dockers/dozzle
  $> docker compose up -d
  ```


## Test the performance
You can try changing `num_threads` in `stress_test.py` or adding/removing the upstream server
```
$> python stress_test.py
```


## Additional settings
apply ThreadPoolExecutor(worker=1) for async model_predict will get more stable and faster responses
