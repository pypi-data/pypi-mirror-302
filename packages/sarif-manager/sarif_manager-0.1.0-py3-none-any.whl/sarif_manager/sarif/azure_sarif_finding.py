from sarif_manager.sarif.azure_sarif_utils import trim_uuid


class AzureSarifFinding:
    def __init__(self, repo_url: str, rule_id: str, message: str, severity: str, location: str, line: int, description: str):
        self.repo_url = repo_url
        self.original_rule_id = rule_id
        # Now the rule ID will end up being the same as the message.
        self.rule_id = trim_uuid(rule_id)
        self.message = message
        self.severity = 'warning' if severity == 'warning' else 'error'
        self.location = location
        self.line = line
        self.description = description

    @property
    def file_path(self):
        return self.location.replace('\\', '/')

    @property
    def file_url(self):
        return f"{self.repo_url}?path=/{self.file_path}&version=GBmain&line={self.line + 1}&lineEnd={self.line + 2}&lineStartColumn=1&lineEndColumn=1&lineStyle=plain&_a=contents"

    @property
    def formatted_message(self):
        return f"{self.rule_id} at {self.location}:{self.line} | {self.file_url}"

    @property
    def azure_devops_message(self):
        return f"##vso[task.logissue type={self.severity}]{self.formatted_message}"

    @property
    def exclude(self):
        """Exclude certain findings. Missing HTTP Headers, or findings that don't have lines."""
        if "Missing HTTP Header" in self.message:
            return True
        # Exclude findings that don't have a file path
        if self.file_path == "/":
            return True
        # Exclude findings that don't have a line number. It will be set to 0 or 1 if it's missing.
        if self.line == 0 or self.line is None or self.line == 1:
            return True
        return False

    def __str__(self):
        return self.formatted_message
