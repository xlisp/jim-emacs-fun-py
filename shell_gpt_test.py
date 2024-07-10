
import subprocess

# Function to execute the command and auto-respond "yes"
def execute_sgpt_command(argument):
    # Format the command to include the argument
    cmd = f'sgpt --shell "{argument}" --no-interaction'

    # Create the subprocess with Popen
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Automatically send "yes" to any prompts
    stdout, stderr = process.communicate(input='Execute\n')

    # Return the command's output
    return stdout, stderr

# Example of calling the function
if __name__ == "__main__":
    argument_to_pass = "find all py files in current folder"
    output, error = execute_sgpt_command(argument_to_pass)
    print("Command Output:\n", output)
    if error:
        print("Command Error:\n", error)

# =>
# Command Output:
#  find . -name '*.py'
#
