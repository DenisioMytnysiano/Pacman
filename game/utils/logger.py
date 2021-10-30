import csv
from pathlib import Path
from dataclasses import dataclass


@dataclass(eq=False)
class Logger:
    log_path: Path = "records.csv"
    delimiter: str = ","
    mode: str = "a"

    def save(self, result) -> None:
        with open(self.log_path, mode=self.mode) as log_file:
            writer = csv.DictWriter(
                log_file, fieldnames=result.keys(), delimiter=self.delimiter
            )
            writer.writerow(result)
