from fastapi import FastAPI, HTTPException, UploadFile, File
from starlette.responses import FileResponse
from cryptography.fernet import Fernet

encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)
app = FastAPI()


@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    encrypted_file_path = f"{file_path}.encrypted"
    with open(encrypted_file_path, "rb") as encrypted_file:
        decrypted_contents = cipher_suite.decrypt(encrypted_file.read())

    decrypted_file_path = f"{file_path}.decrypted"
    with open(decrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_contents)

    return FileResponse(decrypted_file_path, media_type="application/octet-stream")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    encrypted_file_path = f"{file.filename}.encrypted"
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_contents = cipher_suite.encrypt(file.file.read())
        encrypted_file.write(encrypted_contents)

    # Save the encrypted file to disk
    saved_file_path = f"saved_{file.filename}"
    with open(saved_file_path, "wb") as saved_file:
        saved_file.write(encrypted_contents)
