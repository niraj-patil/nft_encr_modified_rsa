from moralis import evm_api
import base64
import os

from dotenv import load_dotenv
load_dotenv()
#image upload
def uploadToIPFS(path:str):
    api_key = os.getenv('API_KEY')
    with open(path, "rb") as img_file:
        BASE64IMG = (base64.b64encode(img_file.read())).decode("ascii")

    imageBody = [
        {
            "path": "RSA.png",
            "content": BASE64IMG,
        }
    ]

    imagePath = evm_api.ipfs.upload_folder(
        api_key=api_key,
        body=imageBody,
    )
#metadata upload
    import json
    content = {
        "name": "Test",
        "description": "Modified RSA Test Image",
        "image":imagePath[0]['path'],
    }

    metadataBody = [
        {
            "path": "metadata.json",
            "content": base64.b64encode(bytes(json.dumps(content), "ascii")).decode(
                "ascii"
            ),
        }
    ]


    result = evm_api.ipfs.upload_folder(
        api_key=api_key,
        body=metadataBody,
    )

    return result[0]['path']

