from typing import Dict, List

from django.core.exceptions import ValidationError
from django.db import models

from .aggregation import Aggregations
from .filters import add_column_indexes
from .settings import aggregation_settings
from .types import Aggregation, AggregationLimit
from .utils import Aggregator


def get_aggregations(
    queryset: models.QuerySet,
    aggregations: Dict[str, Aggregation],
    group_by: List[str] | str = None,
    order_by: List[str] | str = None,
    limit: AggregationLimit | int = None,
):
    app_aggregations = Aggregations()
    if group_by:
        group_by = [
            field.replace(".", "__")
            for field in (
                group_by.split(",") if isinstance(group_by, str) else group_by
            )
        ]

    if order_by:
        order_by = [
            field.replace(".", "__")
            for field in (
                order_by.split(",") if isinstance(order_by, str) else order_by
            )
        ]

    annotations = {}
    group_indexes = {}
    for name, aggregation in aggregations.copy().items():
        aggregation["name"] = name
        aggregation["field"] = (
            aggregation["field"].replace(".", "__")
            if "field" in aggregation and aggregation["field"]
            else None
        )
        if not aggregation["type"]:
            raise ValidationError({"error": "'aggregation' is required"})

        annotations = {
            **annotations,
            **app_aggregations.get_annotation(
                aggregation=aggregation, queryset=queryset
            ),
        }

        index_by_group = aggregation.get("index_by_group", None)
        if index_by_group:
            index_by_group = index_by_group.replace(".", "__")
            group_indexes[index_by_group] = aggregation["name"]

    if group_indexes:
        queryset = add_column_indexes(
            queryset, annotations=annotations, group_indexes=group_indexes
        )

    limit = (
        (
            limit.copy()
            if isinstance(limit, dict)
            else {
                "limit": limit,
            }
        )
        if limit
        else None
    )
    limit = limit if limit and limit.get("limit", None) else None
    if limit:
        limit["by_group"] = limit.get(
            "by_group", group_by[0] if group_by else None
        ).replace(".", "__")
        limit["by_aggregation"] = limit.get(
            "by_aggregation", list(annotations.keys())[0]
        ).replace(".", "__")
        limit["offset"] = limit.get("offset", None)
        limit["show_other"] = limit.get("show_other", False)
        limit["other_label"] = limit.get(
            "other_label", aggregation_settings["DEFAULT_OTHER_GROUP_NAME"]
        )

    aggregator = Aggregator(queryset=queryset)

    return aggregator.get_database_aggregation(
        annotations=annotations,
        group_by=group_by,
        order_by=order_by,
        limit=limit,
    )
