from pydantic import BaseModel  


class CarModel(BaseModel): 
    plate_number: str
    due_amount: int