from PIL import Image
import subprocess
import os
from contextlib import contextmanager
import time
import base64
import logging
import requests
from io import BytesIO

logger = logging.getLogger(__name__)


@contextmanager
def timer(name):
    start = time.time()
    yield
    logger.info(f'[{name}] done in {time.time() - start:.2f} s')


def encode_image(file: str) -> str:
    """将图片编码为 Base64"""
    with timer(f'encode [{file}] to base64'):
        with open(file, 'rb') as f:
            return base64.encodebytes(f.read()).decode('utf8').replace('\n', '').replace('\r', '')


def runcmd(command):
    ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding="utf-8", timeout=1)
    if ret.returncode == 0:
        # print("success:",ret)
        return ret
    else:
        raise ValueError("error: " + str(ret))


def check_pngquant_bin():
    try:
        runcmd('pngquant --help')
    except Exception as e:
        print('error:', e)
        print('用于图片压缩的工具 pngquant 不存在，请先在 https://pngquant.org/ 上下载并安装！！！')
        os._exit(1)


def compress_image_by_zipflipng(src: str):
    from zopflipng import png_optimize

    with open(src, 'rb') as fp:
        data = fp.read()
    result, code = png_optimize(data)
    # if code ==0 ,png compression success
    if code == 0:
        # save png
        with open(src, 'wb') as f:
            f.write(result)
            f.close()
    else:
        logger.error('optimize by zopfilong failed, ignore this image')


def png2webp(src: str, quality=30):
    """ PNG 转 WEBP
    ---
    目前是压缩最佳方式
    """
    with timer('convert png to webp'):
        from PIL import Image
        im = Image.open(src)
        dst = src.replace('.png', ".webp")
        im.save(dst, "WEBP", quality=quality)
        return dst


def png2avif(src: str, quality: int = 30):
    """目前最新的图片格式，据说比 webp 更轻
    但考虑到兼容性，目前还是暂时使用 webp
    ---
    经过测试，极限状态下比 webp 更强，可以用于缩略图
    """
    from PIL import Image
    import pillow_avif
    with timer('convert png to avif'):
        im = Image.open(src)
        dst = src.replace('.png', ".avif")
        im.save(dst, 'AVIF', quality=quality)
    return dst


def compress_image(file: str, zop_enable=False) -> str:
    """压缩图片，返回图片路径
    pngquant: 有损压缩，压缩率高，图片会失真，但速度快
    zopflipng: 无损压缩，压缩率低，图片不失真，但速度慢，适合后台慢慢运行

    ---
    经过比对，不通过压缩，直接将 png 转变为 webp, 能同时保持图片清晰度及最大压缩率
    """
    import pngquant
    dst = file.replace('.png', '.compressed.png')
    import time
    with timer('Image compress by pngquant'):
        pngquant.quant_image(file, dst=dst)
    if zop_enable:
        with timer('Image decompress by zopflipng'):
            compress_image_by_zipflipng(dst)
    return dst


def make_thumbnail(image: str, quality=10) -> str:
    """ 制作缩略图 """
    return 'data:image/cvif;base64, ' + encode_image(png2avif(image, quality=quality))


def handle_image(image: Image.Image, webp_quality=50, avif_quality=10):
    from io import BytesIO
    import base64
    # to webp
    webp_buf = BytesIO()
    logger.info(f'{webp_quality=}')
    image.save(webp_buf, 'WEBP', quality=webp_quality)
    # to avif (thumbnail)
    import pillow_avif as _
    avif_buf = BytesIO()
    image.save(avif_buf, 'AVIF', quality=avif_quality)
    # to base64

    def to_base64(b: BytesIO):
        return base64.b64encode(b.getvalue()).decode('utf8').replace('\n', '').replace('\r', '')
    result = to_base64(webp_buf)
    suffix = 'webp'
    thumbnail = 'data:image/cvif;base64, ' + to_base64(avif_buf)
    return (
        result,
        suffix,
        thumbnail
    )


if __name__ == '__main__':
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    check_pngquant_bin()
    # print(encode_image('assets/demo.png'))
    # dst = compress_image('assets/demo.png', zop_enable=True)
    png2webp('assets/demo.png', quality=1)

    def test_avif_to_base64():
        """ 测试 avif 图片转 base64 后，文件大小"""
        avif = png2avif('assets/demo.png', quality=10)
        encoded = encode_image(avif)
        print(f'{len(encoded)/1024} kB')
    test_avif_to_base64()


def read_file_to_buffer(file_path):
    # 读取文件到缓冲区
    with open(file_path, 'rb') as file:
        buffer = BytesIO(file.read())
    return buffer


def upload_file_from_buffer(buffer, ext, target_url, worker_token):
    # 将缓冲区中的数据作为文件上传
    files = {'file': (f'filename.{ext}', buffer,
                      'application/octet-stream'), 'worker_token': worker_token}

    # 发送请求
    response = requests.post(target_url, files=files)

    # 检查请求是否成功
    if response.status_code == 200:
        print("文件上传成功！")
        # 可以在这里处理服务器返回的数据
        return response.json()
    else:
        print(f"文件上传失败，状态码：{response.status_code}")
        # 如果需要，可以处理错误信息
        print(response.text)
