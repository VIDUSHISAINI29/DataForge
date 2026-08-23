from fastapi import HTTPException
from src.services.readFile import list_raw_files, list_transformed_files, get_raw_file_preview, get_transformed_file_preview 

def get_list_of_raw_files():
    try:
        files_list = list_raw_files()
        return files_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
def get_list_of_transformed_files():
    try:
        files_list = list_transformed_files()
        return files_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# def get_preview_of_file(file_name: str):
#     try:
#         file = get_file_preview(file_name)
#         return file
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


def get_preview_of_raw_file(
    file_name: str,
    limit: int = 100
):
    try:
        return get_raw_file_preview(
            file_name,
            limit
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    
def get_preview_of_transformed_file(
    file_name: str,
    limit: int = 100
):
    try:
        return get_transformed_file_preview(
            file_name,
            limit
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

