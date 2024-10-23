from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting furniture and home-goods product names from the following html content from online store website: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **HTML tags:** You can find html tags with class name, that contains for exapmple 'prod' or 'product', also take a look on tags <a> that contains products under links, but sometimes product names can be without classes or links"
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only names of products, without images or your comments or notes, with no other text."
)

model = OllamaLLM(model="llama3")

def parse_ollama(dom_chunks):
    print('parsing...')
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)
        print(response)

    return "\n".join(parsed_results)