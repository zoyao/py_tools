from openpyxl import Workbook
import datetime
import base64
from openpyxl.drawing.image import Image
from io import BytesIO


def get_excel_column(n: int) -> str:
    assert (isinstance(n, int) and n > 0)
    num = [chr(i) for i in range(65, 91)]
    ret = []
    while n > 0:
        n, m = divmod(n-1, len(num))
        ret.append(num[m])
    return ''.join(ret[::-1])


def csv_to_xlsx_pd(source_path: str, save_path: str, encode='utf-8'):
    """将csv 转为 excel（.xlsx格式）
    如果不需要可以把计时相关代码删除
    Args:
        source_path:str 来源文件路径
        save_path:str 保存文件路径，需要包含保存的文件名，文件名需要是 xlsx 格式的
        encode='utf-8' 默认编码，可以改为需要的编码如gbk
    """
    print('开始处理%s' % source_path)
    curr_time = datetime.datetime.now()
    print(curr_time)

    f = open(source_path, 'r', encoding=encode)
    # 创建一个workbook 设置编码
    workbook = Workbook()
    # 创建一个worksheet
    worksheet = workbook.active
    workbook.title = 'sheet'

    images = []
    for i, line in enumerate(f):
        row = line.split(',')
        for j, word in enumerate(row):
            word = row[j]
            if len(word) > 100:
                image_excel = base64.b64decode(word)
                try:
                    image = Image(BytesIO(image_excel))
                    row[j] = "image(" + str(i) + "," + str(j) + ")"
                    images.append((image, (get_excel_column(j + 1), i + 1)))
                except Exception as e:
                    print(e)
        worksheet.append(row)
    for image in images:
        x = image[1][0]
        y = image[1][1]
        ratio = 0.5
        wh = image[0].width * ratio, image[0].height * ratio
        image[0].width, image[0].height = wh
        worksheet.column_dimensions[x].width, worksheet.row_dimensions[y].height = wh
        worksheet.add_image(image[0], x + str(y))

    workbook.save(save_path)

    print('处理完毕')
    curr_time2 = datetime.datetime.now()
    print(curr_time2 - curr_time)


if __name__ == '__main__':
    source = 'source.csv'
    save = 'result.xlsx'
    csv_to_xlsx_pd(source_path=source, save_path=save, encode='utf-8')
