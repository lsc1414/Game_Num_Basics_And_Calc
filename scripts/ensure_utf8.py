
import os
import chardet

def check_encoding(filepath):
    rawdata = open(filepath, 'rb').read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    confidence = result['confidence']
    return encoding, confidence

def scan_and_fix(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                encoding, confidence = check_encoding(full_path)
                
                # If it's likely not UTF-8 (or ASCII), we might need to fix it.
                # However, chardet is not perfect. 
                # A better way is: try read as UTF-8. If fail, try GBK.
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    status = "UTF-8"
                except UnicodeDecodeError:
                    try:
                        with open(full_path, 'r', encoding='gb18030') as f:
                            content = f.read()
                        # It was GBK/GB18030. Convert to UTF-8
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        status = "CONVERTED_FROM_GBK"
                    except:
                        status = "UNKNOWN_FAIL"
                
                print(f"[{status}] {full_path} (chardet: {encoding}, {confidence})")

if __name__ == "__main__":
    scan_and_fix("i:/MTSVN_NEW/002_Vampirefall/Server/Game_Num_Basics_And_Calc/docs")
