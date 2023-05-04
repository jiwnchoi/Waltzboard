@dataclass
class ColumbusConfig:
    max_attributes: int = 3
    max_categories: int = 10
    max_filters: int = 1
    min_rows: int = 4

    def to_dict(self):
        return {
            "max_attributes": self.max_attributes,
            "max_categories": self.max_categories,
            "max_filters": self.max_filters,
            "min_rows": self.min_rows,
        }
