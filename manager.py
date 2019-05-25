import cv2
from utils.crop_join import slice, join
from secret_sharing.secret_sharing import share_secret, reconstruct_secret
from PIL import Image
from stega.embed import embed
from stega.extract import extract
from aes.aes import AESCipher
import time
import os
import gzip


def encode(img, msg, threshold, nshares, output):
    start_time = time.time()
    try:
        shares = share_secret(threshold, nshares, msg, 'secret42')
    except:
        return 'Не удалось разделить секрет.<br>'
    size = 0
    for i in range(len(shares)):
        size += len(shares[i])
    img_full = cv2.imread(img)
    height, width, channels = img_full.shape
    diff = (height * width) / (size * 8)
    if diff >= 5:
        diff = 5
    if diff >= 1:
        for j in range(int(diff) - 2):
            for i in range(len(shares)):
                shares.append(shares[i])
        titles = slice(img, len(shares))

        angle = [0, 1, 2, 3]
        curr_angle_ind = 0
        try:
            for i in range(0, len(shares)):
                msg = str(shares[i].decode('latin-1'))
                in_img = cv2.imread(titles[i].filename)
                encoded = embed(in_img, msg, angle[curr_angle_ind])
                if curr_angle_ind == 3:
                    curr_angle_ind = 0
                else:
                    curr_angle_ind += 1
                cv2.imwrite(titles[i].filename, encoded)
                titles[i].image = Image.open(titles[i].filename)

            result = join(titles)
            result.save(output)

            for i in range(len(titles)):
                os.remove(titles[i].filename)
        except:
            return 'Не удалось встроить данные.<br>'

        try:
            aes = AESCipher()
            key = aes.encrypt(str(len(shares)))
            str_key = key.decode()
            key_path = os.path.dirname(img) + '/key'
            f_key = open(key_path, 'w')
            f_key.write(str_key)
            f_key.close()
        except:
            return 'Не удалось сформировать ключ.<br>'

    else:
        return 'Размер изображения слишком мал для данного сообщения.<br>'
    end_time = time.time()
    return 'Встраивание прошло успешно.<br>' + 'Потребовалось времени: %.2f сек.' % (end_time - start_time) + '<br>'


def decode(img, key_path, output):
    start_time = time.time()
    try:
        aes = AESCipher()
        f_key = open(key_path, 'r')
        key = f_key.read()
        b_key = key.encode()
        nshares = int(aes.decrypt(b_key))
        f_key.close()
    except:
        return 'Не удалось получить ключ.<br>'

    titles = slice(img, nshares)
    shares = []

    angle = [0, 1, 2, 3]
    curr_angle_ind = 0
    try:
        for i in range(0, nshares):
            img = cv2.imread(titles[i].filename)
            raw = extract(img, angle[curr_angle_ind])
            if curr_angle_ind == 3:
                curr_angle_ind = 0
            else:
                curr_angle_ind += 1
            if raw is None:
                shares.append(None)
            else:
                shares.append(raw.encode('latin1'))

        result = reconstruct_secret(shares)

        msg = result.decode()
        ext = ''
        c = 0
        for m in msg:
            if m == ':':
                break
            else:
                ext += m
                c += 1
        c += 1
        msg = msg[c:]
        msg = msg.encode('latin-1')

        msg = gzip.decompress(msg)

        f = open(output + ext, 'wb')
        f.write(msg)
        f.close()

        for i in range(len(titles)):
            os.remove(titles[i].filename)
    except:
        return 'Не удалось восстановить секрет.<br>'

    end_time = time.time()
    return 'Расшифровка прошла успешно.<br>' + 'Потребовалось времени: %.2f сек.' % (end_time - start_time) + '<br>'
