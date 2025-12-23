import streamlit as st
import requests
import struct

# GitHub URL for the .dat file in Releases
url = "https://github.com/gauriwani3/Quality_report/releases/download/v1.0/Qual_Report_25LPML281106_1.__2025-12-01_06.17.42.dat"
# Function to download the .dat file from GitHub Releases
def download_file():
    response = requests.get(url)  # Sending a GET request to the file URL
    if response.status_code == 200:
        return response.content  # Return the raw binary content of the file
    else:
        st.error("Failed to download the file.")
        return None

# Function to extract the header (first 128 bytes) and interpret it
def extract_header(binary_data):
    # Assuming the header size should be 128 bytes, adjust if needed
    header_size = 128
    header = binary_data[:header_size]
    
    # Check the length of the header before unpacking
    st.write(f"Header Length: {len(header)}")  # This will display the length of the header
    
    if len(header) < 24:  # Minimum length for a 20-byte string + 4-byte float
        st.error("Header is smaller than expected. Check the .dat file format.")
        st.write(f"Header Data: {header.hex()}")  # Display header content in hexadecimal format
        return None, None

    try:
        # Extract the identifier (first 20 bytes) as raw bytes (without decoding)
        identifier = header[:20]  # First 20 bytes as identifier (raw bytes)
        st.write(f"Raw Identifier (bytes): {identifier}")
        
        # Try to decode the identifier as UTF-8 (if it seems like text)
        identifier_str = identifier.decode('utf-8', errors='ignore').strip()
        st.write(f"Decoded Identifier: {identifier_str}")
        
        # Check for any "beginheader:" text or other markers after the identifier
        marker = header[20:].decode('utf-8', errors='ignore')  # Decode remaining part for markers
        st.write(f"Remaining Header Data (Marker): {marker}")

        return identifier_str, marker  # Return identifier and the rest of the header as marker
    
    except Exception as e:
        # Display the error if unpacking fails
        st.error(f"Error processing header: {str(e)}")
        return None, None

# Function to process the entire binary file (header + data sections)
def process_file():
    # Step 1: Download the binary .dat file
    binary_data = download_file()
    if not binary_data:
        return None
    
    # Step 2: Extract the header
    identifier, marker = extract_header(binary_data)
    
    if not identifier:
        return None

    # Step 3: Inspect the Data Section
    data_section = binary_data[128:]  # Assuming data starts after the header (128 bytes)
    
    # Print first few bytes of the data section to inspect its structure
    st.write(f"Data Section (first 64 bytes): {data_section[:64].hex()}")

    # Here, we would need to modify the struct.unpack based on the data structure you observe
    try:
        # If the section contains integers (example), unpack it as a series of 4-byte integers
        # Adjust the format based on what you find in the data section
        # For now, let's assume it's a series of 4-byte integers
        section_data = struct.unpack('i' * (len(data_section) // 4), data_section)
    except struct.error as e:
        st.error(f"Error unpacking data section: {str(e)}")
        return None
    
    return {
        "header": {
            "identifier": identifier,
            "marker": marker  # We’re using `marker` for now as the rest of the header data
        },
        "data_section": section_data
    }

# Streamlit app to display the data
def display_data():
    st.title("Quality Report - Processed Data from .dat File")
    
    # Process the file when the button is pressed
    if st.button('Process .dat File'):
        processed_data = process_file()
        
        if processed_data:
            st.subheader("Header Information")
            st.write(f"Identifier: {processed_data['header']['identifier']}")
            st.write(f"Marker: {processed_data['header']['marker']}")
            
            st.subheader("Data Section")
            st.write(processed_data['data_section'])
        else:
            st.write("Failed to process the file.")

if __name__ == '__main__':
    display_data()
