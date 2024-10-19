import asyncio
import uuid

import pandas as pd
from tqdm.asyncio import tqdm
from asynciolimiter import Limiter

from collinear.BaseService import BaseService


class Inference(BaseService):
    def __init__(self, access_token: str) -> None:
        super().__init__(access_token)

    async def run_inference_on_dataset(self, data: pd.DataFrame,
                                       conv_prefix_column_name: str,
                                       model_id: uuid.UUID,
                                       generation_kwargs={},
                                       calls_per_second: int = 10) -> pd.DataFrame:

        pbar = tqdm(total=len(data))
        if conv_prefix_column_name not in data.columns:
            raise ValueError(f"Column {conv_prefix_column_name} not found in the dataset")
        
        # rate limiter
        rate_limiter = Limiter(calls_per_second)

        async def generate(example):
            await rate_limiter.wait()
            body = {
                "model_id": model_id,
                "messages": example[conv_prefix_column_name],
                "generation_kwargs": generation_kwargs
            }
            output = await self.send_request('/api/v1/model/inference', "POST", body)
            example['response'] = {'role': 'assistant', 'content': output}
            pbar.update(1)
            return example

        tasks = []
        for idx, row in data.iterrows():
            tasks.append(asyncio.create_task(generate(row)))
        results = await asyncio.gather(*tasks)
        results_df = pd.DataFrame(results)
        return results_df
