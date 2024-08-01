# File containing the import statements
import_file = 'imports.txt'

# Dictionary to keep track of import status
import_status = {}

# Read the import statements from the file
with open(import_file, 'r') as file:
    import_statements = file.readlines()

# Attempt to execute each import statement
for import_statement in import_statements:
    import_statement = import_statement.strip()  # Remove any extra whitespace
    if import_statement:  # Check if the line is not empty
        try:
            exec(import_statement)
            import_status[import_statement] = 'Success'
        except ImportError as e:
            import_status[import_statement] = f'Failed: {e}'
        except Exception as e:
            import_status[import_statement] = f'Failed: {e}'

# Print the import status
for statement, status in import_status.items():
    print(f'Import statement "{statement}": {status}')
