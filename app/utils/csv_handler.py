import csv
from typing import List
from io import StringIO
from fastapi import HTTPException, status


async def process_csv(file) -> List[int]:
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a CSV file."
        )
    try:
        # Read and process the CSV file
        content = await file.read()
        csv_data = StringIO(content.decode("utf-8"))
        reader = csv.reader(csv_data)
        attendee_ids = [int(row[0]) for row in reader if row]
        return attendee_ids
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing CSV file: {str(e)}"
        )
    
