import streamlit as st
import requests

# GitHub URL for the .dat file in Releases
url = "https://github.com/gauriwani3/Quality_report/releases/download/v1.0/Qual_Report_25LPML281106_1.__2025-12-01_06.17.42.dat"

# Function to download the .dat file from GitHub Releases
def download_file():
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        st.error("Failed to download the file from GitHub.")
        return None

# Function to extract the header safely
def extract_header(binary_data):
    header_size = 128
    header = binary_data[:header_size]

    # Show header length (should be 128 bytes)
    st.write(f"Header Length: {len(header)} bytes")

    # First 20 bytes are raw identifier (no decoding)
    identifier_bytes = header[:20]
    identifier_hex = identifier_bytes.hex().upper()  # Show identifier in hex format
    st.write(f"Identifier (hex): {identifier_hex}")

    # The remaining 108 bytes as marker / metadata
    marker_bytes = header[20:]

    try:
        # Decode the marker bytes as ASCII text (ignoring errors)
        marker_str = marker_bytes.decode('ascii', errors='ignore').strip()
    except Exception as e:
        st.error(f"Error decoding marker: {e}")
        marker_str = ""

    st.write(f"Marker Info (Decoded): {marker_str}")
    return identifier_hex, marker_str

# Function to process the entire .dat file
def process_file():
    binary_data = download_file()
    if not binary_data:
        return None

    identifier, marker = extract_header(binary_data)

    # Data section starts after 128-byte header
    data_section = binary_data[128:]

    # Decode data section safely as UTF-8
    try:
        data_section_str = data_section.decode('utf-8', errors='ignore')
    except Exception as e:
        st.error(f"Error decoding data section: {e}")
        return None

    # Parse the data section into key-value pairs (if any)
    parsed_data = {}
    for line in data_section_str.splitlines():
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            parsed_data[key.strip()] = value.strip()
        else:
            parsed_data[line] = None

    return {
        "header": {
            "identifier": identifier,
            "marker": marker
        },
        "data_section": parsed_data
    }

# Streamlit UI to display data
def display_data():
    st.title("Quality Report - Processed .dat File")

    if st.button("Process .dat File"):
        processed_data = process_file()
        if processed_data:
            # Header Information
            st.subheader("Header Information")
            st.text(f"Identifier (hex): {processed_data['header']['identifier']}")
            st.text(f"Marker: {processed_data['header']['marker']}")

            # Data Section
            st.subheader("Data Section")
            if processed_data['data_section']:
                st.table(processed_data['data_section'])
            else:
                st.write("No valid data found in the data section.")
        else:
            st.write("Failed to process the file.")

if __name__ == "__main__":
    display_data()
