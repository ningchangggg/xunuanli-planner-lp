"""把 hw/steps/<name>/NN.png（每多一筆的累積圖）做成逐筆擦出的動畫格，10fps。"""
import os,sys,shutil
import numpy as np
from PIL import Image
SUB=4; HOLD0=6; HOLDS=1; HOLDEND=22
def run(name):
    sd=f'hw/steps/{name}'; fs=sorted(os.listdir(sd)); ims=[np.asarray(Image.open(f'{sd}/{f}').convert('RGB'),np.int16) for f in fs]
    od=f'gif/clips/hw_{name}'; shutil.rmtree(od,ignore_errors=True); os.makedirs(od); n=[0]
    def save(a):
        im=Image.fromarray(a.astype(np.uint8)); im=im.resize((1080,round(im.height*1080/im.width)),Image.LANCZOS)
        n[0]+=1; im.save(f'{od}/{n[0]:03d}.jpg',quality=90)
    for _ in range(HOLD0): save(ims[0])
    for a,b in zip(ims,ims[1:]):
        d=np.abs(a-b).sum(2)>18; ys,xs=np.nonzero(d)
        if len(xs)==0: continue
        x0,x1=xs.min(),xs.max()+1; y0,y1=ys.min(),ys.max()+1
        tall=(y1-y0)>(x1-x0)*1.6
        for k in range(1,SUB+1):
            t=k/SUB; c=a.copy()
            if tall:
                yy=int(y0+(y1-y0)*t); c[y0:yy]=b[y0:yy]
            else:
                xx=int(x0+(x1-x0)*t); c[:,x0:xx]=b[:,x0:xx]
            save(c)
        for _ in range(HOLDS): save(b)
    for _ in range(HOLDEND): save(ims[-1])
    print(name,n[0])
for nm in (sys.argv[1:] or ['week','grid','month','reflect','year','vision']): run(nm)
