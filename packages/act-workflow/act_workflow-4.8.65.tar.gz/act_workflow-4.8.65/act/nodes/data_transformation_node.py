import json
import logging
from typing import Dict, Any, List, Union
import asyncio 
from e2b import Sandbox
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataTransformationNode:
    def __init__(self):
        self.sandbox = None
        self.execution_manager = None

    def set_execution_manager(self, execution_manager):
        self.execution_manager = execution_manager

    async def initialize(self):
        logger.info("Initializing DataTransformationNode")
        self.sandbox = Sandbox()
        # No need to start the sandbox as it's started automatically

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Executing DataTransformationNode with data: {json.dumps(node_data, indent=2)}")
        operation = node_data.get('operation')
        input_data = node_data.get('input_data')
        parameters = node_data.get('parameters', {})

        if not operation or input_data is None:
            return {"status": "error", "message": "Missing operation or input_data"}

        try:
            df = self.to_dataframe(input_data)
            result = await self.perform_operation(operation, df, parameters)
            return {
                "status": "success",
                "result": self.to_output_format(result, node_data.get('output_format', 'dict'))
            }
        except Exception as e:
            error_msg = f"Error in DataTransformationNode: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def to_dataframe(self, data: Union[List[Dict], Dict, pd.DataFrame]) -> pd.DataFrame:
        if isinstance(data, pd.DataFrame):
            return data
        elif isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.DataFrame.from_dict(data, orient='index').transpose()
        else:
            raise ValueError("Unsupported input data format")

    async def perform_operation(self, operation: str, df: pd.DataFrame, parameters: Dict[str, Any]) -> pd.DataFrame:
        if operation == 'filter':
            return self.filter_data(df, parameters.get('condition'))
        elif operation == 'sort':
            return self.sort_data(df, parameters.get('columns'), parameters.get('ascending', True))
        elif operation == 'group_by':
            return self.group_by_data(df, parameters.get('columns'), parameters.get('aggregation'))
        elif operation == 'join':
            other_df = self.to_dataframe(parameters.get('other_data', []))
            return self.join_data(df, other_df, parameters.get('on'), parameters.get('how', 'inner'))
        elif operation == 'pivot':
            return self.pivot_data(df, parameters.get('index'), parameters.get('columns'), parameters.get('values'))
        elif operation == 'unpivot':
            return self.unpivot_data(df, parameters.get('id_vars'), parameters.get('value_vars'))
        elif operation == 'apply':
            return self.apply_function(df, parameters.get('function'), parameters.get('axis', 0))
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def filter_data(self, df: pd.DataFrame, condition: str) -> pd.DataFrame:
        return df.query(condition)

    def sort_data(self, df: pd.DataFrame, columns: List[str], ascending: bool) -> pd.DataFrame:
        return df.sort_values(columns, ascending=ascending)

    def group_by_data(self, df: pd.DataFrame, columns: List[str], aggregation: Dict[str, str]) -> pd.DataFrame:
        return df.groupby(columns).agg(aggregation).reset_index()

    def join_data(self, df1: pd.DataFrame, df2: pd.DataFrame, on: Union[str, List[str]], how: str) -> pd.DataFrame:
        return df1.merge(df2, on=on, how=how)

    def pivot_data(self, df: pd.DataFrame, index: Union[str, List[str]], columns: str, values: str) -> pd.DataFrame:
        return df.pivot(index=index, columns=columns, values=values).reset_index()

    def unpivot_data(self, df: pd.DataFrame, id_vars: List[str], value_vars: List[str]) -> pd.DataFrame:
        return df.melt(id_vars=id_vars, value_vars=value_vars)

    def apply_function(self, df: pd.DataFrame, function: str, axis: int) -> pd.DataFrame:
        return df.apply(eval(function), axis=axis)

    def to_output_format(self, df: pd.DataFrame, output_format: str) -> Union[List[Dict], Dict, pd.DataFrame]:
        if output_format == 'dict':
            return df.to_dict(orient='records')
        elif output_format == 'dataframe':
            return df
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    async def close(self):
        # The sandbox doesn't need to be closed explicitly
        self.sandbox = None
        logger.info("DataTransformationNode shutdown completed")

DataTransformationNodeNode = DataTransformationNode

# Example usage
async def run_example():
    data_transformation_node = DataTransformationNode()
    await data_transformation_node.initialize()

    try:
        # Example data
        input_data = [
            {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
            {"id": 2, "name": "Bob", "age": 25, "city": "San Francisco"},
            {"id": 3, "name": "Charlie", "age": 35, "city": "New York"},
            {"id": 4, "name": "David", "age": 28, "city": "San Francisco"}
        ]

        # Example operations
        filter_result = await data_transformation_node.execute({
            "operation": "filter",
            "input_data": input_data,
            "parameters": {"condition": "age > 28"}
        })
        print("Filter result:", json.dumps(filter_result, indent=2))

        sort_result = await data_transformation_node.execute({
            "operation": "sort",
            "input_data": input_data,
            "parameters": {"columns": ["age"], "ascending": False}
        })
        print("Sort result:", json.dumps(sort_result, indent=2))

        group_by_result = await data_transformation_node.execute({
            "operation": "group_by",
            "input_data": input_data,
            "parameters": {"columns": ["city"], "aggregation": {"age": "mean"}}
        })
        print("Group by result:", json.dumps(group_by_result, indent=2))

    except Exception as e:
        print(f"An error occurred during the example run: {str(e)}")
    finally:
        await data_transformation_node.close()

if __name__ == "__main__":
    asyncio.run(run_example())