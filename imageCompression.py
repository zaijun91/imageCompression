import sys, getopt
from PIL import Image
from pathlib import Path
import os

# 全局存放压缩的图片信息
g_compress_data = []

def commandHelp():
    '''
    命令帮助
    '''
    print('\n')
    print('test.py [-i <imgs>] [-q <quality>] [-s <subsampling>] [-j <jpga>] [-d <dir>] [--min-size <min_kb>] [--max-size <max_kb>]')
    print('     -i, --imgs 需要压缩的图片，多个图片以逗号分隔 "a.jpg,b.jpg')
    print('     -q, --quality 默认压缩的图片质量为15，可以调整0-95 ')
    print('     -j, --jpga 为1时设置将图片统计转换成.jpg格式，默认为0 ')
    print('     -d, --dir 设置一个目录，压缩指定目录下的图片 ')
    print('     --min-size 目标最小文件大小 (KB)')
    print('     --max-size 目标最大文件大小 (KB)')
    print('     -s, subsampling 设置编码器的子采样 默认-1 ')
    print('                     -1: equivalent to keep ')
    print('                      0: equivalent to 4:4:4 ')
    print('                      1: equivalent to 4:2:2 ')
    print('                      2: equivalent to 4:2:0 ')
    print('\n')
    print('命令示例：python test.py -i a.jpg,b.jpg -q 20')
    print('\n')

def main(argv):
    """
    命令执行示例：python test.py -i a.jpg,b.jpg -q 20 \n
    imgs：          接收需要压缩的图片路径，a.jpg,b.jpg \n
    quality：       默认压缩的图片质量为15，可以调整 \n
    subsampling     子采样值 默认-1
    dir：           指定要压缩的目录
    jpga：          当为1时统计转换成jpg格式，默认为0不转换
    """
    imgs = ''
    quality = 15
    subsampling = -1
    jpga = 0 #判断是否全部转换成jpg格式保存
    output = 'output'
    dir_files = '' # 要执行的目录，也就是图片文件存在的目标目录
    min_size = 0
    max_size = 0

    try:
        opts, args = getopt.getopt(argv, "hi:q:s:j:d:", ["imgs=", "quality=", "subsampling=", "jpga=", "dir=", "min-size=", "max-size="])
    except getopt.GetoptError:
        commandHelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            commandHelp()
            sys.exit()
        elif opt in ("-i", "--imgs"):
            imgs = arg
        elif opt in ("-q", "--quality"):
            quality = int(arg)
        elif opt in ("-s", "--subsampling"):
            subsampling = int(arg)
        elif opt in ("-j", "--jpga"):
            jpga = int(arg)
            print("opt_jpga: ", jpga)
        elif opt in ("-d", "--dir"):
            dir_files = arg
        elif opt in ("--min-size"):
            min_size = int(arg)
        elif opt in ("--max-size"):
            max_size = int(arg)
        
    # print('imgs:', imgs)
    # print('quality:', quality)

    
    notfound_imgs = []

    if dir_files:
        dirOfImageCompress(dir_files, quality, subsampling, notfound_imgs, jpga, output, min_size, max_size)
        return
    
    if len(imgs) > 0:
        # 创建output目录
        output_dir = Path(output)
        if output_dir.exists() == False:
            os.mkdir(output)
        for img_item in imgs.split(','):
            imageCompress(quality, subsampling, img_item, notfound_imgs, jpga, output, min_size, max_size)
    
    # TODO 向屏幕输出压缩结果信息
    # print(g_compress_data)
    if notfound_imgs:
        print('找不到的文件：', notfound_imgs)

def dirOfImageCompress(dir, quality, subsampling, notfound_imgs, jpga, output, min_size=0, max_size=0, logger=print):
    '''
    当命令行中-d不为空时，表示要在指定目录里搜索图片文件进行压缩
    '''
    for dirpath, dirname, filenames in os.walk(dir):
        # print('目录：', dirpath)

        if dirpath.endswith('/output') == False:
            # print('目录名：', dirname)
            output_dir = Path('{}/{}'.format(dirpath, output))
            if output_dir.exists() == False:
                output_dir.mkdir()

            for filename in filenames:
                # print('文件：', filename)
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.PNG'):
                    imageCompress(quality, subsampling, '{}/{}'.format(dirpath, filename), notfound_imgs, jpga, output_dir, min_size, max_size, logger)

def imageCompress(quality, subsampling, img_item, notfound_imgs, jpga, output, min_size_kb=0, max_size_kb=0, logger=print):
    '''
    把单个文件传入此方法进行压缩
    '''
    img_item_path= ''
    img_item_path = Path(os.path.abspath(img_item))
    img_item_endswith = img_item.endswith('.png') or img_item.endswith('.jpg') or img_item.endswith('.JPG') or img_item.endswith('.PNG')

    if img_item_path.is_file() and img_item_endswith:
        # 文件存在就开始压缩
        # 压缩前的文件名
        img_file_name = img_item_path.name
        img_item_data = {'fileNameBefore': img_file_name}
        img: Image.Image = Image.open(img_item_path)
        # w,h = img.size
        # print('Origin image size: %sx%s' % (w, h))
        shotname = '' # 文件名
        extension = '' # 扩展名
        (shotname, extension) = os.path.splitext(img_file_name)
        # 获取压缩前的文件byte
        byteSizeBefore = os.path.getsize(img_item_path)
        img_item_data['byteSizeBefore'] = byteSizeBefore

        # 只压缩大于300KB图片
        # if byteSizeBefore < 307200:
        #     return
        
        # 只压缩大于100KB图片
        if byteSizeBefore < 102400:
            return

        if min_size_kb > 0 and max_size_kb > 0:
            if (byteSizeBefore / 1024) < min_size_kb:
                logger(f"{img_file_name} ({convert_mb_kb(byteSizeBefore)}) is already smaller than the minimum target size of {min_size_kb}KB. Skipping compression.")
                logger("-"*70)
                return
            # 二分查找最佳质量
            low = 0
            high = 100
            best_quality = -1
            
            min_bytes = min_size_kb * 1024
            max_bytes = max_size_kb * 1024

            while low <= high:
                q = (low + high) // 2
                if q == 0: # Quality 0 is a special case
                    break

                # 创建一个临时的内存文件来保存压缩结果
                from io import BytesIO
                temp_buffer = BytesIO()

                # 复制原始图片对象，避免重复打开文件
                temp_img = img.copy()

                if temp_img.mode == 'P': # 如果是P模式（通常是PNG量化后），先转回RGB
                    temp_img = temp_img.convert('RGB')
                
                if img_item.endswith('.png') or img_item.endswith('.PNG'):
                    if jpga > 0:
                        temp_img = temp_img.convert('RGB')
                        extension = ".jpg"
                    # PNGs do not have a 'quality' parameter in the same way, this logic is mainly for JPEGs.
                    # For simplicity, we'll focus on the JPEG case as requested.
                
                temp_img.save(temp_buffer, format='JPEG', quality=q, optimize=False, subsampling=0)
                current_size = temp_buffer.tell()

                if min_bytes <= current_size <= max_bytes:
                    best_quality = q
                    break
                elif current_size > max_bytes:
                    high = q - 1
                else: # current_size < min_bytes
                    low = q + 1
            
            if best_quality != -1:
                quality = best_quality
            else:
                # 如果找不到合适的质量，默认使用一个折中的值或直接跳过
                logger(f"无法在 {min_size_kb}-{max_size_kb}KB 范围内找到合适的压缩质量，将使用默认值或最低值。")
                # 可以在这里选择一个默认行为，比如使用 high (最接近但不超过max_size)
                quality = high if high > 0 else 1 # 保证质量至少为1

        # 区别jpg、png
        if img_item.endswith('.png') or img_item.endswith('.PNG'):
            if jpga > 0:
                img = img.convert('RGB')
                extension = ".jpg"
            else:
                img = img.quantize(colors=256)


        save_file = "{}/{}{}".format(output, shotname, extension)
        img_item_data['fileNameAfter'] = save_file
        img.save(save_file, quality=quality, optimize=False, subsampling=0)
        byteSizeAfter = os.path.getsize(save_file)
        img_item_data['byteSizeAfter'] = byteSizeAfter
        g_compress_data.append(img_item_data)
        logger(f"{img_file_name} 压缩前：{convert_mb_kb(byteSizeBefore)} 压缩后：{convert_mb_kb(byteSizeAfter)}")
        logger("-"*70)
        
    else:
        # 标记不存在的文件
        notfound_imgs.append(img_item)

def convert_mb_kb(bytesize):
    """
    把byte长度转换成KB,MB
    """
    if bytesize > 0:
        bytesize = bytesize / 1024
        if bytesize < 1024:
            return "%.fKB" % bytesize
        else:
            return "%.2fMB" % (bytesize / 1024)    
    
if __name__ == "__main__":
    main(sys.argv[1:])
