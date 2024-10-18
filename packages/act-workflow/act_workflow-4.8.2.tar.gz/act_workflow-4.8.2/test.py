import os
from pathlib import Path
from act import ExecutionManager

def main():
    # Get the directory of the current script
    current_dir = Path(__file__).parent

    # Construct the path to the Actfile
    actfile_path = current_dir / 'Actfile'

    print(f"Looking for Actfile at: {actfile_path}")

    # Check if the file exists
    if not actfile_path.exists():
        print(f"Error: Actfile not found at {actfile_path}")
        return

    # Initialize the ExecutionManager with the full path to your Actfile
    execution_manager = ExecutionManager(str(actfile_path))
    
    # Execute the workflow
    result = execution_manager.execute_workflow()
    
    # Print the result
    print("Workflow Execution Result:")
    print(result)

if __name__ == "__main__":
    main()