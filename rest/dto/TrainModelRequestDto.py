from pydantic import BaseModel


class TrainModelRequestDto(BaseModel):
    courseId: str
    schoolYear: str
    gradeItemPosition: str
