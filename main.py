import streamlit as st
import parser
import llama_model
import subprocess

def main():
    subprocess.run("libglib2.0-0=2.50.3-2 \
                    libnss3=2:3.26.2-1.1+deb9u1 \
                    libgconf-2-4=3.2.6-4+b1 \
                    libfontconfig1=2.11.0-6.7+b1",
                   capture_output=True, text=True)
    st.title("Product Scraper")
    urls = st.text_input("Enter a Website URLs: ")

    result = "NO RESPONSE"
    if st.button("Scrape site"):
        st.write("Scraping the website...")

        result = parser.URL_parser(urls)
        body_content = parser.body_content(result)
        cleaned_content = parser.cleaned_content(body_content)

        #st.session_state.dom_content = result

        #with st.expander("View"):
            #st.text_area("DOM", cleaned_content, height=300)

        if result != "NO RESPONSE":
            dom_chunks = parser.split_dom_content(cleaned_content)
            result = llama_model.parse_ollama(dom_chunks)
        st.write(result)
    
if __name__ == "__main__":
    main()
