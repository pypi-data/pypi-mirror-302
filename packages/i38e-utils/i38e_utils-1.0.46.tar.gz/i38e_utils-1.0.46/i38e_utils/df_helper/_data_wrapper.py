
import os
from typing import Type, Any, Dict
from ..log_utils import Logger
import datetime
import time
from tqdm import tqdm

logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')

class DataWrapper:
    DEFAULT_MAX_AGE_MINUTES = 1440
    DEFAULT_HISTORY_DAYS_THRESHOLD = 30

    def __init__(self, dataclass: Type, date_field: str, data_path: str, parquet_filename: str,
                 start_date: Any, end_date: Any, verbose: bool = False, class_params:Dict = None,
                 load_params: Dict = None,
                 reverse_order: bool = False, overwrite: bool = False,
                 max_age_minutes: int = DEFAULT_MAX_AGE_MINUTES,
                 history_days_threshold: int = DEFAULT_HISTORY_DAYS_THRESHOLD,
                 show_progress: bool = False):
        self.dataclass = dataclass
        self.date_field = date_field
        self.data_path = self.ensure_forward_slash(data_path)
        self.parquet_filename = parquet_filename
        self.verbose = verbose
        self.class_params = class_params or {}
        self.load_params = load_params or {}
        self.reverse_order = reverse_order
        self.overwrite = overwrite
        self.max_age_minutes = max_age_minutes
        self.history_days_threshold = history_days_threshold
        self.show_progress = show_progress

        self.start_date = self.convert_to_date(start_date)
        self.end_date = self.convert_to_date(end_date)
        self.remove_empty_directories(self.data_path)

    @staticmethod
    def convert_to_date(date: Any) -> datetime.date:
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d').date() if isinstance(date, str) else date
        except ValueError as e:
            logger.error(f"Error converting {date} to datetime: {e}")
            raise

    @staticmethod
    def ensure_forward_slash(path: str) -> str:
        return path if path.endswith('/') else path + '/'

    @staticmethod
    def ensure_directory_exists(path: str):
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            logger.error(f"Error creating directory {path}: {e}")
            raise

    def generate_date_range(self):
        step = -1 if self.reverse_order else 1
        start, end = (self.end_date, self.start_date) if self.reverse_order else (self.start_date, self.end_date)
        current_date = start
        while current_date != end + datetime.timedelta(days=step):
            yield current_date
            current_date += datetime.timedelta(days=step)

    def process(self):
        date_range = list(self.generate_date_range())
        if self.show_progress:
            date_range = tqdm(date_range, desc="Processing dates", unit="date")

        for current_date in date_range:
            self.process_date(current_date)

    def is_file_older_than(self, file_path: str, current_date: datetime.date) -> bool:
        if not os.path.exists(file_path):
            return True

        if self.overwrite:
            os.remove(file_path)
            return True

        file_modification_date = datetime.date.fromtimestamp(os.path.getmtime(file_path))
        file_age_days = (datetime.date.today() - file_modification_date).days

        if file_age_days <= self.history_days_threshold:
            file_age_seconds = time.time() - os.path.getmtime(file_path)
            if self.verbose:
                logger.info(f"File {file_path} is {round((file_age_seconds / 60), 0)} minutes old")
            return file_age_seconds / 60 > self.max_age_minutes or self.max_age_minutes == 0

        return False

    def process_date(self, date: datetime.date):
        folder = f'{self.data_path}{date.year}/{date.month:02d}/{date.day:02d}/'
        full_parquet_filename = os.path.join(folder, self.parquet_filename)

        start_time = time.time()  # Start timing before processing

        if self.verbose:
            logger.info(f"Processing {full_parquet_filename}...")

        today = datetime.date.today()
        days_difference = (today - date).days

        if days_difference > self.history_days_threshold and not self.overwrite:
            if os.path.exists(full_parquet_filename):
                if self.verbose:
                    logger.info(f"File exists and date is beyond history days threshold without overwrite. Skipping.")
                return
            else:
                if self.verbose:
                    logger.info(
                        f"File does not exist for date beyond history days threshold. Proceeding with generation.")

        if not self.is_file_older_than(full_parquet_filename, date):
            if self.verbose:
                logger.info("File exists and conditions for regeneration are not met. Skipping.")
            return

        data_object = self.dataclass(**self.class_params)
        date_filter_params = {f'{self.date_field}__year': date.year, f'{self.date_field}__month': date.month,
                              f'{self.date_field}__day': date.day}
        df = data_object.load(**self.load_params, **date_filter_params)

        if len(df.index)==0:
            if self.verbose:
                logger.info("No data found for the specified date.")
            return

        # Create directory structure only if df is not empty
        self.ensure_directory_exists(folder)
        df.to_parquet(full_parquet_filename)

        end_time = time.time()  # End timing after processing
        duration_seconds = end_time - start_time  # Calculate duration

        if self.verbose:
            logger.info(f"Data saved to {full_parquet_filename}. Processing time: {duration_seconds:.2f} seconds")
        self.remove_empty_directories(os.path.dirname(folder))

    def remove_empty_directories(self, path: str):
        if not os.path.isdir(path) or os.path.realpath(path) == os.path.realpath(self.data_path):
            return

        if not os.listdir(path):
            try:
                os.rmdir(path)
                if self.verbose:
                    logger.info(f"Removed empty directory: {path}")
                self.remove_empty_directories(os.path.dirname(path))
            except OSError as e:
                if self.verbose:
                    logger.error(f"Error removing directory {path}: {e}")
        else:
            if self.verbose:
                logger.info(f"Directory not empty, stopping: {path}")


# Usage:
# wrapper = DataWrapper(dataclass=YourDataClass, date_field="created_at", data_path="/path/to/data", parquet_filename="data.parquet", start_date="2022-01-01", end_date="2022-12-31")
# wrapper.process()

