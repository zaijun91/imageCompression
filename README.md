# Image Compressor GUI

A simple and powerful desktop application for compressing JPG and PNG images with full control over the output file size.

![App Screenshot](placeholder.png)  
*(This is a placeholder for the application's screenshot)*

## ✨ Features

- **User-Friendly Interface:** An intuitive graphical user interface (GUI) for easy operation.
- **File & Folder Selection:** Compress single images or entire folders in batches.
- **Custom Output Location:** Choose exactly where you want to save your compressed files.
- **Target Size Compression:** Specify a minimum and maximum file size (in KB), and the application will automatically find the best compression quality to match your target.
- **Standalone Application:** Packaged as a single `.exe` file that runs without needing Python or any other dependencies.

## 🚀 How to Use

1.  **Launch the Application:** Double-click the `image_compressor_app.exe` file.
2.  **Select Input:**
    - Click **"选择图片"** to compress a single image file.
    - Click **"选择文件夹"** to compress all images within a folder.
3.  **Select Output:**
    - Click **"选择输出文件夹"** to choose where the compressed images will be saved.
4.  **Set Compression Range:**
    - Enter your desired **"最小大小 (KB)"** and **"最大大小 (KB)"**.
5.  **Compress:**
    - Click the **"开始压缩"** button and monitor the progress in the log window.

## 💻 For Developers (Command-Line Usage)

The core logic can also be run as a Python script.

### Compress a single image:
```bash
python imageCompression.py -i "path/to/your/image.jpg" --min-size 2048 --max-size 4096
```

### Compress a directory:
```bash
python imageCompression.py -d "path/to/your/folder" --min-size 2048 --max-size 4096
