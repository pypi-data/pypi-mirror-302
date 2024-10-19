"""
Script to generate a sharepoint-copyable metadata file
from the Exaspim Mouse Tracker Spreadsheet
"""

import csv
from typing import List, Union

import pandas as pd

from aind_smartsheet_api.client import SmartsheetClient, SmartsheetSettings

from aind_msma_utils.exaspim.models import JobSettings

single_sub_raw_headings = [
    "nROID#",
    "roVol#",
    "roSub#a",
    "roLot#a",
    "roGC#a",
    "roVolV#a",
    "roTite#a",
    "roSub#b",
    "roLot#b",
    "roGC#b",
    "roVolV#b",
    "roTite#b",
    "roSub#c",
    "roLot#c",
    "roGC#c",
    "roVolV#c",
    "roTite#c",
    "roSub#d",
    "roLot#d",
    "roGC#d",
    "roVolV#d",
    "roTite#d",
    "roTube#",
    "roBox#",
]

relevant_sub_headings = [
    "nROID#",
    "roVol#",
]

relevant_inj_headings = [
    "roSub#*",
    "roLot#*",
    "roGC#*",
    "roTite#*",
]

headings_map = {
    "nROID#": "Mouse ID",
    "roVol#": "Virus Mix Total Volume injected RO (uL)",
    "roSub#*": "Virus*",
    "roLot#*": "Virus* ID",
    "roGC#*": "Virus* Dose (GC)",
    "roTite#*": "Virus* Effective Titer (GC/mL)",
}

subheadings_map = {
    "a": "1",
    "b": "2",
    "c": "3",
}


def replace_number(str, idx):
    """Replace the # character with the index number"""
    return str.replace("#", f"{idx}")


def replace_letter(str, letter):
    """Replace the * character with the counting letter"""
    return str.replace("*", f"{letter}")


def replace_heading_counters(str, idx, letter):
    """
    Replace the # and * characters with the index number and counting letter
    """
    return replace_letter(replace_number(str, idx), letter)


class SharePointGenerator:
    """
    Class to generate sharepoint metadata file
    from Exaspim Mouse Tracker Spreadsheet
    """

    def __init__(self, job_settings: Union[JobSettings, str]):
        """
        Class constructor for Base etl class.
        Parameters
        ----------
        job_settings: Union[JobSettings, str]
          Variables for a particular session
        """

        if isinstance(job_settings, str):
            self.job_settings = JobSettings.model_validate_json(job_settings)
        else:
            self.job_settings = job_settings

        self.smartsheet_settings = SmartsheetSettings(
            access_token=self.job_settings.smartsheet_token,
        )

    def run_job(self):
        """Run the ETL job"""

        self._extract()

        transformed_data = []
        for idx, subj_id in enumerate(self.job_settings.subjects_to_ingest):
            transformed_data.append(
                self._transform(self._extract(), subj_id, idx + 1)
            )

        combined_data = self._combine(transformed_data)

        return self._load(combined_data)

    def _extract(self):
        """Extract the input spreadsheet"""

        smartsheet_client = SmartsheetClient(self.smartsheet_settings)
        sheet = smartsheet_client.get_parsed_sheet(
            sheet_id=self.job_settings.smartsheet_sheet_id
        )

        df = pd.DataFrame.from_dict(sheet, orient="columns")
        return df

    def _transform(self, materials_sheet, subj_id, subj_idx):
        """Extract data from the input spreadsheet"""

        subj_row = materials_sheet.loc[
            materials_sheet["Mouse ID"] == int(subj_id)
        ]

        output = {}

        for header in relevant_sub_headings:
            input_sheet_header = replace_number(headings_map[header], subj_idx)
            output[replace_number(header, subj_idx)] = subj_row[
                input_sheet_header
            ].values[0]

        for letter, inj_num in subheadings_map.items():
            for header in relevant_inj_headings:
                input_sheet_header = replace_heading_counters(
                    headings_map[header], subj_idx, inj_num
                )
                output_header = replace_heading_counters(
                    header, subj_idx, letter
                )

                output[output_header] = subj_row[input_sheet_header].values[0]

        output_expanded = {}
        for header in self.generate_curr_subj_headings(subj_idx):
            if header in output.keys():
                output_expanded[header] = output[header]
            else:
                output_expanded[header] = None
        return output_expanded

    @staticmethod
    def _combine(transformed_data: List):
        """Combine the transformed data into a single dictionary"""

        combined = {}
        for data in transformed_data:
            for key, value in data.items():
                combined[key] = value
        return combined

    def _load(self, transformed_data):
        """Load the transformed data to a sharepoint metadata file"""
        """
        Will write to an output directory if an output_directory is not None.
        If output_directory is None, then the model will be returned as json
        in the JobResponse object.
        Parameters
        ----------
        input_model : dict
          all data necessary to produce the final spreadsheet.

        Returns
        -------
        saved_model : csv
          The final spreadsheet that has been constructed,
          saved to output_directory
        """

        if self.job_settings.output_spreadsheet_path is None:
            return transformed_data

        with open(
            self.job_settings.output_spreadsheet_path, "w", newline=""
        ) as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=transformed_data.keys(), dialect="excel"
            )
            writer.writeheader()
            writer.writerow(transformed_data)

    @staticmethod
    def generate_curr_subj_headings(subj_idx):
        """Generate headings for the current subject"""
        headings = []
        for heading in single_sub_raw_headings:
            headings.append(replace_number(heading, subj_idx))
        return headings

    def generate_headings(self):
        """Generate sharepoint metadata file"""

        headings = []

        for idx, subj_id in enumerate(self.job_settings.subjects_to_ingest):
            new_headings = [
                heading.replace("#", f"{idx+1}")
                for heading in single_sub_raw_headings
            ]
            headings.extend(new_headings)

        return headings
