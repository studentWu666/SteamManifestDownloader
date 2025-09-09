import tkinter as tk
from tkinter import messagebox, filedialog
import re
import requests
import os
import sys
import webbrowser

class SteamManifestDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam Manifest 下载器")
        self.root.geometry("600x250")
        self.root.resizable(False, False)
        
        # 设置窗口背景色
        self.root.configure(bg="#f0f0f0")
        
        # 创建标题标签
        title_font = ("微软雅黑", 12, "bold")
        self.title_label = tk.Label(root, text="Steam Manifest 下载器", font=title_font, bg="#f0f0f0", fg="#333333")
        self.title_label.pack(pady=15)
        
        # 创建主框架
        main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.RAISED)
        main_frame.pack(padx=20, pady=5, fill=tk.BOTH)
        
        # 创建标签和输入框
        input_font = ("微软雅黑", 10)
        self.label = tk.Label(main_frame, text="请输入appID或Steam商店链接:", font=input_font, bg="#ffffff", fg="#555555")
        self.label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        
        # 创建输入框，添加样式
        self.entry = tk.Entry(main_frame, font=input_font, width=50, bd=2, relief=tk.SUNKEN, highlightthickness=1)
        self.entry.grid(row=1, column=0, padx=15, pady=5, ipady=5, columnspan=2)
        self.entry.configure(highlightbackground="#cccccc", highlightcolor="#0078d7")
        
        # 创建下载按钮，添加样式
        button_font = ("微软雅黑", 10, "bold")
        self.download_button = tk.Button(
            main_frame, 
            text="下载清单", 
            font=button_font, 
            command=self.download_manifest, 
            bg="#0078d7", 
            fg="white", 
            relief=tk.RAISED, 
            bd=2, 
            padx=10, 
            pady=5
        )
        self.download_button.grid(row=2, column=0, columnspan=2, pady=(15, 15))
        
        # 添加悬停效果
        self.download_button.bind("<Enter>", lambda e: self.download_button.config(bg="#106ebe"))
        self.download_button.bind("<Leave>", lambda e: self.download_button.config(bg="#0078d7"))
        
        # 添加底部信息标签
        info_font = ("微软雅黑", 8)
        self.info_label = tk.Label(root, text="支持从Steam商店链接或直接输入appID下载清单文件", font=info_font, bg="#f0f0f0", fg="#666666")
        self.info_label.pack(pady=(5, 10))
        
    def extract_steam_id(self, input_text):
        """从输入文本中提取Steam ID"""
        # 检查是否已经是纯数字ID
        if input_text.isdigit():
            return input_text
        
        # 使用正则表达式从URL中提取ID
        match = re.search(r'https://store\.steampowered\.com/app/(\d+)/', input_text)
        if match:
            return match.group(1)
        
        return None
    
    def get_application_path(self):
        """获取应用程序所在路径"""
        if getattr(sys, 'frozen', False):
            # 打包后的exe文件
            return os.path.dirname(sys.executable)
        else:
            # 开发环境
            return os.path.dirname(os.path.abspath(__file__))
    
    def download_manifest(self):
        """下载清单文件"""
        input_text = self.entry.get().strip()
        if not input_text:
            messagebox.showerror("输入错误", "请输入appID或Steam商店链接！")
            return
        
        # 提取Steam ID
        steam_id = self.extract_steam_id(input_text)
        if not steam_id:
            messagebox.showerror("输入错误", "请输入有效的appID或Steam商店链接！")
            return
        
        # 构建下载URL
        download_url = f"https://codeload.github.com/SteamAutoCracks/ManifestHub/zip/refs/heads/{steam_id}"
        
        # 获取保存路径
        save_dir = self.get_application_path()
        save_path = os.path.join(save_dir, f"{steam_id}.zip")
        
        # 显示下载提示
        messagebox.showinfo("下载中", f"请确保可以正常访问Github，否则下载时会出现连接被拒绝！\n\n将保存到:\n{save_path}")
        
        try:
            # 下载文件
            response = requests.get(download_url, stream=True)
            response.raise_for_status()  # 检查请求是否成功
            
            # 写入文件
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            messagebox.showinfo("成功", "下载完成！")
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if "Connection refused" in error_msg or "ConnectionResetError" in error_msg:
                result = messagebox.askyesno("下载失败", f"连接被拒绝，请检查互联网连接或使用加速器以访问Github\n\n详细错误：\n{error_msg}\n\n是否跳转到备用网站 https://manifest.steam.run/ 尝试下载？")
            else:
                result = messagebox.askyesno("下载失败", f"下载过程中出现错误：\n{error_msg}\n\n是否跳转到备用网站 https://manifest.steam.run/ 尝试下载？")
            
            if result:
                webbrowser.open("https://manifest.steam.run/")
        except Exception as e:
            error_msg = str(e)
            result = messagebox.askyesno("下载失败", f"发生未知错误：\n{error_msg}\n\n是否跳转到备用网站 https://manifest.steam.run/ 尝试下载？")
            
            if result:
                webbrowser.open("https://manifest.steam.run/")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteamManifestDownloader(root)
    root.mainloop()