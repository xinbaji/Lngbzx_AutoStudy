import ddddocr
import os
def ocr(data):
    
    ocr_tool = ddddocr.DdddOcr(show_ad=False)
    if isinstance(data, str):
        if os.path.exists(data):
            with open(data, "rb") as f:
                img_bytes = f.read()
        else:
            raise FileNotFoundError(f"文件 {data} 不存在")
    

    text = ocr_tool.classification(img_bytes)

    return text

if __name__ == "__main__":
    ocr("screenshots\passcode.png")
