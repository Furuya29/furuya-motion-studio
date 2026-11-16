#!/usr/bin/env python3
"""Deterministic geometric animatic for the original 15s pilot specification.

NOT final anime art, lip-sync, real contact QA, or a PC Remote Agent execution.
Input: pilot-shot-spec/0.1 JSON. Output: technical MP4 with 3D camera and 2D rig.
Dependencies: Pillow and FFmpeg. No internet, AI model, or third-party media.
"""
import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPEC = ROOT / 'docs/projeto-animacao-automatizada/piloto_15s_shot_spec_v0_1.json'

def mix(a,b,t): return a+(b-a)*t
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,k): return tuple(x*k for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(v):
    length=math.sqrt(dot(v,v))
    if length < 1e-6: raise ValueError('camera has invalid orientation')
    return mul(v,1/length)

class Camera:
    def __init__(self,position,target,focal,w,h):
        self.position=tuple(position)
        self.forward=norm(sub(target,position))
        self.right=norm(cross(self.forward,(0,0,1)))
        self.up=cross(self.right,self.forward)
        self.focal_px=w*focal/36.0
        self.width,self.height=w,h
    def project(self,p):
        d=sub(p,self.position)
        depth=dot(d,self.forward)
        if depth<=.12:return None
        return (self.width/2+self.focal_px*dot(d,self.right)/depth,
                self.height/2-self.focal_px*dot(d,self.up)/depth,depth)

def camera_at(shot,frame,w,h):
    keys=shot['camera']['keyframes']
    before,after=keys[0],keys[-1]
    for i in range(len(keys)-1):
        if keys[i]['frame']<=frame<=keys[i+1]['frame']:
            before,after=keys[i],keys[i+1]
            break
    t=max(0,min(1,(frame-before['frame'])/max(1,after['frame']-before['frame'])))
    a=[mix(x,y,t) for x,y in zip(before['position_m'],after['position_m'])]
    b=[mix(x,y,t) for x,y in zip(before['look_at_m'],after['look_at_m'])]
    return Camera(a,b,shot['camera']['focal_length_mm'],w,h)

def pt(cam,p):
    v=cam.project(p)
    return (round(v[0]),round(v[1])) if v else None

def polygon(draw,points,fill,outline=None,width=1):
    if all(p is not None for p in points):
        draw.polygon(points,fill=fill)
        if outline:draw.line(points+[points[0]],fill=outline,width=width,joint='curve')

def line3d(draw,cam,p1,p2,color,width=2):
    a,b=pt(cam,p1),pt(cam,p2)
    if a and b:draw.line((a,b),fill=color,width=width,joint='curve')

def ellipse3d(draw,cam,center,rx,rz,fill,outline=None,width=2):
    c=cam.project(center)
    if c is None:return
    sx=max(1,rx*cam.focal_px/c[2]);sy=max(1,rz*cam.focal_px/c[2]);x,y=c[:2]
    draw.ellipse((round(x-sx),round(y-sy),round(x+sx),round(y+sy)),fill=fill,outline=outline,width=width)

def scenery(draw,cam):
    for ix in range(-5,6):
        line3d(draw,cam,(ix*.5,-2,0),(ix*.5,3,0),'#314a61')
    for iy in range(-4,7):
        line3d(draw,cam,(-2.5,iy*.5,0),(2.5,iy*.5,0),'#314a61')
    for j in range(7):
        x=(j-3)*.75
        line3d(draw,cam,(x,2.1,0),(x,2.1,.75+.2*((j*3)%4)),'#33465e',2)
    ellipse3d(draw,cam,(0,0,.015),.68,.015,'#1b3649')

def puppet(draw,cam,frame,shot_id,fps):
    sec=frame/fps
    if shot_id=='P15_B':
        t=(frame-120)/119;x=mix(-.65,.48,t)
        walk=math.sin(2*math.pi*1.4*(sec-5))
        bob=.03*abs(walk)
    else:
        x=-.2 if shot_id=='P15_C' else 0
        walk=0;bob=.015*math.sin(2*math.pi*.7*sec)
    y=0;z=bob
    skin='#efb6a4';ink='#172333';hair='#1d1836';coat='#3e7793';inner='#91dfe0'
    left_foot=(x-.19+.17*walk,y-.04,max(.04,.08+.15*max(0,walk)))
    right_foot=(x+.19-.17*walk,y-.04,max(.04,.08+.15*max(0,-walk)))
    ls=(x-.30,y,1.43+z);rs=(x+.30,y,1.43+z)
    for side,foot in ((-1,left_foot),(1,right_foot)):
        knee=(x+side*.14-side*.1*walk,y,.51+z)
        line3d(draw,cam,(x+side*.12,y,.90+z),knee,coat,11)
        line3d(draw,cam,knee,foot,ink,9)
        ellipse3d(draw,cam,foot,.12,.06,'#222438')
    polygon(draw,[pt(cam,p) for p in [ls,rs,(x+.20,y,.93+z),(x-.20,y,.93+z)]],coat,ink,3)
    line3d(draw,cam,(x,y,1.42+z),(x,y,.96+z),inner,3)
    line3d(draw,cam,(x-.05,y,1.32+z),(x+.05,y,1.32+z),'#efad62',3)
    if shot_id=='P15_C':
        elbow=(x+.35,y-.04,1.18+z)
        hand=(.43,-.37,1.30+z)
    else:
        elbow=(x+.35,y-.02,1.12+.07*math.sin(sec*2)+z)
        hand=(x+.40+.05*math.sin(sec*2),y-.04,1.03+.11*math.sin(sec*2)+z)
    line3d(draw,cam,ls,(x-.40,y-.03,1.11+z),coat,13)
    line3d(draw,cam,(x-.40,y-.03,1.11+z),(x-.38,y-.05,.97+z),skin,9)
    line3d(draw,cam,rs,elbow,coat,13)
    line3d(draw,cam,elbow,hand,skin,9)
    ellipse3d(draw,cam,hand,.065,.07,skin)
    ellipse3d(draw,cam,(x,y,1.76+z),.235,.29,hair,ink,2)
    ellipse3d(draw,cam,(x,y-.022,1.73+z),.196,.245,skin,ink,2)
    blink=frame%73 in (0,1,2)
    if blink:
        for d in (-.083,.083):
            line3d(draw,cam,(x+d-.027,y-.07,1.76+z),(x+d+.027,y-.07,1.76+z),ink,3)
    else:
        for d in (-.083,.083):
            ellipse3d(draw,cam,(x+d,y-.046,1.76+z),.027,.032,ink)
    # Scripted mouth poses; do not mislabel as lip sync.
    aperture=.018+.04*abs(math.sin(sec*9.1)) if shot_id=='P15_A' else .013
    ellipse3d(draw,cam,(x,y-.06,1.625+z),.055,aperture,'#733449')
    polygon(draw,[pt(cam,p) for p in [(x-.23,y-.075,1.91+z),(x-.10,y-.10,2.015+z),
         (x+.13,y-.10,1.98+z),(x+.23,y-.075,1.91+z),(x+.11,y-.084,1.865+z),
         (x+.025,y-.105,1.91+z),(x-.10,y-.09,1.86+z)]],hair)

def microphone(draw,cam):
    # Stable world anchor and explicit ring geometry (no screen-facing billboard).
    center_x,center_y=.54,-.40
    line3d(draw,cam,(center_x,center_y,0),(center_x,center_y,1.45),'#b0bacb',7)
    line3d(draw,cam,(.35,center_y,.03),(.73,center_y,.03),'#b0bacb',5)
    ring=lambda angle,z:(center_x+.105*math.cos(angle),center_y+.105*math.sin(angle),z)
    facets=[]
    for j in range(16):
        a=j*2*math.pi/16;b=(j+1)*2*math.pi/16
        world=[ring(a,1.38),ring(b,1.38),ring(b,1.65),ring(a,1.65)]
        facets.append((sum(cam.project(p)[2] for p in world),[pt(cam,p) for p in world],j))
    for _,points,j in sorted(facets,reverse=True):
        k=int(170+33*math.cos(j*2*math.pi/16))
        polygon(draw,points,(k,k+2,min(255,k+15)),'#3b465b',1)
    for z in (1.45,1.5,1.55):
        points=[pt(cam,ring(j*2*math.pi/48,z)) for j in range(49)]
        if all(p is not None for p in points):draw.line(points,fill='#738399',width=1)

def render_frame(spec,frame,width,height):
    shot=next(s for s in spec['shots'] if s['start_frame']<=frame<s['end_frame'])
    cam=camera_at(shot,frame,width,height)
    im=Image.new('RGB',(width,height),'#101a2a');draw=ImageDraw.Draw(im)
    for y in range(height):
        t=y/height
        draw.line(((0,y),(width,y)),fill=(int(14+14*t),int(25+19*t),int(42+16*t)))
    scenery(draw,cam)
    if shot['id']=='P15_C':microphone(draw,cam)
    puppet(draw,cam,frame,shot['id'],spec['timeline']['fps'])
    draw.rectangle((10,8,width-10,36),fill='#121e31')
    name={'P15_A':'RIG FACIAL','P15_B':'MOVIMENTO + CAMERA','P15_C':'CAMERA + MICROFONE'}[shot['id']]
    draw.text((20,15),f"PILOTO 15s | {shot['id']} / {name}",fill='#f0e2cc')
    draw.text((20,height-30),
        f"FRAME {frame:03d}/{spec['timeline']['total_frames']-1} | {frame/spec['timeline']['fps']:05.2f}s | BLOCKING TECNICO / NAO E ARTE FINAL",
        fill='#a2bfcb')
    return im

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec',type=Path,default=DEFAULT_SPEC)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--width',type=int,default=640)
    parser.add_argument('--height',type=int,default=360)
    args=parser.parse_args(argv)
    if min(args.width,args.height)<180 or args.width%2 or args.height%2:
        parser.error('width/height must be even and at least 180')
    if not shutil.which('ffmpeg'):parser.error('ffmpeg is required on PATH')
    from validate_shot_spec import validate
    spec=json.loads(args.spec.read_text(encoding='utf-8'))
    errors=validate(spec)
    if errors:parser.error('Invalid shot spec: '+'; '.join(errors))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{args.width}x{args.height}','-r',str(spec['timeline']['fps']),
         '-i','-','-c:v','libx264','-preset','veryfast','-crf','23',
         '-pix_fmt','yuv420p','-movflags','+faststart',str(args.out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(spec['timeline']['total_frames']):
            proc.stdin.write(render_frame(spec,i,args.width,args.height).tobytes())
        proc.stdin.close()
        err=proc.stderr.read().decode('utf-8','replace')
        if proc.wait()!=0:raise RuntimeError('FFmpeg: '+err[-1200:])
    except BaseException:
        if proc.poll() is None:proc.kill()
        proc.wait()
        args.out.unlink(missing_ok=True)
        raise
    print(f"RENDERED_TECHNICAL_ANIMATIC: {args.out} ({spec['timeline']['total_frames']} frames)")

if __name__=='__main__':main()
