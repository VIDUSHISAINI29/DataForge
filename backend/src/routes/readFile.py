from fastapi import APIRouter
from src.controllers.readFile import get_list_of_raw_files, get_list_of_transformed_files, get_preview_of_raw_file, get_preview_of_transformed_file


read_file_router = APIRouter()

@read_file_router.get('/read-raw-files-list')
def read_raw_data_endpoint():
    files = get_list_of_raw_files()
    return files    


@read_file_router.get('/read-transformed-files-list')
def read_transformed_data_endpoint():
    files = get_list_of_transformed_files()
    return files    

# @read_file_router.get('/file-preview/{file_name}')
# def preview_endpoint(file_name:str):
#     file = get_preview_of_file(file_name)
#     print(file)
#     return file    

@read_file_router.get("/raw-file-preview/{file_name}")
def raw_preview_endpoint(
    file_name: str,
    limit: int = 10
):
    return get_preview_of_raw_file(
        file_name,
        limit
    )


@read_file_router.get("/transformed-file-preview/{file_name}")
def transformed_preview_endpoint(
    file_name: str,
    limit: int = 10
):
    return get_preview_of_transformed_file(
        file_name,
        limit
    )

@read_file_router.get("/export/{file_name}")
def export_transformed_file(
    file_name: str,
    limit: int = 100
):
    return get_preview_of_transformed_file(
        file_name,
        limit
    )