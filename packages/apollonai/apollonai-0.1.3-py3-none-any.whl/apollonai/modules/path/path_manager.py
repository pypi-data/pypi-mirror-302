from pathlib import Path

class PathManager:
    """
    Manages paths for imports and exports in the data pipeline, with mode and step management.
    """
    def __init__(self, base_dir: Path, mode: str = 'local', step_name: str = '', sub_dir: str = ''):
        """
        Initializes the PathManager with a base directory, mode (e.g., local/cloud),
        step name (e.g., data_retrieving), and optional sub-directory (e.g., Images).
        
        Args:
            base_dir (Path): The base directory for the pipeline.
            mode (str): The mode of operation (default is 'local'). Can be 'local', 'cloud', etc.
            step_name (str): The current pipeline step (e.g., 'data_retrieving').
            sub_dir (str): Optional sub-directory for exports (e.g., 'Images').
        """
        self.base_dir = base_dir.resolve()  # Ensure base_dir is a Path object
        self.mode = mode
        self.step_name = step_name
        self.sub_dir = sub_dir

        # Create necessary directories based on mode and step
        self.setup_directories()

    def setup_directories(self):
        """
        Sets up the directories based on the mode, step name, and sub-directory.
        """
        if self.mode == 'local':
            self.import_dir = self.base_dir / 'imports'
            self.export_dir = self.base_dir / 'exports' / self.step_name
            self.export_sub_dir = self.export_dir / self.sub_dir if self.sub_dir else None

            # Create directories if they don't exist
            self.import_dir.mkdir(parents=True, exist_ok=True)
            self.export_dir.mkdir(parents=True, exist_ok=True)
            if self.export_sub_dir:
                self.export_sub_dir.mkdir(parents=True, exist_ok=True)
        
        # You can extend the logic for other modes (e.g., 'cloud') if needed.

    def get_import_directory(self) -> Path:
        """
        Returns the path to the import directory.
        """
        return self.import_dir

    def get_export_directory(self) -> Path:
        """
        Returns the path to the export directory for the current step.
        """
        return self.export_dir

    def get_export_subdirectory(self) -> Path:
        """
        Returns the path to the export sub-directory for the current step.
        """
        return self.export_sub_dir if self.sub_dir else self.export_dir

    def get_export_file_path(self, file_name: str) -> Path:
        """
        Returns the path for a file to be exported to the current step's directory.
        
        Args:
            file_name (str): Name of the file to be exported.
        
        Returns:
            Path: Full path to the export file.
        """
        return self.get_export_subdirectory() / file_name
