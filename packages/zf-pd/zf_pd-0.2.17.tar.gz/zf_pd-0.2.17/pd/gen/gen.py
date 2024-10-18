import json
import os
from os import path as os_path
from typing import Tuple

from click import Path, argument, group, option
from loguru import logger
from openai import OpenAI
from tqdm import tqdm

from pd.__model__.utils import parse_str_list_str

api_key = os.getenv("PD_OPENAI_API_KEY")
if not api_key:
    logger.info("PD_OPENAI_API_KEY is not set, using default API key")
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


@group(name="gen", help="Generate embeddings for files")
def gen():
    pass


@gen.command(help="Generate embeddings for files")
@option("--model", default="text-embedding-3-small", help="Model to use for embedding")
@option("--keys", callback=parse_str_list_str, type=str, help="Comma separated list of keys to use for embedding")
@argument("filepaths", nargs=-1, type=Path(exists=True), required=True)
def embeddings(filepaths: Tuple[str, ...], model: str, keys: list[str]):
    data: dict[str, str] = {}
    for path in filepaths:
        path_splits = path.split("/")
        filedir = "/".join(path_splits[:-1])

        filename, fileext = os_path.splitext(path_splits[-1])

        if not fileext == ".json":
            raise ValueError(f"File {filename} is not a JSON file")

        logger.debug(f"Path = {path}, filename = {filename}, fileext = {fileext}")

        with open(path, "r") as f:
            filedata = json.load(f)

            if not keys:
                data[filename] = json.dumps(filedata)
            else:
                keyed_data: dict[str, str] = {}
                for key in keys:
                    if key in filedata:
                        keyed_data[key] = filedata[key]

                data[filename] = json.dumps(keyed_data)

    keys = list(data.keys())
    response = client.embeddings.create(input=list(data.values()), model=model)
    if not response.data:
        raise ValueError(f"No embeddings returned for {keys}")

    logger.info(f"Response: {response.data}")

    for i, embedding in tqdm(list(enumerate(response.data))):
        with open(f"{filedir}/{keys[i]}.ebd", "w") as f:
            json.dump(embedding.embedding, f)
