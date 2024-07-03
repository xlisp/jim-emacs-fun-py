import asyncio

async def fetch_from_socket():
    reader, writer = await asyncio.open_connection('example.com', 80)
    
    writer.write(b'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n')
    await writer.drain()

    # Open the file in binary mode
    with open('example.txt', 'wb') as f:
        while True:
            data = await reader.read(100)  # Adjust the buffer size as needed
            if not data:
                break
            f.write(data)

    writer.close()
    await writer.wait_closed()

    print("Fetch complete")
    return 'example.txt'

async def process_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        # Process the content as needed
        print(f"Processed {len(content)} bytes from {file_path}")

async def main():
    # First async function
    file_path = await fetch_from_socket()
    
    # Next async function, which waits for the first one to complete
    await process_file(file_path)

# Run the main function
asyncio.run(main())

