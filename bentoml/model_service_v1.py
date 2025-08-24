import bentoml
from bentoml.io import JSON
from pydantic import BaseModel

# Load model and create runner
model_runner = bentoml.sklearn.get("house_price_model:latest").to_runner()

# Define service with runner
svc = bentoml.Service("house_price_predictor", runners=[model_runner])

# Define input model
class HouseInput(BaseModel):
    square_footage: float
    num_rooms: int

# Define prediction endpoint
@svc.api(input=JSON(pydantic_model=HouseInput), output=JSON())
async def predict(input_data: HouseInput):
    df = [[input_data.square_footage, input_data.num_rooms]]
    prediction = await model_runner.predict.async_run(df)
    return {"price": prediction[0]}
