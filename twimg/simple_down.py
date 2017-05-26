from urllib import request


def down(source, output):
    # 画像ソースを開く
    response = request.urlopen(source)

    # HTTPステータスコードが200でないなら0を返す
    if response.code != 200:
        raise Exception('down_img error: failed to download from given link')

    # 保存先をバイナリ形式で開く
    with open(output, "wb") as fout:
        # 保存先に画像データを書き込む
        fout.write(response.read())

    # 1を返す
    return 1
