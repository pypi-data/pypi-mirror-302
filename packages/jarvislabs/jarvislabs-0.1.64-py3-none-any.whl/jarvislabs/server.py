from pydantic import BaseModel, create_model
from fastapi import FastAPI
from jarvislabs import App
from typing import Callable, Any
import uvicorn
import time
import inspect
import asyncio
import json
import os
import aiohttp

class Server:
    def __init__(self, app: App):
        self.app = app
        self.fastapi_app = FastAPI()
        self._setup()
        self._setup_routes()

    def _setup(self):
        if self.app.setup_fn:
            self.app.setup_fn()

    def _setup_routes(self):
        for name, method in self.app.api_endpoints.items():
            print(f"Route name {name}")
            self._create_route(method)
            

    def _create_route(self, method: Callable):
        method_name = method.__name__
        signature = inspect.signature(method)
        parameters = signature.parameters

        # Get the first non-self parameter, which should be the Pydantic BaseModel
        model_param = next((param for name, param in parameters.items() if name != 'self'), None)
        
        if model_param is None or not issubclass(model_param.annotation, BaseModel):
            raise ValueError(f"Method {method_name} must have a Pydantic BaseModel parameter")

        BodyModel = model_param.annotation
        
        # Create a new model with the original BodyModel fields and prediction_id
        import uuid

        # Create a new model with the original BodyModel fields and optional prediction_id
        ExtendedBodyModel = create_model(
            f'Extended{BodyModel.__name__}',
            prediction_id=(str, None),
            **{field: (field_info.annotation, field_info.default) for field, field_info in BodyModel.__fields__.items()}
        )

        @self.fastapi_app.post(f"/{method_name}")
        async def endpoint(body: ExtendedBodyModel):
            # Generate a random prediction_id if not provided
            if body.prediction_id is None:
                body.prediction_id = str(uuid.uuid4())

            # Extract the original BodyModel fields
            original_body = BodyModel(**{k: v for k, v in body.dict().items() if k in BodyModel.__fields__})
            
            # Run the API endpoint as a background task
            asyncio.create_task(self._run_endpoint(method_name, original_body, body.prediction_id))
            
            # Return the prediction_id immediately
            return {"prediction_id": body.prediction_id, "status": "Processing"}

    async def _run_endpoint(self, method_name: str, body: BaseModel, prediction_id: str):
        try:
            start_time = time.time()
            result = await self.app.api_endpoints[method_name](body)
            end_time = time.time()
            response = {"prediction_id": prediction_id, "output": result, "time": end_time - start_time}
            await self.send_to_api(response)
        except Exception as e:
            error_message = f"Error processing request: {str(e)}"
            error_response = {"prediction_id": prediction_id, "error": error_message}
            await self.send_to_api(error_response)

    async def send_to_api(self, response: dict):
        prediction_id = response.get("prediction_id")
        api_url = f"{os.environ.get('SERVERLESS_URL')}/models/prediction/{prediction_id}"
        api_key = os.environ.get("JL_API")
        
        if api_key:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(api_url, json=response, headers=headers) as api_response:
                        api_response.raise_for_status()
                        print(f"Response sent to API endpoint. Status code: {api_response.status}")
            except aiohttp.ClientError as e:
                print(f"Error sending response to API endpoint: {e}")
        else:
            print("JL_API environment variable not found. Skipping API request.")

    def run(self, host: str = "0.0.0.0", port: int = 6006):
        @self.fastapi_app.get("/health")
        async def health():
            return {"success": True}
        uvicorn.run(self.fastapi_app, host=host, port=port)
