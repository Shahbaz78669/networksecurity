from dataclasses import dataclass


@dataclass
class DataIngestionAirtifact:
    trained_file_path:str
    test_file_path:str
    