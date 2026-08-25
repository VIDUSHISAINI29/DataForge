import os
from pathlib import Path
import io 
import pandas as pd
import duckdb
from fastapi import HTTPException


DATA_ROOT = Path(
    os.getenv("DATA_ROOT", "/app/data")
)

DATA_DIR = DATA_ROOT / "raw"
TRANSFORMED_DIR = DATA_ROOT / "transformed"

DATA_DIR.mkdir(parents=True, exist_ok=True)
TRANSFORMED_DIR.mkdir(parents=True, exist_ok=True)

def list_raw_files():
    """Lists all supported data files in the folder."""
    supported_extensions = (".csv", ".json", ".xlsx", ".xls", ".parquet")
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(supported_extensions)]
    return {"files": files}

def list_transformed_files():
    """Lists all supported data files in the folder."""
    supported_extensions = (".csv", ".json", ".xlsx", ".xls", ".parquet")
    files = [f for f in os.listdir(TRANSFORMED_DATA_DIR) if f.endswith(supported_extensions)]
    return {"files": files}



## Reading Files to show on the frontend


# def fetch_file_from_data_folder(file_name: str):

#     file_path = os.path.join(DATA_DIR, file_name)

#     if not os.path.isfile(file_path):
#         raise HTTPException(
#             status_code=404,
#             detail="File not found"
#         )

#     with open(file_path, "rb") as file:
#         file_bytes = file.read()

#     extension = file_name.rsplit(".", 1)[-1].lower()

#     return file_bytes, extension


# def process_file_to_df(file_bytes: bytes, extension: str) -> pd.DataFrame:
#     try:
#         file_stream = io.BytesIO(file_bytes)
#         if extension == "csv":
#             return pd.read_csv(file_stream)
#         elif extension == "json":
#             return pd.read_json(file_stream)
#         elif extension == "parquet":
#             return pd.read_parquet(file_stream)
#         elif extension == "xls":
#             return pd.read_excel(file_stream)
#         elif extension == "xlsx":
#             return pd.read_excel(file_stream)
#         else:
#             raise HTTPException(status_code=400, detail="Unsupported file format")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to parse file: {str(e)}")


# def get_file_preview(file_name: str):
#     file_bytes, extension = fetch_file_from_data_folder(file_name)
#     df = process_file_to_df(file_bytes, extension)
#     df = df.astype(object).where(pd.notna(df), None)

#     preview_df = df.head(2)

#     preview_df = preview_df.astype(object).where(
#         pd.notna(preview_df),
#         None
#     )
#     return {
#         "columns": list(df.columns),
#         "data": preview_df.to_dict(orient="records")
#     }



# --------------------------------------------------
# Convert DataFrame → JSON Preview
# --------------------------------------------------

def dataframe_to_preview(df: pd.DataFrame):
    """
    Converts a DataFrame into a JSON-safe preview response.
    """

    # Replace NaN / NaT with None
    df = df.astype(object).where(
        pd.notna(df),
        None
    )

    return {
        "columns": list(df.columns),
        "data": df.to_dict(orient="records"),
    }


# --------------------------------------------------
# Parquet Preview
# --------------------------------------------------

def get_parquet_preview(
    file_path: Path,
    limit: int
):
    """
    Reads only the required number of rows
    from a Parquet file using DuckDB.
    """

    query = """
        SELECT *
        FROM read_parquet(?)
        LIMIT ?
    """

    df = duckdb.execute(
        query,
        [str(file_path), limit]
    ).df()

    return dataframe_to_preview(df)


# --------------------------------------------------
# CSV Preview
# --------------------------------------------------

def get_csv_preview(
    file_path: Path,
    limit: int
):
    """
    Reads only the required number of rows
    from a CSV file using DuckDB.
    """

    query = """
        SELECT *
        FROM read_csv_auto(?)
        LIMIT ?
    """

    df = duckdb.execute(
        query,
        [str(file_path), limit]
    ).df()

    return dataframe_to_preview(df)


# --------------------------------------------------
# Excel Preview
# --------------------------------------------------

def get_excel_preview(
    file_path: Path,
    limit: int
):
    """
    Reads only the required number of rows
    from an Excel file.
    """

    df = pd.read_excel(
        file_path,
        nrows=limit
    )

    return dataframe_to_preview(df)


# --------------------------------------------------
# JSON Preview
# --------------------------------------------------

def get_json_preview(
    file_path: Path,
    limit: int
):
    query = """
        SELECT *
        FROM read_json_auto(?)
        LIMIT ?
    """

    df = duckdb.execute(
        query,
        [str(file_path), limit]
    ).df()

    return dataframe_to_preview(df)


# --------------------------------------------------
# Main File Preview
# --------------------------------------------------

def get_raw_file_preview(
    file_name: str,
    limit: int = 100
):
    """
    Returns a preview of the requested file.

    The reader is selected based on the file extension.
    """

    file_path = DATA_DIR / file_name

    # Check file exists
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=400,
            detail="Invalid file"
        )

    extension = file_path.suffix.lower()

    # ------------------------------
    # Parquet
    # ------------------------------

    if extension == ".parquet":
        return get_parquet_preview(
            file_path,
            limit
        )

    # ------------------------------
    # CSV
    # ------------------------------

    elif extension == ".csv":
        return get_csv_preview(
            file_path,
            limit
        )

    # ------------------------------
    # Excel
    # ------------------------------

    elif extension in (".xlsx", ".xls"):
        return get_excel_preview(
            file_path,
            limit
        )

    # ------------------------------
    # JSON
    # ------------------------------

    elif extension == ".json":
        return get_json_preview(
            file_path,
            limit
        )

    # ------------------------------
    # Unsupported
    # ------------------------------

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )




def get_transformed_file_preview(
    file_name: str,
    limit: int = 10
):
    """
    Returns a preview of the requested file.

    The reader is selected based on the file extension.
    """

    file_path = TRANSFORMED_DATA_DIR / file_name

    # Check file exists
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=400,
            detail="Invalid file"
        )

    extension = file_path.suffix.lower()

    # ------------------------------
    # Parquet
    # ------------------------------

    if extension == ".parquet":
        return get_parquet_preview(
            file_path,
            limit
        )

    # ------------------------------
    # CSV
    # ------------------------------

    elif extension == ".csv":
        return get_csv_preview(
            file_path,
            limit
        )

    # ------------------------------
    # Excel
    # ------------------------------

    elif extension in (".xlsx", ".xls"):
        return get_excel_preview(
            file_path,
            limit
        )

    # ------------------------------
    # JSON
    # ------------------------------

    elif extension == ".json":
        return get_json_preview(
            file_path,
            limit
        )

    # ------------------------------
    # Unsupported
    # ------------------------------

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )