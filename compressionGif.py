import imageio
from PIL import Image,ImageSequence

def compression_gif(gifName):
    image_list = []
    im = Image.open(gifName)

    #取每一偵進行壓縮，存入image_list
    for frame in ImageSequence.Iterator(im):
        frame = frame.convert('RGB')
        w,h = frame.size[:2]
        frame.thumbnail((int(w*0.7),int(h*0.7)))
        image_list.append(frame)

    #計算偵頻率
    duration = (im.info)['duration']/1000

    #讀取image_list 合併成gif
    imageio.mimsave('resultCompression.gif',image_list,duration=duration)
