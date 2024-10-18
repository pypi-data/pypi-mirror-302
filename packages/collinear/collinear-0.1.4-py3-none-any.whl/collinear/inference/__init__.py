import asyncio

import pandas as pd
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm

from collinear.BaseService import BaseService
from collinear.judge.types import ConversationMessage


class Inference(BaseService):
    def __init__(self, access_token: str) -> None:
        super().__init__(access_token)


    async def run_inference_on_dataset(self, data: pd.DataFrame,
                                       conv_prefix_column_name: str,
                                       model: str, api_url: str, api_key: str | None) -> pd.DataFrame:
        if api_key is None:
            api_key = 'NA'
        client = AsyncOpenAI(base_url=api_url, api_key=api_key)
        pbar = tqdm(total=len(data))
        if conv_prefix_column_name not in data.columns:
            raise ValueError(f"Column {conv_prefix_column_name} not found in the dataset")

        async def generate(example):
            messages = [ConversationMessage(**m).dict() for m in example[conv_prefix_column_name]]
            response = await client.chat.completions.create(messages=messages, model=model)
            if not response:
                example["response"] = None,
            else:
                example["response"] = {'role': 'assistant', 'content': response.choices.pop().message.content}
            pbar.update(1)
            return example

        tasks = []
        for idx, row in data.iterrows():
            tasks.append(asyncio.create_task(generate(row)))
        results = await asyncio.gather(*tasks)
        result_df = pd.DataFrame({
            'conv_prefix': [row[conv_prefix_column_name] for row in results],
            'response': [row['response'] for row in results]
        })

        return result_df
