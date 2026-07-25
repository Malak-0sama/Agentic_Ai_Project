import pandas as pd

from config.constants import (
    IDENTIFIER_KEYWORDS,
    IDENTIFIER_NAME_SCORE,
    IDENTIFIER_UNIQUE_SCORE,
    IDENTIFIER_STRING_SCORE,
    IDENTIFIER_SCORE_THRESHOLD,
)


def detect_column_type(series: pd.Series):

    """
    Detect the semantic type of a column.
    """

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    if pd.api.types.is_string_dtype(series):

     try:

        converted = pd.to_datetime(
            series.dropna(),
            errors="raise"
        )

        if len(converted) > 0:

            return "datetime"

     except Exception:

        pass    
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_string_dtype(series):

        avg_length = (
            series
            .dropna()
            .astype(str)
            .str.len()
            .mean()
        )

        if avg_length > 50:
            return "text"

        return "categorical"

    return "unknown"

def missing_ratio(series):

    return series.isnull().mean()

def unique_ratio(series):

    return (
        series.nunique(dropna=True)
        /
        len(series)
    )

def has_outliers(series):

    if not pd.api.types.is_numeric_dtype(series):

        return False

    q1 = series.quantile(0.25)

    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr

    upper = q3 + 1.5 * iqr

    return bool(
    (
        (series < lower)
        |
        (series > upper)
    ).any()
)
def is_identifier(
    column_name,
    series
):

    score = 0

    normalized = (
        column_name
        .lower()
        .replace("_", "")
        .replace(" ", "")
    )

    for keyword in IDENTIFIER_KEYWORDS:

        if keyword in normalized:

            score += IDENTIFIER_NAME_SCORE

            break

    
    ratio = unique_ratio(series)

    if ratio >= 0.95:

        score += IDENTIFIER_UNIQUE_SCORE

   
    if (
        detect_column_type(series)
        == "categorical"
        and ratio >= 0.90
    ):

        score += IDENTIFIER_STRING_SCORE

    return score >= IDENTIFIER_SCORE_THRESHOLD


def is_constant(series):

    return series.nunique(dropna=True) <= 1

def column_memory(series):

    return int(
        series.memory_usage(deep=True)
    )

