from fastapi import FastAPI

from model import create_model
from predict import predict
from rest.dto.TrainModelRequestDto import TrainModelRequestDto

app = FastAPI()


@app.post("/v1/train")
async def train_model(request: TrainModelRequestDto):
    create_model(request.courseId, request.schoolYear, request.gradeItemPosition)


@app.get("/v1/predict")
async def get_prediction(course_id, school_year, grade_item_position, student_id):
    return {"prediction": predict(course_id, school_year, grade_item_position, student_id)}
