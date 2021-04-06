"""Module where all app routes(urls) will be listed"""
import cloudinary.uploader

from fastapi import UploadFile, File, APIRouter
from starlette.requests import Request

from src.api.db import photo

router = APIRouter()


@router.get("/health")
def health_check():
    """Method that is checking if server is running and return Telegram User Info"""
    return {"Message": "Active!", "status": 200}


@router.post("/upload_file")
async def add_photo(request: Request, image: UploadFile = File(...)):
    """
    Method that is receiving a photo from the client and adding it to an external cloud
    @param request:
    @param image:
    @return:
    """
    result = cloudinary.uploader.upload(image.file)
    query = photo.insert().values(name=image.filename, description="description", image=result.get("url"))
    record_id = await request.state.db.execute(query)
    return {"id": record_id}
