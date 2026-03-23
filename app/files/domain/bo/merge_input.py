from pydantic import BaseModel


class MergeInput(BaseModel):
    file_id_1: int
    file_id_2: int
    merged_filename: str
