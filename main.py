from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.templating import Jinja2Templates
from docx import Document
from io import BytesIO

app = FastAPI()

# Global variable to store the uploaded Word document data
word_data = None

# Templates
templates = Jinja2Templates(directory="templates")

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    global word_data
    
    # Check if the uploaded file is a Word document
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only Word documents (docx) are allowed.")
    
    # Read the file content
    data = await file.read()
    
    try:
        # Read the Word document data
        word_data = Document(BytesIO(data))
        
        # Extract text from the document
        document_text = []
        for paragraph in word_data.paragraphs:
            document_text.append(paragraph.text)
        
        # Now, document_text contains a list of text extracted from the Word document
        # You can print or process this text as needed
        for text in document_text:
            print(text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading Word document: {str(e)}")
    
    return {"message": "Word document uploaded and processed successfully"}

@app.post("/query/")
async def query_data(query: str):
    if word_data is None:
        raise HTTPException(status_code=400, detail="No Word document data uploaded")

    # Extract text from the Word document
    document_text = ""
    for paragraph in word_data.paragraphs:
        document_text += paragraph.text + "\n"
    
    # Debugging: Print the entire document_text
    
    # Search for the query text in the document text
    results = [line for line in document_text.split('\n') if query in line]
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
