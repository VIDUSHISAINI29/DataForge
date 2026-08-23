from pydantic import BaseModel
import os
import traceback
from pathlib import Path
import io 
import pandas as pd
import duckdb
from fastapi import HTTPException
from src.services.readFile import dataframe_to_preview

ROOT = Path(__file__).resolve().parent.parent.parent

DATA_DIR = ROOT / "data" / "raw" 
TRANSFORMED_DIR = ROOT / "data" / "transformed"

TRANSFORMED_DIR.mkdir(parents=True, exist_ok=True)


def get_reader(file_path: Path):

    extension = file_path.suffix.lower()

    if extension == ".parquet":
        return f"read_parquet('{file_path}')"

    elif extension == ".csv":
        return f"read_csv_auto('{file_path}')"

    elif extension == ".json":
        return f"read_json_auto('{file_path}')"

    elif extension in [".xlsx", ".xls"]:
        return f"read_xlsx('{file_path}')"

    raise HTTPException(
        status_code=400,
        detail="Unsupported file format"
    )


def execute_sql_query_for_raw_file(
    file_name: str,
    query: str
):
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    reader = get_reader(file_path)

    connection = duckdb.connect()

    try:
        connection.execute(
            f"""
            CREATE TABLE data AS
            SELECT *
            FROM {reader}
            """
        )

        query_type = query.strip().split()[0].upper()

        if query_type == "SELECT":

            df = connection.sql(query).limit(10).df()

        else:

            connection.execute(query)

            df = connection.sql(
            "SELECT * FROM data LIMIT 10"
            ).df()

        return {
            "message": "File transformed successfully",
            "result": dataframe_to_preview(df)
        }
    except Exception as e:
        print("🔥 DUCKDB ERROR:", repr(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=f"Query failed: {str(e)}"
        )

    finally:
        connection.close()




def execute_sql_query_for_transformed_file(
    file_name: str,
    query: str
):
    file_path = TRANSFORMED_DIR / file_name

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    reader = get_reader(file_path)

    connection = duckdb.connect()

    try:
        connection.execute(
            f"""
            CREATE TABLE data AS
            SELECT *
            FROM {reader}
            """
        )

        # Execute query
        result = connection.sql(query)

        # Only fetch rows needed for frontend preview
        df = result.limit(10).df()

        return {
            "message": "Transformed file queried successfully",
            "result": dataframe_to_preview(df)
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Query failed: {str(e)}"
        )

    finally:
        connection.close()




def transform_file(
    file_name: str,
    query: str
):
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    reader = get_reader(file_path)

    output_path = (
        TRANSFORMED_DIR /
        f"{file_path.stem}_transformed.parquet"
    )

    connection = duckdb.connect()

    try:
        connection.execute(
            f"""
            CREATE TABLE data AS
            SELECT *
            FROM {reader}
            """
        )

        # Modify the DuckDB table
        connection.execute(query)

        # Save transformed table
        connection.execute(
            f"""
            COPY data
            TO '{output_path}'
            (FORMAT PARQUET)
            """
        )

        return {
            "message": "File transformed successfully",
            "file_name": output_path.name,
            "path": str(output_path)
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Transformation failed: {str(e)}"
        )

    finally:
        connection.close()