# Steam Manifest 下载器

这是一个简单的Windows桌面应用程序，用于从GitHub下载Steam游戏的清单文件。

## 功能介绍
- 启动时弹出对话框，提示用户输入Steam appID或商店链接
- 支持解析Steam商店链接（如 https://store.steampowered.com/app/{id}/）并提取其中的appID
- 点击"下载清单"按钮后，从GitHub下载对应的Manifest文件
- 下载的文件将保存到程序所在目录

## 使用方法
1. 运行 `Steam_Manifest_Downloader.exe`
2. 在输入框中输入Steam appID（纯数字）或完整的Steam商店链接
3. 点击"下载清单"按钮
4. 程序会自动下载对应的Manifest文件并保存到当前目录

## 注意事项
- 如果编译失败，请检查`compile.bat`中的GCC路径是否正确
- 下载过程中请确保网络连接正常
- 下载的文件格式为ZIP压缩包，文件名与appID相同

## 示例
- 输入纯数字ID：`730`（Counter-Strike 2的appID）
- 输入完整链接：`https://store.steampowered.com/app/730/CounterStrike_2/`
- 点击"下载清单"按钮后，会下载名为`730.zip`的文件
