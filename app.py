import streamlit as st
import numpy as np
import requests

# -------------------------------
# Extract header from binary file
# -------------------------------
def extract_header(binary_data):
    header_size = 128
    header = binary_data[:header_size]

    st.write(f"Header Length: {len(header)} bytes")

    # First 20 bytes: identifier (binary)
    identifier_bytes = header[:20]
    identifier_hex = identifier_bytes.hex().upper()
    st.write(f"Identifier (hex): {identifier_hex}")

    # Remaining 108 bytes: marker / metadata
    marker_bytes = header[20:]
    marker_str = marker_bytes.decode("ascii", errors="ignore").strip()
    marker_hex = marker_bytes.hex().upper()

    st.write("Marker Info (Decoded):")
    st.text(marker_str)

    return identifier_hex, marker_str


# -------------------------------
# Process uploaded .dat file
# -------------------------------
def process_file(uploaded_file):
    if not uploaded_file:
        st.error("No file uploaded.")
        return None

    binary_data = uploaded_file.read()

    # Extract header
    identifier, marker = extract_header(binary_data)

    # Data starts after 128-byte header
    data_section = binary_data[128:]

    # Decode binary REAL values (float32)
    try:
        data_array = np.frombuffer(data_section, dtype=np.float32)
    except Exception as e:
        st.error(f"Binary decode error: {e}")
        return None

    return {
        "header": {
            "identifier": identifier,
            "marker": marker
        },
        "data": data_array
    }


# -------------------------------
# Streamlit UI
# -------------------------------
def display_data():
    st.title("Quality Report – .dat File Viewer")

    uploaded_file = st.file_uploader("Upload a .dat file", type=["dat"])

    if uploaded_file:
        processed = process_file(uploaded_file)

        if processed:
            # Header info
            st.subheader("Header Information")
            st.text(f"Identifier (hex): {processed['header']['identifier']}")
            st.text("Marker:")
            st.text(processed['header']['marker'])

            # Data section
            st.subheader("Data Section (Binary REAL values)")

            data = processed["data"]

            st.write(f"Total Samples: {len(data)}")

            # Show first samples
            st.write("First 20 Samples:")
            st.write(data[:20])

            # Plot data
            st.subheader("Signal Plot (First 1000 Samples)")
            st.line_chart(data[:1000])

        else:
            st.error("Failed to process file.")
    else:
        st.info("Please upload a .dat file to begin.")


if __name__ == "__main__":
    display_data()
