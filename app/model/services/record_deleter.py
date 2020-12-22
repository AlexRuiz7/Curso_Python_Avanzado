from ..repository.record_repo import RecordRepository
from ..data.record import Record

class RecordDeleter:

    def __init__(self, repository: RecordRepository):
        self.repo = repository

    def delete_record(self, record: Record) -> bool:
        return self.repo.delete(record)
