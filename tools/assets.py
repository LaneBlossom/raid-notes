import numpy as np, sys
from PIL import Image
from scipy import ndimage as nd
S='/mnt/user-data/uploads/AI work sample/'; O='/home/claude/work/img/home/'
def save(im,name,w=None,q=84):
    if w and im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    im.save(O+name+'.webp','WEBP',quality=q,method=6); print(name,im.size)
def comps(a,thr_area,dil=12):
    m=a[...,3]>20
    lab,n=nd.label(nd.binary_dilation(m,iterations=dil))
    out=[]
    for i,sl in enumerate(nd.find_objects(lab)):
        area=(lab[sl]==i+1).sum()
        if area>thr_area: out.append(sl)
    out.sort(key=lambda s:(s[0].start//150,s[1].start))
    return out
def crop_sheet(path,prefix,thr,w,dil=12,white=False):
    im=Image.open(S+path).convert('RGBA'); a=np.array(im)
    if white:  # white bg -> alpha from darkness
        g=a[...,:3].mean(-1); a[...,3]=np.clip((235-g)*3,0,255).astype(np.uint8); a[...,:3]=np.where(g[...,None]<128,a[...,:3]*0,a[...,:3])
    sls=comps(a,thr,dil)
    for k,sl in enumerate(sls):
        y0,y1=max(sl[0].start-4,0),sl[0].stop+4; x0,x1=max(sl[1].start-4,0),sl[1].stop+4
        save(Image.fromarray(a[y0:y1,x0:x1]),f'{prefix}{k}',w)
    return len(sls)
# character poses (transparent)
print('poses',crop_sheet('LaneBlossom 角色icon素材/冰藍天使騎士八姿態貼紙集.png','pose',20000,420,dil=6))
print('cry',crop_sheet('Rewink 素材/素材貼紙/水晶櫻花夢幻裝飾圖示集.png','cry',3000,160,dil=6))
print('neon',crop_sheet('Rewink 素材/素材貼紙/霓虹萌系四格圖標貼紙.png','neon',8000,200,dil=10))
print('pix',crop_sheet('Rewink 素材/素材貼紙/黑白像素圖示貼紙集.png','pix',3000,96,dil=4,white=True))
print('y2k',crop_sheet('Rewink 素材/素材貼紙/極簡黑白抽象圖標網格.png','y2k',3000,140,dil=4,white=True))
# hero banner + portraits
save(Image.open(S+'LaneBlossom 角色icon素材/雲海沉眠的羽翼騎士.png').convert('RGB'),'banner',1900,80)
for n,f in [('smile','冰藍羽翼騎士的甜笑守護.png'),('sleep','冰藍羽翼盾劍少女.png')]:
    save(Image.open(S+'LaneBlossom 角色icon素材/'+f).convert('RGB'),n,720,82)
# frames: key green -> transparent
def key(path,name,w):
    a=np.array(Image.open(S+path).convert('RGBA')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]
    gr=(g>120)&(g>r+50)&(g>b+50)
    a[...,3]=np.where(gr,0,a[...,3])
    # despill
    a[...,1]=np.where(~gr&(a[...,1]>np.maximum(a[...,0],a[...,2])),np.maximum(a[...,0],a[...,2]),a[...,1])
    # hole bbox
    ys,xs=np.where(gr); print(name,'hole',xs.min(),ys.min(),xs.max(),ys.max(),a.shape)
    save(Image.fromarray(a.astype(np.uint8)),name,w)
key('Rewink 素材/拍立得框/霓虹綠未來感鍍鉻相框.png','frame_chrome',600)
key('Rewink 素材/拍立得框/復古像素霓虹綠拍立得框.png','frame_pixel',600)
# crystal frame: green hole + baked checkerboard outside -> flood fill from border on low-sat light pixels
a=np.array(Image.open(S+'Rewink 素材/拍立得框/水晶櫻花夢幻拍立得框.png').convert('RGBA')).astype(int)
r,g,b=a[...,0],a[...,1],a[...,2]
gr=(g>120)&(g>r+50)&(g>b+50)
sat=np.max(a[...,:3],-1)-np.min(a[...,:3],-1)
chk=(sat<14)&(np.min(a[...,:3],-1)>180)
lab,_=nd.label(chk); border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
bg=np.isin(lab,list(border))
a[...,3]=np.where(gr|bg,0,255)
ys,xs=np.where(gr); print('crystal hole',xs.min(),ys.min(),xs.max(),ys.max(),a.shape)
save(Image.fromarray(a.astype(np.uint8)),'frame_crystal',600)
