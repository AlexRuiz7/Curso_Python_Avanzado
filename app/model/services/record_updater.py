from ..repository.record_repo import RecordRepository
from ..data.record import Record

class RecordUpdater:

    def __init__(self, repository: RecordRepository):
        self.repo = repository

    def update_record(self, record: Record) -> bool:      
        return self.repo.update(record)
