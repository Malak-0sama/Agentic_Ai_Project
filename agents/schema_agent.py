import pandas as pd

from agents.base_agent import BaseAgent

from utils.column_utils import (
    detect_column_type,
    unique_ratio,
    missing_ratio,
    has_outliers,
    is_identifier,
    is_constant,
    column_memory,
)



class SchemaAgent(BaseAgent):

    def run(self, context):

        file_path = context["file_path"]

        df = pd.read_csv(
            file_path,
            encoding="latin1"
        )

        context["dataframe"] = df

        context["schema"] = self.build_schema(df)

        return context

    def build_schema(self, df):

        schema = {

            "dataset": self.build_dataset_metadata(df),

            "columns": self.build_columns_metadata(df),

            "quality": self.build_quality_metadata(df)

        }

        return schema

        def build_dataset_metadata(self, df):

         return {

            "rows": len(df),

            "columns": len(df.columns),

            "memory_usage_mb": round(

                df.memory_usage(deep=True).sum()

                / (1024 ** 2),

                2

            ),

            "duplicate_rows": int(

                df.duplicated().sum()

            )

        }

        def build_columns_metadata(self, df):

          columns = {}

        for column in df.columns:

            series = df[column]

            semantic_type = detect_column_type(series)

            metadata = {

                "dtype": str(series.dtype),

                "semantic_type": semantic_type,

                "missing_count": int(

                    series.isnull().sum()

                ),

                "missing_ratio": round(

                    missing_ratio(series),

                    4

                ),

                "unique_count": int(

                    series.nunique(dropna=True)

                ),

                "unique_ratio": round(

                    unique_ratio(series),

                    4

                ),

                "memory_bytes": int(

                    series.memory_usage(deep=True)

                ),
            "is_constant": is_constant(series),

           "has_outliers": has_outliers(series),

           "is_identifier": is_identifier(
             column,
             series
),

"memory_bytes": column_memory(series),
            }

            columns[column] = metadata

        return columns

    def build_quality_metadata(self, df):

     total_missing = int(
        df.isnull().sum().sum()
    )

     total_cells = (
        len(df)
        * len(df.columns)
    )

     missing_ratio = (
        total_missing / total_cells
        if total_cells > 0
        else 0
    )

     quality_score = self.calculate_quality_score(df)

     return {

        "missing_cells": total_missing,

        "missing_ratio": round(
            missing_ratio,
            4
        ),

        "duplicate_rows": int(
            df.duplicated().sum()
        ),

        "quality_score": quality_score

    }

    def calculate_quality_score(self, df):

     score = 100

    
     missing_ratio = (
        df.isnull()
        .sum()
        .sum()
        /
        (len(df) * len(df.columns))
    )

     score -= missing_ratio * 40

    
     duplicate_ratio = (
        df.duplicated().sum()
        /
        len(df)
    )

     score -= duplicate_ratio * 30

     constant_columns = 0

     for column in df.columns:

        if is_constant(df[column]):

            constant_columns += 1

     constant_ratio = (
        constant_columns
        /
        len(df.columns)
    )

     score -= constant_ratio * 30

     score = max(0, score)

     return float(
    round(score, 2)
)

    def build_dataset_metadata(self, df):

     return {

        "rows": len(df),

        "columns": len(df.columns),

        "memory_usage_mb": float(
    round(
        df.memory_usage(deep=True).sum()
        / (1024 ** 2),
        2
    )
),



 
        
        "duplicate_rows": int(
            df.duplicated().sum()
        ),

        "numeric_columns": len(
            df.select_dtypes(include="number").columns
        ),

        "categorical_columns": len(
            df.select_dtypes(
                include=["object", "category"]
            ).columns
        ),

        "datetime_columns": len(
            df.select_dtypes(
                include=["datetime64"]
            ).columns
        )

    }


    def build_columns_metadata(self, df):

     columns = {}

     for column in df.columns:

        series = df[column]

        semantic_type = detect_column_type(series)

        metadata = {

            "dtype": str(series.dtype),

            "semantic_type": semantic_type,

            "nullable": bool(
                series.isnull().any()
            ),

            "missing_count": int(
                series.isnull().sum()
            ),

            "missing_ratio": float(
    round(
        missing_ratio(series),
        4
    )
),

            "unique_count": int(
                series.nunique(dropna=True)
            ),

            "unique_ratio": float(
    round(
        unique_ratio(series),
        4
    )
),

            "memory_bytes": column_memory(series),

            "is_constant": is_constant(series),

            "has_outliers": has_outliers(series),

            "is_identifier": is_identifier(
                column,
                series
            ),

            "sample_values": (
    series
    .dropna()
    .sample(
        n=min(5, len(series.dropna())),
        random_state=42
    )
    .astype(str)
    .tolist()
)

        }

        columns[column] = metadata

     return columns