"""file to hold models"""
from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings


class JobSettings(BaseSettings):
    """Class to hold job settings"""

    smartsheet_token: str
    smartsheet_sheet_id: str
    output_spreadsheet_path: Optional[Path] = None
    subjects_to_ingest: List[str]
