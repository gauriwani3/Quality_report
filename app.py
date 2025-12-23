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

# Function to extract the header (first 128 bytes) safely
def extract_header(binary_data):
    header_size = 128
    header = binary_data[:header_size]

    st.write(f"Header Length: {len(header)}")

    try:
        # First 20 bytes as identifier (keep raw, decode latin-1 to avoid errors)
        identifier_bytes = header[:20]
        identifier_str = identifier_bytes.decode('latin-1').strip()
        st.write(f"Identifier (safe decoding): {identifier_str}")

        # Remaining header bytes as marker / metadata
        marker_bytes = header[20:]
        marker_str = marker_bytes.decode('latin-1', errors='ignore').strip()
        st.write(f"Marker Info: {marker_str}")

        return identifier_str, marker_str

    except Exception as e:
        st.error(f"Error processing header: {e}")
        return None, None

# Function to process the entire .dat file
def process_file():
    binary_data = download_file()
    if not binary_data:
        return None

    identifier, marker = extract_header(binary_data)
    if not identifier:
        return None

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
            st.text(f"Identifier: {processed_data['header']['identifier']}")
            st.text(f"Marker: {processed_data['header']['marker']}")

            st.subheader("Data Section")
            st.table(processed_data['data_section'])
        else:
            st.write("Failed to process the file.")

if __name__ == "__main__":
    display_data()
