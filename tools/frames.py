import numpy as np
from PIL import Image
from scipy import ndimage as nd
S='/mnt/user-data/uploads/AI work sample/Rewink 素材/拍立得框/'; O='/home/claude/work/img/home/'
def green(a):
    r,g,b=a[...,0],a[...,1],a[...,2]; return (g>110)&(g>r+40)&(g>b+40)
def hole_clear(a,gr):
    # fill the region enclosed by green (interior) as transparent
    filled=nd.binary_fill_holes(nd.binary_closing(gr,iterations=25))
    a[...,3]=np.where(filled,0,a[...,3])
    edge=nd.binary_dilation(filled,iterations=3)&~filled  # soften despill
    a[...,1]=np.where(edge|(a[...,1]>np.maximum(a[...,0],a[...,2])+30),np.maximum(a[...,0],a[...,2]),a[...,1])
    ys,xs=np.where(filled); return xs.min(),ys.min(),xs.max(),ys.max()
out={}
for n,f in [('frame_chrome','霓虹綠未來感鍍鉻相框.png'),('frame_pixel','復古像素霓虹綠拍立得框.png'),('frame_crystal','水晶櫻花夢幻拍立得框.png')]:
    a=np.array(Image.open(S+f).convert('RGBA')).astype(int)
    gr=green(a)
    if n=='frame_crystal':
        mn=a[...,:3].min(-1); sat=a[...,:3].max(-1)-mn
        chk=(sat<16)&(mn>125)
        lab,_=nd.label(chk); border=np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])); border=border[border>0]
        bg=np.isin(lab,border); a[...,3]=np.where(bg,0,255)
    h=hole_clear(a,gr); H,W=a.shape[:2]
    out[n]=[round(h[0]/W*100,2),round(h[1]/H*100,2),round((W-h[2])/W*100,2),round((H-h[3])/H*100,2),W,H]
    im=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); im=im.resize((600,round(600*H/W)),Image.LANCZOS)
    im.save(O+n+'.webp','WEBP',quality=86,method=6)
print(out)
