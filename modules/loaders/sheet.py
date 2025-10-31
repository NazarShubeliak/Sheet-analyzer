from pathlib import Path
from typing import Dict, List, Optional

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config.config import GOOGLE_CREDENTIALS_PATH, logger


class SheetLoader:
    """
    SheetLoader handles authorization and data retrieval from a Google Spreadsheet.

    Usage:
        loader = SheetLoader(sheet_name="FinanceData")
        loader.select_worksheet("2025")
        data = loader.load_data()

    Attributes:
        creds_path (Path): Path to service account credentials JSON
        client (gspread.Client): Authorized gspread client
        sheet (gspread.Spreadsheet): Opened spreadsheet object
        worksheet (Optional[gspread.Worksheet]): Selected worksheet tab
    """

    def __init__(self, sheet_name: str, creds_path: Path) -> None:
        """
        Initialize SheetLoader with sheet name and optional credentials path.

        Args:
            sheet_name (str): Name of the Google Spreadsheet
            creds_path (Optional[Path]): Path to credentials JSON file. Defaults to config value.
        """
        self.creds_path = creds_path or GOOGLE_CREDENTIALS_PATH
        self.client = self.__authorize()
        self.sheet = self.__open_sheet(sheet_name)
        self.worksheet: Optional[gspread.Worksheet] = None

    def __authorize(self) -> gspread.Client:
        """
        Authorize access to Google Sheets using service account credentials.

        Returns:
            gspread.Client: Authorized client for accessing spreadsheets
        """
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            str(self.creds_path), scope
        )
        logger.debug("Authorization complete")
        return gspread.authorize(creds)

    def __open_sheet(self, sheet_name: str) -> gspread.Spreadsheet:
        """
        Open a Google Spreadsheet by name.

        Args:
            sheet_name (str): Name of the spreadsheet

        Returns:
            gspread.Spreadsheet: Opened spreadsheet object

        Raises:
            Exception: If the sheet cannot be opened
        """
        try:
            sheet = self.client.open(sheet_name)
            logger.info(f"Opened sheet: {sheet_name}")
            return sheet
        except Exception as e:
            logger.error(f"Failed to open sheet '{sheet_name}': {e}")
            raise

    def select_worksheet(self, worksheet_name: str) -> None:
        """
        Select a worksheet tab within the opened spreadsheet.

        Args:
            worksheet_name (str): Name of the worksheet/tab to select

        Raises:
            Exception: If the worksheet cannot be found
        """
        try:
            self.worksheet = self.sheet.worksheet(worksheet_name)
            logger.info(f"Selected worksheet: {worksheet_name}")
        except Exception as e:
            logger.error(f"Failed to select worksheet '{worksheet_name}': {e}")
            raise

    def load_data(self) -> List[Dict[str, str]]:
        """
        Load all records from the selected worksheet.

        Returns:
            List[Dict[str, str]]: List of row dictionaries with column headers as keys

        Raises:
            ValueError: If worksheet is not selected
            Exception: If data retrieval fails
        """
        if not self.worksheet:
            logger.error("Worksheet not selected")
            raise ValueError("Worksheet must be selected before loading data")

        try:
            records = self.worksheet.get_all_records()
            logger.debug(f"Loaded {len(records)} rows from worksheet")
            return records
        except Exception as e:
            logger.error(f"Error loading data from worksheet: {e}")
            raise
