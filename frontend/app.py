import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="ARGUS",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    """
    <div style="text-align:center; padding:20px 0;">
        <h1>🛡️ ARGUS</h1>
        <p style="font-size:20px;">
            Multimodal AI Agent
        </p>
        <p style="font-size:14px;">
            Text • Vision • Documents • Tools • Memory
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("Session Memory: Active")

st.divider()


# ==========================================================
# MODE SELECTION
# ==========================================================

st.markdown("### Choose how you want to interact with ARGUS")

mode = st.radio(
    "",
    ["Text", "Image", "Document"],
    horizontal=True
)


# ==========================================================
# TEXT MODE
# ==========================================================

if mode == "Text":

    st.markdown("### Ask ARGUS")

    prompt = st.text_area(
        "Ask ARGUS anything",
        placeholder=(
            "Try:\n"
            "• Explain machine learning\n"
            "• What is the weather in Hyderabad?\n"
            "• What am I building?"
        ),
        height=140
    )

    if st.button(
        "Ask ARGUS",
        type="primary",
        use_container_width=True
    ):

        if prompt.strip():

            try:

                response = requests.post(
                    f"{API_URL}/agent",
                    json={
                        "prompt": prompt
                    },
                    timeout=60
                )

                if response.ok:

                    data = response.json()

                    st.success(
                        f"ARGUS Route: {data['category']}"
                    )

                    st.markdown("### ARGUS Response")

                    st.info(
                        data["response"]
                    )

                    if data.get("tool"):

                        st.caption(
                            f"Tool used: {data['tool']}"
                        )

                else:

                    st.error(
                        f"ARGUS backend returned an error: "
                        f"{response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to ARGUS backend. "
                    "Make sure FastAPI is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "ARGUS request timed out. "
                    "Please try again."
                )

        else:

            st.warning(
                "Please enter a question."
            )


# ==========================================================
# IMAGE MODE
# ==========================================================

elif mode == "Image":

    st.markdown("### ARGUS Vision")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )

    prompt = st.text_input(
        "Ask ARGUS about this image",
        value=(
            "Analyze this image and explain what is shown."
        )
    )

    if uploaded_file:

        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True
        )

    if st.button(
        "Analyze Image",
        type="primary",
        use_container_width=True
    ):

        if uploaded_file:

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{API_URL}/agent-image",
                    files=files,
                    data={
                        "prompt": prompt
                    },
                    timeout=120
                )

                if response.ok:

                    data = response.json()

                    st.success(
                        f"ARGUS Route: {data['category']}"
                    )

                    st.markdown(
                        "### ARGUS Vision Response"
                    )

                    st.info(
                        data["response"]
                    )

                    st.caption(
                        "Analysis powered by ARGUS Multimodal Vision"
                    )

                else:

                    st.error(
                        f"ARGUS image error: "
                        f"{response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to ARGUS backend. "
                    "Make sure FastAPI is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Image analysis timed out. "
                    "Please try again."
                )

        else:

            st.warning(
                "Please upload an image first."
            )


# ==========================================================
# DOCUMENT MODE
# ==========================================================

elif mode == "Document":

    st.markdown("### ARGUS Document Intelligence")

    uploaded_document = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"]
    )

    if uploaded_document:

        st.info(
            f"Selected document: "
            f"{uploaded_document.name}"
        )

        if st.button(
            "Process PDF",
            type="primary",
            use_container_width=True
        ):

            try:

                files = {
                    "file": (
                        uploaded_document.name,
                        uploaded_document.getvalue(),
                        "application/pdf"
                    )
                }

                response = requests.post(
                    f"{API_URL}/upload-document",
                    files=files,
                    timeout=120
                )

                if response.ok:

                    data = response.json()

                    st.session_state[
                        "document_ready"
                    ] = True

                    st.success(
                        "PDF processed successfully."
                    )

                    st.caption(
                        f"{data['chunks']} document chunks created."
                    )

                else:

                    st.error(
                        f"PDF processing failed: "
                        f"{response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to ARGUS backend. "
                    "Make sure FastAPI is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "PDF processing timed out. "
                    "Please try again."
                )

    if st.session_state.get(
        "document_ready",
        False
    ):

        st.divider()

        st.markdown(
            "### Ask questions about your document"
        )

        question = st.text_area(
            "Document question",
            placeholder=(
                "Example:\n"
                "What are the main points of this document?"
            ),
            height=120
        )

        if st.button(
            "Ask ARGUS From Document",
            type="primary",
            use_container_width=True
        ):

            if question.strip():

                try:

                    response = requests.post(
                        f"{API_URL}/agent",
                        json={
                            "prompt": question
                        },
                        timeout=120
                    )

                    if response.ok:

                        data = response.json()

                        st.success(
                            f"ARGUS Route: {data['category']}"
                        )

                        st.markdown(
                            "### ARGUS Document Answer"
                        )

                        st.info(
                            data["response"]
                        )

                        sources = data.get(
                            "sources",
                            []
                        )

                        if sources:

                            with st.expander(
                                "View Retrieved Sources"
                            ):

                                for index, source in enumerate(
                                    sources,
                                    start=1
                                ):

                                    st.markdown(
                                        f"**Source {index}**"
                                    )

                                    st.caption(
                                        f"Similarity: "
                                        f"{source['similarity']:.4f}"
                                    )

                                    st.write(
                                        source["text"]
                                    )

                                    if index < len(sources):
                                        st.divider()

                    else:

                        st.error(
                            f"ARGUS document query failed: "
                            f"{response.status_code}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to ARGUS backend. "
                        "Make sure FastAPI is running."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "Document query timed out. "
                        "Please try again."
                    )

            else:

                st.warning(
                    "Please enter a question."
                )