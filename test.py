import wikipediaapi
import os
from pathlib import Path

def download_wiki_page(title: str, folder_path: str, filename: str = None):
    """下载Wikipedia页面到指定文件夹"""
    
    # 创建Wikipedia对象
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent='RAG-Project/1.0 (Educational Purpose)'
    )
    
    # 确保文件夹存在
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    
    # 获取页面
    page = wiki.page(title)
    
    if page.exists():
        # 生成文件名
        if filename is None:
            filename = title.replace(" ", "_").replace("/", "_").lower() + ".md"
        
        # 完整文件路径
        file_path = os.path.join(folder_path, filename)
        
        # 保存文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"title: \"{page.title}\"\n")
            f.write(f"description: \"Wikipedia article about {page.title}\"\n")
            f.write(f"---\n\n")
            f.write(f"# {page.title}\n\n")
            f.write(page.text)
        
        print(f"Downloaded: {title} -> {file_path}")
        return file_path
    else:
        print(f"Article not found: {title}")
        return None


def download_multiple_pages(titles: list, folder_path: str):
    """批量下载多个Wikipedia页面"""
    
    success_count = 0
    failed_titles = []
    
    for title in titles:
        result = download_wiki_page(title, folder_path)
        if result:
            success_count += 1
        else:
            failed_titles.append(title)
    
    print(f"\nDownload Summary:")
    print(f"Successfully downloaded: {success_count}/{len(titles)}")
    if failed_titles:
        print(f"Failed downloads: {failed_titles}")



if __name__ == "__main__":

    articles = [
        "Artificial intelligence",
        "Machine learning",
        "Natural language processing", 
        "Deep learning",
        "Neural network",
        "Computer vision",
        "Robotics",
        "Data science"
    ]
    
    download_folder = "WIKI"
    
    download_multiple_pages(articles, download_folder)
    
    downloaded_files = os.listdir(download_folder)
    print(f"\nFiles in {download_folder}:")
    for file in downloaded_files:
        print(f"  - {file}")