from ..repository.record_repo import RecordRepository
from ..data.record import Record

class RecordCreator:

    def __init__(self, repository: RecordRepository):
        self.repo = repository

    def insert_record(self, record : Record) -> int:
        return self.repo.insert(record)
