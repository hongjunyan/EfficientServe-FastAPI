## Step1: Build Image
```bash
$> docker build -t demo_ner .
```

## Step2: Run Service
```bash
$> docker-compose -f docker-compose-multi.yaml up -d
```