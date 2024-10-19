from typing import Optional, Dict

import logging


class PrometheusQueryBuilder:
    def __init__(self, verbose=False):
        self.metric_name = None
        self.match_exact_labels = {}
        self.match_regex_labels = {}
        self.exclude_exact_labels = {}
        self.exclude_regex_labels = {}
        self.query_range = None
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)

    def set_metric(self, metric_name):
        self.metric_name = metric_name
        return self

    def add_exact_label(self, label, value):
        self.match_exact_labels[label] = value
        return self

    def add_regex_label(self, label, value):
        self.match_regex_labels[label] = value
        return self

    def exclude_exact_label(self, label, value):
        self.exclude_exact_labels[label] = value
        return self

    def exclude_regex_label(self, label, value):
        self.exclude_regex_labels[label] = value
        return self

    def set_time_range(self, start_time, end_time):
        self.query_range = (start_time, end_time)
        return self

    def reset(self):
        self.metric_name = None
        self.match_exact_labels = {}
        self.match_regex_labels = {}
        self.exclude_exact_labels = {}
        self.exclude_regex_labels = {}
        self.query_range = None
        return self

    def build(self):
        if not self.metric_name:
            raise ValueError("Metric name must be specified")

        query = self.parse_base_query()
        self.reset()
        return query

    def parse_base_query(self) -> str:
        """
        Parse the base query for a given metric, including exact matches, regex matches, and exclusions.
        Returns:
            str: The constructed base query string.

        Raises:
            ValueError: If metric_name is empty or all label dicts are empty.
        """
        label_clauses = []

        if self.match_exact_labels:
            for label, value in self.match_exact_labels.items():
                label_clauses.append(f'{label}="{value}"')

        if self.match_regex_labels:
            for label, value in self.match_regex_labels.items():
                label_clauses.append(f'{label}=~"{value}"')

        if self.exclude_exact_labels:
            for label, value in self.exclude_exact_labels.items():
                label_clauses.append(f'{label}!="{value}"')

        if self.exclude_regex_labels:
            for label, value in self.exclude_regex_labels.items():
                label_clauses.append(f'{label}!~"{value}"')

        # If there are no label clauses, raise an error or return the metric alone
        if not label_clauses:
            # logging.warning(f"No labels provided for metric '{self.metric_name}'. Returning metric name only.")
            return self.metric_name  # or raise ValueError("At least one label must be provided")

        label_clause_str = ', '.join(label_clauses)
        return f'{self.metric_name}{{{label_clause_str}}}'
