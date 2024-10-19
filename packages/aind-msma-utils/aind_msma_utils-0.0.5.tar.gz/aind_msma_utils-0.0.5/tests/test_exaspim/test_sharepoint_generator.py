"""Test the methods in the SharepointGenerator class."""

import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

import pandas as pd

from aind_msma_utils.exaspim.models import JobSettings
from aind_msma_utils.exaspim.sharepoint_generator import SharePointGenerator

RESOURCES_DIR = Path(__file__).parent.parent / "resources" / "exaspim"

INPUT_SPREADSHEET_PATH = RESOURCES_DIR / "mouse_tracker_example.xlsx"
EXAMPLE_TRANSFORM_PATH = RESOURCES_DIR / "example_transformed_output.json"
EXAMPLE_COMBINE_PATH = RESOURCES_DIR / "example_combined_output.json"
INPUT_SMARTSHEET_DF_PATH = RESOURCES_DIR / "example_smartsheet.xlsx"


class TestSharePointGenerator(unittest.TestCase):
    """Test the SharePointGenerator class"""

    @classmethod
    def setUpClass(cls):
        """Set up the test class"""

        with open(EXAMPLE_COMBINE_PATH, "r") as f:
            expected_combine = json.load(f)

        with open(EXAMPLE_TRANSFORM_PATH, "r") as f:
            expected_transform = json.load(f)

        cls.expected_smartsheet_df = pd.read_excel(INPUT_SMARTSHEET_DF_PATH)

        cls.expected_combine = expected_combine
        cls.expected_transform = expected_transform

        cls.job_settings = JobSettings(
            smartsheet_sheet_id="12345",
            smartsheet_token="fake_token",
            output_spreadsheet_path="output_spreadsheet_path.csv",
            subjects_to_ingest=[
                "717442",
                "717443",
                "717444",
            ],
        )

    def test_constructor_from_string(self):
        """Construct a job settings model from a string"""

        job_settings_string = self.job_settings.model_dump_json()

        etl0 = SharePointGenerator(self.job_settings)
        etl1 = SharePointGenerator(job_settings_string)

        self.assertEqual(etl1.job_settings, etl0.job_settings)

    @patch("aind_smartsheet_api.client.SmartsheetClient.get_parsed_sheet")
    def test_extract(
        self, mock_get_sheet: MagicMock
    ):
        """Tests the extract method"""
        generator = SharePointGenerator(job_settings=self.job_settings)

        mock_get_sheet.return_value = self.expected_smartsheet_df

        extracted = generator._extract()
        self.assertIsNotNone(extracted)

    def test_transform(self):
        """Tests the transform method"""
        generator = SharePointGenerator(job_settings=self.job_settings)
        extracted = self.expected_smartsheet_df
        transformed = generator._transform(extracted, "717442", 1)

        expected_transform = self.expected_transform

        transformed_string = json.dumps(transformed)
        expected_transformed_string = json.dumps(expected_transform)

        self.assertEqual(transformed_string, expected_transformed_string)

    def test_combine(self):
        """Tests the combine method"""
        generator = SharePointGenerator(job_settings=self.job_settings)
        extracted = self.expected_smartsheet_df
        transformed = []
        for idx, subj_id in enumerate(self.job_settings.subjects_to_ingest):
            transformed.append(
                generator._transform(extracted, subj_id, idx + 1)
            )

        combined = generator._combine(transformed)

        expected_combine = self.expected_combine

        combined_string = json.dumps(combined)
        expected_combine_string = json.dumps(expected_combine)

        self.assertEqual(combined_string, expected_combine_string)

    @patch("builtins.open", new_callable=mock_open)
    def test_load(self, mock_file: MagicMock):
        """Tests the load method"""
        generator = SharePointGenerator(job_settings=self.job_settings)

        combined = self.expected_combine

        generator._load(combined)

        mock_file.assert_has_calls(
            [call(Path("output_spreadsheet_path.csv"), "w", newline="")]
        )

    def test_generate_curr_subj_headings(self):
        """Tests the generate_curr_subj_headings method"""
        generator = SharePointGenerator(job_settings=self.job_settings)
        generated_headings = generator.generate_curr_subj_headings(1)
        expected_headings = [
            "nROID1",
            "roVol1",
            "roSub1a",
            "roLot1a",
            "roGC1a",
            "roVolV1a",
            "roTite1a",
            "roSub1b",
            "roLot1b",
            "roGC1b",
            "roVolV1b",
            "roTite1b",
            "roSub1c",
            "roLot1c",
            "roGC1c",
            "roVolV1c",
            "roTite1c",
            "roSub1d",
            "roLot1d",
            "roGC1d",
            "roVolV1d",
            "roTite1d",
            "roTube1",
            "roBox1",
        ]

        self.assertEqual(generated_headings, expected_headings)

    def test_generate_headings(self):
        """Tests the generate_headings method"""
        generator = SharePointGenerator(job_settings=self.job_settings)
        generated_headings = generator.generate_headings()

        expected_headings = [
            "nROID1",
            "roVol1",
            "roSub1a",
            "roLot1a",
            "roGC1a",
            "roVolV1a",
            "roTite1a",
            "roSub1b",
            "roLot1b",
            "roGC1b",
            "roVolV1b",
            "roTite1b",
            "roSub1c",
            "roLot1c",
            "roGC1c",
            "roVolV1c",
            "roTite1c",
            "roSub1d",
            "roLot1d",
            "roGC1d",
            "roVolV1d",
            "roTite1d",
            "roTube1",
            "roBox1",
            "nROID2",
            "roVol2",
            "roSub2a",
            "roLot2a",
            "roGC2a",
            "roVolV2a",
            "roTite2a",
            "roSub2b",
            "roLot2b",
            "roGC2b",
            "roVolV2b",
            "roTite2b",
            "roSub2c",
            "roLot2c",
            "roGC2c",
            "roVolV2c",
            "roTite2c",
            "roSub2d",
            "roLot2d",
            "roGC2d",
            "roVolV2d",
            "roTite2d",
            "roTube2",
            "roBox2",
            "nROID3",
            "roVol3",
            "roSub3a",
            "roLot3a",
            "roGC3a",
            "roVolV3a",
            "roTite3a",
            "roSub3b",
            "roLot3b",
            "roGC3b",
            "roVolV3b",
            "roTite3b",
            "roSub3c",
            "roLot3c",
            "roGC3c",
            "roVolV3c",
            "roTite3c",
            "roSub3d",
            "roLot3d",
            "roGC3d",
            "roVolV3d",
            "roTite3d",
            "roTube3",
            "roBox3",
        ]

        self.assertEqual(generated_headings, expected_headings)

    @patch(
        "aind_msma_utils.exaspim.sharepoint_generator.SharePointGenerator"
        "._load"
    )
    @patch(
        "aind_msma_utils.exaspim.sharepoint_generator.SharePointGenerator"
        "._extract"
    )
    def test_run_job(self, mock_extract: MagicMock, mock_load: MagicMock):
        """Tests the run_job method"""
        generator = SharePointGenerator(job_settings=self.job_settings)
        mock_extract.return_value = self.expected_smartsheet_df
        generator.run_job()

        mock_load.assert_called_once()

    @patch(
        "aind_msma_utils.exaspim.sharepoint_generator.SharePointGenerator"
        "._extract"
    )
    def test_no_output_path(self, mock_extract: MagicMock):
        """Test output with no path"""
        example_job_settings = JobSettings(
            smartsheet_token=self.job_settings.smartsheet_token,
            smartsheet_sheet_id=self.job_settings.smartsheet_sheet_id,
            subjects_to_ingest=self.job_settings.subjects_to_ingest,
        )

        etl = SharePointGenerator(job_settings=example_job_settings)

        mock_extract.return_value = self.expected_smartsheet_df

        transformed = etl.run_job()

        expected_combine = self.expected_combine

        combined_string = json.dumps(transformed)
        expected_combine_string = json.dumps(expected_combine)

        self.assertEqual(combined_string, expected_combine_string)


if __name__ == "__main__":
    unittest.main()
