from ..repository.record_repo import RecordRepository
from ..data.record import Record

class RecordGetter:

    def __init__(self, repository: RecordRepository):
        self.repo = repository

    def get_records(self) -> list:
        return self.repo.get_all()
    
