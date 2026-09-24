import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="ARGUS",
    page_icon="🛡️",
    layout="wide"
)


st.title("🛡️ ARGUS")
st.subheader("Multimodal AI Agent")

st.divider()


mode = st.radio(
    "Choose input type",
    ["Text", "Image", "Document"],
    horizontal=True
)


if mode == "Text":

    prompt = st.text_area(
        "Ask ARGUS anything",
        placeholder="Enter your question..."
    )

    if st.button("Ask ARGUS"):
        if prompt.strip():
            response = requests.post(
                f"{API_URL}/ask",
                json={"prompt": prompt}
            )

            if response.ok:
                data = response.json()
                st.write(data["response"])
            else:
                st.error("ARGUS backend returned an error.")


elif mode == "Image":

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    prompt = st.text_input(
        "What should ARGUS analyze?",
        value="Analyze this image carefully and describe what you see."
    )

    if st.button("Analyze Image"):
        if uploaded_file:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            response = requests.post(
                f"{API_URL}/analyze-image",
                files=files,
                data={"prompt": prompt}
            )

            if response.ok:
                data = response.json()

                st.image(
                    uploaded_file,
                    caption="Uploaded Image"
                )

                st.write(data["response"])
            else:
                st.error("ARGUS image analysis failed.")


elif mode == "Document":

    question = st.text_area(
        "Ask a question about the document",
        placeholder="Example: What are the main areas I need to improve?"
    )

    if st.button("Ask From Document"):
        if question.strip():

            response = requests.post(
                f"{API_URL}/ask-document",
                json={"question": question}
            )

            if response.ok:
                data = response.json()

                st.write("### ARGUS Answer")
                st.write(data["answer"])

                with st.expander("Sources"):
                    for source in data["sources"]:
                        st.write(
                            f"Similarity: "
                            f"{source['similarity']:.4f}"
                        )
                        st.write(source["text"])

            else:
                st.error("ARGUS document search failed.")