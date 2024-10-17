import csv
import logging
import os

from singleton_decorator import singleton
from typing import List, Optional

from . import constants
from .file_utils import check_infile_status
from .record import Record


@singleton
class Parser:
    """Class for parsing comma-separated samplesheet file."""

    def __init__(self, **kwargs):
        """Constructor for class Parser"""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.infile = kwargs.get("infile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", constants.DEFAULT_OUTDIR)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self._is_parsed = False
        self._records = []

        logging.info(f"Instantiated Parser in {os.path.abspath(__file__)}")

    def get_records(self, infile: Optional[str]) -> List[Record]:
        """Get the records.

        Args:
            infile (Optional[str]): The path to the file.

        Returns:
            List[Record]: List of records.
        """
        if not self._is_parsed:
            self._parse_file(infile)
        return self._records

    def _parse_file(self, infile: Optional[str]) -> None:
        """Parse the comma-separated samplesheet file.

        Args:
            infile (Optional[str]): The path to the file.
        """
        if infile is None:
            infile = self.infile

        check_infile_status(infile)

        logging.info(f"Will parse the comma-separated samplesheet file '{infile}'")

        with open(infile, mode='r', newline='') as f:
            reader = csv.reader(f)
            line_ctr = 0
            for row in reader:
                line_ctr += 1
                if line_ctr == 1:
                    continue
                record = Record(
                    r_number=row[0],
                    flowcell=row[1],
                    lane=row[2],
                    test_code=row[3],
                    test=row[4],
                    midpool=row[5],
                    sample=row[6],
                    index_id=row[7],
                    library=row[8],
                    family_id=row[9],
                    slims_number=row[10],

                )
                self._records.append(record)

            logging.info(f"Processed '{line_ctr}' lines in the file '{infile}'")

