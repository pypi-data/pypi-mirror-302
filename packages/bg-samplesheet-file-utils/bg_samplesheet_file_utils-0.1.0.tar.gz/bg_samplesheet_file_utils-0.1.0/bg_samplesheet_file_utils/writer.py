import csv
import logging
import os
from datetime import datetime

from singleton_decorator import singleton
from typing import List, Optional

from . import constants
from .record import Record


@singleton
class Writer:
    """Class for writing comma-separated samplesheet file."""

    def __init__(self, **kwargs):
        """Constructor for class Writer."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.outfile = kwargs.get("outfile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", constants.DEFAULT_OUTDIR)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        logging.info(f"Instantiated Writer in {os.path.abspath(__file__)}")

    def write_file(self, records: List[Record], outfile: Optional[str]) -> None:
        """Write the records to the output comma-separated file.

        Args:
            records: List of records.
            outfile (Optional[str]): The path to the output file.
        """
        with open(outfile, 'w') as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## logfile: {self.logfile}\n")

            of.write("R Number,Flowcell,Lane,Test Code,Test,Midpool,Sample,Index ID,Library,Family ID,SLIMS Number\n")
            for record in records:
                line = f"{record.r_number},{record.flowcell},{record.lane},{record.test_code},{record.test}," \
                       f"{record.midpool},{record.sample},{record.index_id},{record.library},{record.family_id}," \
                       f"{record.slims_number}"

                of.write(f"{line}\n")

        logging.info(f"Wrote file '{outfile}'")
        if self.verbose:
            print(f"Wrote file '{outfile}'")

