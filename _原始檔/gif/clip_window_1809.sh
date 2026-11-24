#!/bin/bash
# 開窗封面動圖 v8：阿寧 IMG_1809 100.2–104.4s（照片從左推進三格窗），1.2 倍，iPhone HLG 轉 bt709，裁 864x1080 放大成 1080x1350
F="/Users/ningchang/Library/Mobile Documents/com~apple~CloudDocs/○煦暖曆/01_廣告投放/手帳/毛片/阿寧_毛片/IMG_1809.MOV"
cd "$(dirname "$0")/.."; rm -rf gif/clips/f_window; mkdir -p gif/clips/f_window
ffmpeg -v error -ss 100.2 -t 4.2 -i "$F" -vf "colorspace=all=bt709:iall=bt2020:itrc=bt709:format=yuv420p,setpts=PTS/1.2,fps=15,crop=864:1080:216:468,scale=1080:1350:flags=lanczos,eq=saturation=1.45:contrast=1.05" -q:v 2 gif/clips/f_window/%03d.jpg </dev/null
ls gif/clips/f_window | wc -l
