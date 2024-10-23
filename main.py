import streamlit as st
import parser
import llama_model
import subprocess

@st.cache_resource
def get_driver():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=chrome_options,
    )
    
def main():
    # Run the command to install the necessary packages
    command = [
        "sudo", "apt-get", "install", "-y",
        "libglib2.0-0=2.50.3-2",
        "libnss3=2:3.26.2-1.1+deb9u1",
        "libgconf-2-4=3.2.6-4+b1",
        "libfontconfig1=2.11.0-6.7+b1"
    ]
    
    # Execute the command
    subprocess.run(command, capture_output=True, text=True)

    st.title("Product Scraper")
    urls = st.text_input("Enter a Website URLs: ")

    result = "NO RESPONSE"
    if st.button("Scrape site"):
        st.write("Scraping the website...")

        result = parser.URL_parser(urls)
        body_content = parser.body_content(result)
        cleaned_content = parser.cleaned_content(body_content)

        if result != "NO RESPONSE":
            dom_chunks = parser.split_dom_content(cleaned_content)
            result = llama_model.parse_ollama(dom_chunks)
        st.write(result)

if __name__ == "__main__":
    main()
