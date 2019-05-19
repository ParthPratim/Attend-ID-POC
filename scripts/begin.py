import os
import ipfsapi

conn = ipfsapi.connect()

struct_newuser = {
    "DigitalID" : digital_id,
    "RGBS" : []
}
ipfs = IpfsStorage()

for persons in os.listdir("../test_dataset/train"):
    raw_imgs = []
    for ufile in os.listdir("../test_dataset/train/"+persons):
        img = Image.open(BytesIO(ufile['body']))
        pixels = list(img.getdata())
        width, height = img.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        np_img = np.array(pixels,dtype=np.uint8)
        raw_imgs.append(np_img)
    
