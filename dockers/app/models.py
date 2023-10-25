from typing import Union
from pathlib import Path
from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForTokenClassification
from optimum.pipelines import pipeline


def convert_hf_to_onnx(model_checkpoint: str, save_directory: str, pipeline_tag: str):
    """
    INPUTS
    ------
        checkpoint: str,
            e.g.,  "JasonYan/bert-base-chinese-stock"

        save_directory: str,
            e.g., "./onnx"

        pipeline_tag: str,
            same as transformer pipeline_tag, e.g, "token-classification"
    """
    model_checkpoint = model_checkpoint
    save_directory = save_directory

    # Load a model from transformers and export it to ONNX
    if pipeline_tag == "token-classification":
        ort_model = ORTModelForTokenClassification.from_pretrained(model_checkpoint, export=True, cache_dir="./hf_cache")
        tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

        # Save the onnx model and tokenizer
        ort_model.save_pretrained(save_directory)
        tokenizer.save_pretrained(save_directory)


class NERModel(object):
    def __init__(self, checkpoint: str, use_gpu=False):
        self.checkpoint = checkpoint
        self.use_gpu = use_gpu
        self.pipeline = self.build_model("./onnx")

    def build_model(self, save_dir: str):
        save_dir = Path(save_dir)
        if not save_dir.exists():
            convert_hf_to_onnx(self.checkpoint, str(save_dir), pipeline_tag="token-classification")

        if self.use_gpu:
            model = ORTModelForTokenClassification.from_pretrained(str(save_dir), provider="CUDAExecutionProvider")
        else:
            model = ORTModelForTokenClassification.from_pretrained(str(save_dir), provider="CPUExecutionProvider")
        tokenizer = AutoTokenizer.from_pretrained(str(save_dir))
        return pipeline("token-classification", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    def __call__(self, inp_sentence: str):
        ners = self.pipeline(inp_sentence)
        results = []  # (ENTITY, value)
        for ner in ners:
            results.append((ner["entity_group"], inp_sentence[ner["start"]:ner["end"]]))
        return results