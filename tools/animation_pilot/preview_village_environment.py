#!/usr/bin/env python3
"""Animação técnica de atmosfera para still autoral existente.

Gera um MP4 verificável (neve em profundidade, fumaça, variação luminosa
em focos de fogo e movimento leve de câmera). NÃO anima corpos/personagens
nem substitui a arte original. Nenhum serviço de IA, rede ou GPU necessária.

Uso:
 python preview_ambiente_vila.py --input village.png --output preview.mp4 \
     --duration 4 --width 960 --height 540 --fps 24
Dependências: Python, numpy, opencv-python, FFmpeg, FFprobe.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import cv2
import numpy as np


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def render(input_path, output_path, duration, width, height, fps, seed=199):
    src = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
    if src is None:
        raise ValueError('Imagem fonte não pôde ser aberta.')
    H, W = src.shape[:2]
    if width % 2 or height % 2:
        raise ValueError('A resolução precisa ser par para libx264/yuv420p')
    frames = int(round(duration * fps))
    if frames < 2:
        raise ValueError('O piloto precisa de pelo menos 2 frames.')

    # Escala com cobertura. O movimento de câmera só expande em ~2% e
    # preserva a topologia dos prédios (sem warping de estruturas).
    base_scale = max(width / W, height / H)
    rng = np.random.default_rng(seed)
    # Cada floco tem posição e velocidade persistentes: não há reposição
    # aleatória por frame nem 'flicker' por reamostragem de sprite.
    counts = [240, 100, 32]
    scales = [0.5, 1.0, 2.15]
    snow = []
    for n, sc in zip(counts, scales):
        x = rng.uniform(0, width, n).astype(np.float32)
        y = rng.uniform(0, height, n).astype(np.float32)
        sx = rng.uniform(-6, 11, n).astype(np.float32) * sc
        sy = rng.uniform(23, 52, n).astype(np.float32) * sc
        r = rng.uniform(.7, 1.35, n).astype(np.float32) * sc
        lum = rng.uniform(.36, .80, n).astype(np.float32)
        snow.append((x, y, sx, sy, r, lum, sc))

    # Coordenadas normalizadas de focos de fogo observáveis na referência.
    fire_centers = [(0.085,0.27),(.36,.42),(.50,.18),(.64,.27),(.78,.58),(.59,.93)]
    # Três colunas de fumaça já visíveis no original, para continuidade.
    smoke_origins = [(0.33, 0.25),(.49,.22),(.61,.17)]
    smoke_overlay = np.zeros((height,width,3),dtype=np.uint8)
    glow = np.zeros((height,width,3),dtype=np.uint8)

    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y',
           '-f','rawvideo','-pix_fmt','bgr24', '-s',f'{width}x{height}',
           '-r',str(fps), '-i','-', '-an','-c:v','libx264', '-preset','veryfast',
           '-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(output_path)]
    proc = subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    sample_sigs=[]
    try:
        for f in range(frames):
            t=f/fps
            progress=t/max(duration,1e-6)
            zoom=1.012 + 0.018*progress
            scale=base_scale*zoom
            # Câmera diminui lentamente a distância; pequena pan horizontal.
            sw=int(math.ceil(W*scale)); sh=int(math.ceil(H*scale))
            scaled=cv2.resize(src,(sw,sh),interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR)
            pan=int(4*progress)
            x0=max(0,(sw-width)//2 + pan); y0=max(0,(sh-height)//2 - int(2*progress))
            x0=min(x0,sw-width); y0=min(y0,sh-height)
            frame=scaled[y0:y0+height,x0:x0+width].copy()
            if frame.shape[:2] != (height,width):
                raise RuntimeError('Falha de crop da câmera')

            # Sombra de fumaça de baixa opacidade, sem alteração estrutural.
            smoke_overlay.fill(0)
            for j,(fx,fy) in enumerate(smoke_origins):
                ux=fx*width+11*math.sin(.50*t+j)
                uy=fy*height-18*t
                for layer in range(4):
                    ox=ux + math.sin(t*0.9+j*.8+layer)*13 + layer*5
                    oy=uy-layer*19 - 6*math.sin(.35*t+layer)
                    rx=int(18+8*layer); ry=int(16+8*layer)
                    cv2.ellipse(smoke_overlay,(int(ox),int(oy)),(rx,ry),0,0,360,(220,220,220),-1,cv2.LINE_AA)
            smoke_overlay[:]=cv2.GaussianBlur(smoke_overlay,(0,0),sigmaX=13,sigmaY=12)
            # Não desenhar nuvens artificiais pesadas: densidade máxima ~8%.
            a=cv2.cvtColor(smoke_overlay,cv2.COLOR_BGR2GRAY).astype(np.float32)*(0.11/255)
            gray_smoke=np.array((56,63,71),dtype=np.float32)
            frame=(frame.astype(np.float32)*(1-a[...,None]) + gray_smoke*a[...,None]).astype(np.uint8)

            # Oscilação espacial das brasas já existentes: calor local sutil.
            glow.fill(0)
            for j,(fx,fy) in enumerate(fire_centers):
                intensity=0.65+0.35*math.sin(7.6*t+j*1.94)+0.14*math.sin(12.4*t+j)
                power=int(34*max(.15,intensity))
                p=(int(fx*width),int(fy*height))
                cv2.circle(glow,p,int(7+3*max(.15,intensity)),(0,int(power*.50),power),-1,cv2.LINE_AA)
            glow=cv2.GaussianBlur(glow,(0,0),sigmaX=9)
            frame=cv2.add(frame,glow)
            # Neve separada em 3 planos, persistência temporal de cada partícula.
            # Não movemos pedras, edifícios, corpos ou faixas da imagem original.
            snow_layer=np.zeros_like(frame)
            for xs,ys,vxs,vys,rs,lum,sc in snow:
                xx=(xs+vxs*t+5*np.sin(.55*t+ys*.03)*sc)%width
                yy=(ys+vys*t)%height
                for x,y,r,a in zip(xx,yy,rs,lum):
                    cx=int(x); cy=int(y)
                    if sc>1.5:
                        cv2.line(snow_layer,(cx,cy),(cx-int(sc*1.8),max(0,cy-int(sc*3))),
                                 (int(206*a),int(215*a),int(230*a)),max(1,int(r)),cv2.LINE_AA)
                    else:
                        cv2.circle(snow_layer,(cx,cy),max(1,int(r)),
                                   (int(205*a),int(218*a),int(237*a)),-1,cv2.LINE_AA)
            frame=cv2.add(frame,snow_layer)
            if f in (0,frames//2,frames-1):
                sample_sigs.append(hashlib.sha256(frame.tobytes()).hexdigest())
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        err=proc.stderr.read().decode('utf-8',errors='replace')
        ret=proc.wait()
        if ret:
            raise RuntimeError(f'ffmpeg falhou ({ret}): {err[-1300:]}')
    except Exception:
        if proc.poll() is None: proc.kill()
        raise
    result=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries',
                           'stream=width,height,r_frame_rate,nb_frames:format=duration,size',
                           '-of','json',str(output_path)],capture_output=True,text=True,check=True)
    data=json.loads(result.stdout)
    return {
        'mode':'VALIDACAO_TECNICA_DE_AMBIENTE; NAO E ANIMACAO_COMPLETA',
        'source':str(input_path),'source_sha256':sha256_file(input_path),
        'video':str(output_path),'video_sha256':sha256_file(output_path),
        'ffprobe':data,'frames_requested':frames,'sample_frame_sha256':sample_sigs,
        'seed':seed,'effects':['snow_particles_temporally_persistent','smoke_animated_overlay',
                               'ember_local_luminance_flicker','camera_slow_dolly'],
        'source_integrity':'Original preservado, quadro de vídeo derivado não sobrescreve fonte',
        'limitations':['Prédios e personagens continuam estáticos na fotografia fonte',
                       'Não inclui geometria 3D, personagens com rig, parallax real por camada, lip-sync ou atuação',
                       'Qualidade cinematográfica depende de aceite humano e provas posteriores',
                       'Teste local da sessão, não no Windows/PCRA do usuário']
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--duration',type=float,default=4)
    p.add_argument('--fps',type=int,default=24)
    p.add_argument('--width',type=int,default=960)
    p.add_argument('--height',type=int,default=540)
    p.add_argument('--seed',type=int,default=199)
    args=p.parse_args()
    result=render(args.input,args.output,args.duration,args.width,args.height,args.fps,args.seed)
    report=args.output.with_suffix('.qa.json')
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'report':str(report),'video':str(args.output),
                      'size_bytes':args.output.stat().st_size,'ffprobe':result['ffprobe']},ensure_ascii=False))

if __name__=='__main__':
    main()