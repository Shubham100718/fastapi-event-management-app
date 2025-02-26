import csv
from typing import List
from io import StringIO
from fastapi import HTTPException, status, UploadFile

    
async def process_csv(upload_file: UploadFile) -> List[int]:
    # Validate file type
    if not upload_file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a CSV file."
        )
    try:
        # Read and process the CSV file
        content = await upload_file.read()
        csv_data = StringIO(content.decode("utf-8"))
        reader = csv.reader(csv_data)
        attendee_ids = [int(row[0]) for row in reader if row]
        return attendee_ids
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing CSV file: {str(err)}"
        )

