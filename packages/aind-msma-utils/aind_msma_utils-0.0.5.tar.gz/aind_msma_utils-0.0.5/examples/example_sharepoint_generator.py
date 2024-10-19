"""SharePointGenerator usage example"""

from pathlib import Path
import os

from aind_msma_utils.exaspim.sharepoint_generator import (
    JobSettings,
    SharePointGenerator,
)

if __name__ == "__main__":

    # Set up a JobSettings object with the relevant user-input data
    # See testing resources for the example input spreadsheet
    settings = JobSettings(
        smartsheet_token="your_smartsheet_token_here",
        smartsheet_sheet_id="your_smartsheet_sheet_id_here",
        subjects_to_ingest=[
            "717442",
            "717443",
            "717444",
        ],
        output_spreadsheet_path=Path(
            os.path.join(
                os.path.dirname(__file__),
                "output_sharepoint_metadata.xlsx",
            )
        ),
    )

    # Create a SharePointGenerator object with the JobSettings object
    ingest = SharePointGenerator(settings)

    # Create the output spreadsheet at the intended location
    ingest.run_job()
