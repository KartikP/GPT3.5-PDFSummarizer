import PyPDF2
import openai

openai.organization = "INSERT-OPENAI-ORGANIZATION-HERE"
openai.api_key = "INSERT-OPENAI-API-KEY-HERE"
openai.Model.list()
messages = [{"role": "user", "content": "Hello!"}, ]

def chat(text):
    global messages
    messages.append({"role": "user", "content": text})

    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=300
    )
    print(f"The current usage is: {output['usage']}")
    return output.choices[0]['message']['content']

def create_image(text):
    global messages
    messages.append({"role": "user", "content": text})
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

def load_pdf(file, nPages=0):
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    print(f"This document contains {len(pdfReader.pages)} pages.")
    text = {}
    if type(nPages) == int:
        pageObj = pdfReader.pages[nPages]
        text[nPages] = pageObj.extract_text()
    else:
        for p in range(nPages[0], nPages[1]):
            pageObj = pdfReader.pages[p]
            text[p] = pageObj.extract_text()
    pdfFileObj.close()
    print(f"Completed extracting text.")
    return text

def combine_dict(dict):
    combined_text = " ".join(dict.values())
    return combined_text

def summarize_text(text):
    prompt = "Summarize the following text '" + text + "'"
    return chat(prompt)


pdftext = load_pdf(file="data/bitcoin.pdf", nPages=[0, 1])

print(summarize_text(combine_dict(pdftext)))
