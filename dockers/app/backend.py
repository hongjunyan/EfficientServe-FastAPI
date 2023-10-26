from fastapi import FastAPI, Request
import uvicorn
import time
import os
from models import NERModel
from utils import create_logger


# os.environ["HF_DATASETS_CACHE"] = "D:/Projects/token_classification/try_api/hf_cache"
app = FastAPI()
logger = create_logger("demo", "./logs")
model = NERModel("JasonYan/bert-base-chinese-stock-ner", use_gpu=True)


def model_predict():
    text = "世界先進9月合併營收約為34.44億元，較去年同月減少6.75%，也較上月減少2.06%。"*100
    ner_result = model(text)
    time.sleep(2)
    return ner_result


def save_to_db(ner_result):
    time.sleep(1)
    return ner_result


@app.get("/")
def entrypoint(request: Request):
    ts = time.time()
    ner_result = model_predict()
    es = time.time()
    logger.info(f"Model  : cost: {es-ts}, start: {ts}, end: {es}")

    ts = time.time()
    result = save_to_db(ner_result)
    es = time.time()
    logger.info(f"io task: : cost: {es-ts}, start: {ts}, end: {es}")
    return result


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9999, root_path="/ner/")
