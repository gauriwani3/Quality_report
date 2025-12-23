import streamlit as st
import requests

# GitHub URL for the .dat file in Releases
url = "https://github.com/gauriwani3/Quality_report/releases/download/v1.0/Qual_Report_25LPML281106_1.__2025-12-01_06.17.42.dat"

# Function to download the .dat file
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

    st.write(f"Header Length: {len(header)}")

    # First 20 bytes are raw identifier (do not decode as text)
    identifier_bytes = header[:20]

    # Show identifier as hex string for readability
    identifier_hex = identifier_bytes.hex().upper()
    st.write(f"Identifier (hex): {identifier_hex}")

    # Remaining header bytes are marker / metadata, decode as UTF-8 safely
    marker_bytes = header[20:]
    try:
        marker_str = marker_bytes.decode('utf-8', errors='ignore').strip()
    except Exception as e:
        st.error(f"Error decoding marker: {e}")
        marker_str = ""

    st.write(f"Marker Info: {marker_str}")
    return identifier_hex, marker_str

# Function to process the .dat file
def process_file():
    binary_data = download_file()
    if not binary_data:
        return None

    identifier, marker = extract_header(binary_data)

    # Data section starts after 128-byte header
    data_section = binary_data[128:]

    # Decode data section safely
    try:
        data_section_str = data_section.decode('utf-8', errors='ignore')
    except Exception as e:
        st.error(f"Error decoding data section: {e}")
        return None

    # Parse key-value pairs
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

# Streamlit UI
def display_data():
    st.title("Quality Report - Processed .dat File")

    if st.button("Process .dat File"):
        processed_data = process_file()
        if processed_data:
            st.subheader("Header Information")
            st.text(f"Identifier (hex): {processed_data['header']['identifier']}")
            st.text(f"Marker: {processed_data['header']['marker']}")

            st.subheader("Data Section")
            st.table(processed_data['data_section'])
        else:
            st.write("Failed to process the file.")

if __name__ == "__main__":
    display_data()
