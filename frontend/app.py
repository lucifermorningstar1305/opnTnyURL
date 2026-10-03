import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


st.title("Open Tiny URL")
url = st.text_input("Enter a URL")


API_BASE_URL = os.getenv("API_BASE_URL")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL")

if st.button("Shorten"):
    if not url:
        st.warning("Please enter a URL.")

    else:
        assert API_BASE_URL is not None
        response = requests.post(f"{API_BASE_URL}/add", json={"url": url}, timeout=10)

        if response.ok:
            data = response.json()
            short_id = data["data"]
            short_url = f"{PUBLIC_BASE_URL}/{short_id}"
            st.success("Short URL Created")
            st.code(short_url)

            st.link_button("Open short URL", short_url)

        else:
            st.error("Failed to create short URL.")
