import tempfile

# create a temporary file and write some data to it
fp = tempfile.TemporaryFile()
fp.write(b'Hello world!')
# read data from file
fp.seek(0)
fp.read()

b'Hello world!'

# close the file, it will be removed

fp.close()

fp.name #=> 7

f = tempfile.NamedTemporaryFile(delete=False)
f.write(b"dasdsadsadsadsadas")
f.name

import tempfile
import os

# Specify the custom directory path
custom_dir = 'src/abc'

# Create a temporary file in the custom directory
temp_fd, temp_path = tempfile.mkstemp(dir=custom_dir)

# Close the file descriptor since we're not using it
os.close(temp_fd)

# Print the temporary file path
print(temp_path)
