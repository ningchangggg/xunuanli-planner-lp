"""手帳落地頁實拍動圖片段（2026-11-24）。iPhone HLG 先轉 bt709；丁丁俯拍橫式先轉 90 度；之後裁 4:5、加彩度 1.45、對比 1.05。"""
import subprocess,os,shutil,sys
from concurrent.futures import ThreadPoolExecutor
M="/Users/ningchang/Library/Mobile Documents/com~apple~CloudDocs/○煦暖曆/01_廣告投放/手帳/毛片/"
FPS=15
# name: (src, t0, t1, speed, cy, rotate, hdr, out_w, out_h)
C={
 'f_flat':   (M+'丁丁_新拍_1110_調色對齊麻豆/C0148.mp4', 16.5, 23.5, 1.3, 0.5, 'transpose=2', False, 1080, 1350),
 'f_flip':   (M+'麻豆_影片_0812/C0285.mp4', 12.8, 19.0, 1.4, 0.5, '', False, 1080, 1350),
 'f_window': (M+'阿寧_出外景/IMG_1137.MOV', 2.6, 9.0, 1.2, 0.45, '', True, 1080, 1350),
}
def run(item):
    n,(src,t0,t1,sp,cy,rot,hdr,ow,oh)=item
    od=f'gif/clips/{n}'; shutil.rmtree(od,ignore_errors=True); os.makedirs(od)
    pre=('colorspace=all=bt709:iall=bt2020:itrc=bt709:format=yuv420p,' if hdr else 'scale=in_color_matrix=bt709:out_color_matrix=bt709,')+(rot+',' if rot else '')
    vf=(f"{pre}setpts=PTS/{sp},fps={FPS},crop=iw:iw*{oh}/{ow}:0:(ih-iw*{oh}/{ow})*{cy},"
        f"scale={ow}:{oh}:flags=lanczos,eq=saturation=1.45:contrast=1.05")
    subprocess.run(['ffmpeg','-v','error','-ss',str(t0),'-t',str(t1-t0),'-i',src,'-vf',vf,'-q:v','2',f'{od}/%03d.jpg'],check=True,stdin=subprocess.DEVNULL)
    return n,len(os.listdir(od))
sel=sys.argv[1:] or list(C)
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(run,[(k,C[k]) for k in sel]): print(r)
