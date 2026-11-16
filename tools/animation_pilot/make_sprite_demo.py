#!/usr/bin/env python3
"""Create original geometric PNG layers and a demo JSON rig (no third-party assets)."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw

def save(path,size,drawfn):
    image=Image.new('RGBA',size,(0,0,0,0))
    drawfn(ImageDraw.Draw(image))
    image.save(path)

def make(out):
    out=Path(out)
    assets=out/'assets'
    assets.mkdir(parents=True,exist_ok=True)
    def background(draw):
        for y in range(360):
            draw.line([(0,y),(640,y)],fill=(16+y//29,31+y//18,48+y//15,255))
        for y in range(160,360,40):
            draw.line([(0,y),(640,y)],fill=(70,96,113,100),width=1)
        for x in range(0,640,80):
            draw.line([(x,165),(x,360)],fill=(70,96,113,100),width=1)
    save(assets/'background.png',(640,360),background)
    save(assets/'torso.png',(130,150),lambda d:(
        d.polygon([(25,17),(105,17),(127,136),(3,136)],fill='#367ca3',outline='#162b48',width=4),
        d.line([(65,20),(65,137)],fill='#bedddb',width=4),
        d.line([(50,35),(80,35)],fill='#efaa70',width=4)))
    save(assets/'head.png',(140,145),lambda d:(
        d.ellipse((15,2,125,136),fill='#251f3d',outline='#17152a',width=3),
        d.ellipse((26,21,114,123),fill='#f4bd9f',outline='#383044',width=3),
        d.polygon([(19,34),(55,13),(85,28),(117,24),(110,50),(80,43),(65,57),(45,42),(25,55)],fill='#26213d')))
    save(assets/'arm.png',(46,115),lambda d:(
        d.rounded_rectangle((7,7,39,97),radius=13,fill='#3c86a0',outline='#182d47',width=3),
        d.ellipse((10,84,36,112),fill='#f4bd9f',outline='#9f697b',width=2)))
    save(assets/'eye_open.png',(18,12),lambda d:d.ellipse((4,0,15,11),fill='#262039'))
    save(assets/'eye_closed.png',(18,12),lambda d:d.line((2,7,16,7),fill='#262039',width=3))
    save(assets/'mouth_closed.png',(26,16),lambda d:d.arc((3,0,23,12),0,180,fill='#a24c63',width=3))
    save(assets/'mouth_open.png',(26,16),lambda d:d.ellipse((6,1,20,15),fill='#713149'))
    def part(name,sprite,parent,pivot,offset,layer):
        return dict(id=name,sprite='assets/'+sprite,parent=parent,pivot=pivot,offset=offset,layer=layer)
    parts=[
        part('background','background.png',None,[320,180],[320,180],-10),
        part('torso','torso.png',None,[65,65],[320,232],0),
        part('arm_l','arm.png','torso',[22,20],[-55,-40],1),
        part('arm_r','arm.png','torso',[22,20],[55,-40],1),
        part('head','head.png','torso',[70,112],[0,-67],2),
        part('eye_l','eye_open.png','head',[9,6],[-20,-45],3),
        part('eye_r','eye_open.png','head',[9,6],[20,-45],3),
        part('mouth','mouth_closed.png','head',[13,8],[0,-16],4),
    ]
    def track(part,property_,values):
        return dict(part=part,property=property_,keys=[dict(frame=f,value=v) for f,v in values])
    tracks=[
        track('head','rotation_deg',[(0,0),(18,-5),(35,4),(52,-2),(71,0)]),
        track('arm_l','rotation_deg',[(0,-10),(22,0),(42,-13),(71,-10)]),
        track('arm_r','rotation_deg',[(0,12),(18,28),(40,8),(71,12)]),
        track('torso','offset_y',[(0,0),(18,-2),(36,0),(54,2),(71,0)]),
        track('mouth','sprite',[(0,'assets/mouth_closed.png'),(6,'assets/mouth_open.png'),
             (12,'assets/mouth_closed.png'),(17,'assets/mouth_open.png'),
             (26,'assets/mouth_closed.png'),(39,'assets/mouth_open.png'),
             (45,'assets/mouth_closed.png'),(55,'assets/mouth_open.png'),
             (63,'assets/mouth_closed.png')]),
        track('eye_l','sprite',[(0,'assets/eye_open.png'),(30,'assets/eye_closed.png'),(33,'assets/eye_open.png')]),
        track('eye_r','sprite',[(0,'assets/eye_open.png'),(30,'assets/eye_closed.png'),(33,'assets/eye_open.png')]),
    ]
    rig=dict(version='sprite-rig/0.1',name='Sample geometry only; not anime art',
             canvas=[640,360],fps=24,frames=72,parts=parts,tracks=tracks)
    (out/'rig.json').write_text(json.dumps(rig,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('SAMPLE_SPRITES_CREATED',out)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    make(args.out)

if __name__=='__main__':
    main()
