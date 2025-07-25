# ai_pdf_converter.py
from marker.convert import convert_single_pdf
from marker.models import load_all_models
import os
from pathlib import Path

def convert_pdf_with_marker(pdf_path: str, output_folder: str):
    """使用marker AI模型转换PDF"""
    
    print("🤖 Loading AI models...")
    model_lst = load_all_models()
    
    print(f"📄 Converting: {pdf_path}")
    
    # AI转换
    full_text, images, out_meta = convert_single_pdf(pdf_path, model_lst)
    
    # 准备输出
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    filename = Path(pdf_path).stem
    output_path = f"{output_folder}/{filename}.md"
    
    # 保存Markdown
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    # 保存图片（如果有）
    if images:
        images_folder = f"{output_folder}/images"
        Path(images_folder).mkdir(parents=True, exist_ok=True)
        
        for img_name, img_data in images.items():
            img_path = f"{images_folder}/{img_name}"
            with open(img_path, 'wb') as f:
                f.write(img_data)
    
    print(f"✅ AI Conversion complete!")
    print(f"   📄 Output: {output_path}")
    print(f"   📷 Images: {len(images)} extracted")
    
    return output_path

def batch_convert_with_marker(pdf_folder: str, output_folder: str):
    """批量AI转换"""
    
    if not os.path.exists(pdf_folder):
        print(f"❌ Folder not found: {pdf_folder}")
        return
    
    pdf_files = list(Path(pdf_folder).glob("*.pdf"))
    print(f"📁 Found {len(pdf_files)} PDF files")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n🔄 Processing {i}/{len(pdf_files)}: {pdf_file.name}")
        try:
            convert_pdf_with_marker(str(pdf_file), output_folder)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    PDF_FOLDER = "LegalFiles"
    OUTPUT_FOLDER = "WIKI"
    
    batch_convert_with_marker(PDF_FOLDER, OUTPUT_FOLDER)