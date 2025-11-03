import os,sys,time,random
from PIL import Image,ImageEnhance
# GPU/CUDA detection and fallback to NumPy
try:
    import numpy as np
    import cupy as cp
    gpu=cp.cuda.Device(0);gpu_on=True
    print("\033[1;32m🚀 GPU Found: NVIDIA CUDA Device\033[0m")
except:
    import numpy as np
    gpu_on=False;print("\033[1;33m❌ GPU Not Detected - Using CPU\033[0m")
try:import cv2
except:cv2=None
# Clear-screen helper for Windows/Linux terminals
def clr():os.system('cls' if os.name=='nt' else 'clear')
    
# MODE 1: Image to ASCII - setup and user choices
def m1():
    print("\n"+"="*70+"\n\033[1;36mMODE 1: IMAGE → ASCII ART 🎨\033[0m\n"+"="*70)
    pth=input("\n📁 Enter image path: ").strip().strip('"')
    if not os.path.exists(pth):print("\033[1;31m⚠️  File not found!\033[0m");input("Press Enter...");return
    print("\n\033[1;35m📊 Select Resolution:\033[0m")
    print("  [1] Fast    (120 cols)  [2] Medium (200 cols)  [3] Good (300 cols)")
    print("  [4] Better  (400 cols)  [5] Excellent (500 cols)  [6] Ultra (600 cols)")
    res_map={1:120,2:200,3:300,4:400,5:500,6:600}
    res_ch=input("\n> Choice (1-6): ").strip()
    wid=res_map.get(int(res_ch) if res_ch.isdigit() else 3,300)
    print("\n\033[1;35m🎨 Select Mode:\033[0m  [1] RGB (Color)  [2] BW (Grayscale)")
    mod=input("> Choice: ").strip()
    rgb=mod!='2'
    print("\n\033[1;35m✨ Edit Options:\033[0m  [1] Default  [2] Edit (Brightness/Contrast)")
    edt=input("> Choice: ").strip()=='2'
    bri,con=0,1.0
    if edt:
        bri=float(input("\n💡 Brightness (-50 to 50, 0=normal): ") or 0)
        con=float(input("🔆 Contrast (0.5 to 2.0, 1.0=normal): ") or 1.0)
    print(f"\n\033[1;36m{'🚀 GPU ACTIVE' if gpu_on else '⏳ CPU PROCESSING'}\033[0m - Converting image...")
    st=time.time()
    try:
        img=Image.open(pth).convert('RGB')
        if edt:
            img=ImageEnhance.Brightness(img).enhance(1+bri/100)
            img=ImageEnhance.Contrast(img).enhance(con)
        asp=img.height/img.width
        hgt=int(wid*asp*0.55)
        img=img.resize((wid,hgt))
        # Convert image on GPU if available, else CPU path
        if gpu_on:
            np_img=np.array(img)
            pix=cp.asarray(np_img)
            if rgb:
                r,g,b=pix[:,:,0],pix[:,:,1],pix[:,:,2]
                gry=(0.299*r+0.587*g+0.114*b).astype(cp.uint8)
            else:
                gry=cp.asarray(np.array(img.convert('L')))
            gry=cp.asnumpy(gry)
            if rgb:pix=cp.asnumpy(pix)
        else:
            if rgb:
                pix=np.array(img)
                gry=np.dot(pix[...,:3],[0.299,0.587,0.114]).astype(np.uint8)
            else:gry=np.array(img.convert('L'))
        chr=" .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        # Build ANSI-colored or plain ASCII string
        asc=""
        for y in range(hgt):
            for x in range(wid):
                val=gry[y,x]
                idx=int((val/255)*(len(chr)-1))
                if rgb:
                    r,g,b=int(pix[y,x,0]),int(pix[y,x,1]),int(pix[y,x,2])
                    asc+=f"\033[38;2;{r};{g};{b}m{chr[idx]}\033[0m"
                else:asc+=chr[idx]
            asc+="\n"
        # Build plain (no ANSI) version for saving
        plain=[]
        for y in range(hgt):
            row_chars=[chr[int((gry[y,x]/255)*(len(chr)-1))] for x in range(wid)]
            plain.append(''.join(row_chars))
        plain='\n'.join(plain)+"\n"
        et=time.time()-st
        clr(); print("\n"+asc)
        print(f"Done in {et:.2f}s | {wid}x{hgt} | {'RGB' if rgb else 'BW'} | {'GPU' if gpu_on else 'CPU'}")
        # Save option
        sv=input("Save ASCII to file? (y/N): ").strip().lower()=="y"
        if sv:
            print("\n[1] Plain .txt  [2] ANSI color .ans")
            fm=input("> ").strip()
            use_color=(fm=='2' and rgb)
            def_path=(os.path.splitext(os.path.basename(pth))[0])+("_color.ans" if use_color else "_ascii.txt")
            out_p=input(f"Output path [{def_path}]: ").strip().strip('"')
            if not out_p: out_p=def_path
            try:
                with open(out_p,'wb') as f:
                    data=(asc if use_color else plain).encode('utf-8')
                    f.write(data)
                print(f"\033[1;32m✅ Saved to {out_p}\033[0m")
            except Exception as e:
                print(f"\033[1;31m⚠️  Save failed: {e}\033[0m")
    except Exception as e:print(f"\033[1;31m⚠️  Error: {e}\033[0m")
    input("\n[Enter to continue]")
    
# MODE 2: simple terminal visualizations (bar/line/pie)
def m2():
    print("\n\033[1;36mMODE 2: DATA VISUALIZATION\033[0m")
    print("[1] Bar\n[2] Line\n[3] Pie")
    ch = input("> ").strip()
    try:
        if ch == '1':  # ---- BAR ----
            raw = input("Enter Label:Value pairs (comma separated):\n> ")
            parts = [p.split(':') for p in raw.split(',')]
            lbl, val = zip(*[(a.strip(), float(b.strip())) for a,b in parts])
            clr(); mx = max(val) or 1; scale = 60/mx
            for i,v in enumerate(val):
                print("\n"+f"{lbl[i][:12]:12} | {'█'*int(v*scale)} {v:.2f}")

        elif ch == '2':  # ---- LINE ----
            raw = input("Enter Y values (comma separated):\n> ")
            ys = [float(x.strip()) for x in raw.split(',')]
            if len(ys)<2: raise ValueError
            clr(); h,w = 20,60; mn,mx = min(ys),max(ys); rng = (mx-mn) or 1
            pts=[(int(i*(w-1)/(len(ys)-1)), h-1-int((y-mn)/rng*(h-1))) for i,y in enumerate(ys)]
            g=[[" " for _ in range(w)] for _ in range(h)]
            for x,y in pts: g[y][x]='●'
            for i in range(len(pts)-1):
                x1,y1=pts[i]; x2,y2=pts[i+1]; dx=max(1,abs(x2-x1))
                for t in range(1,dx):
                    x=x1+int((x2-x1)*t/dx); y=y1+int((y2-y1)*t/dx)
                    if 0<=x<w and 0<=y<h: g[y][x]='·'
            for r in g: print(''.join(r))

        elif ch == '3':  # ---- PIE ----
            raw = input("Enter Name:Value pairs (comma separated):\n> ")
            parts = [p.split(':') for p in raw.split(',')]
            lbl, val = zip(*[(a.strip(), float(b.strip())) for a,b in parts])
            clr(); tot=sum(val) or 1
            for i,v in enumerate(val):
                pct=v/tot*100
                print(f"{lbl[i][:12]:12}: {pct:5.1f}% {'█'*int(pct/2)}")
        else:
            print("Invalid choice")
    except:
        print("Invalid input")
    input("\n[Enter to continue]")

# MODE 3: Runner game loop with speed scaling per 100 points
def m3():
    print("\n"+"="*60+"\nMODE 3: RAPTORS GO 🦖\n"+"="*60+"\n🎮 SPACE=Jump | Q=Quit\n")
    input("Press Enter...")
    w,h=120,28;px,py=20,h-7;vy=0;obs=[];scr=0;gm=True;cld=[];frm=0;lst_obs=0;hlth=3;spd=4;step=0
    mnt_pos=[(i,random.randint(5,8)) for i in range(10,w,25)]
    for _ in range(5):cld.append([random.randint(0,w),random.randint(2,5)])
    sys.stdout.write("\033[?25l");st_time=time.time()
    while gm and hlth>0:
        frm+=1
        cur_step=scr//100
        if cur_step>step:
            spd=min(spd+0.4,12)
            step=cur_step
        # Input handling (non-blocking): space to jump, Q to quit
        if os.name!='nt':
            import termios,tty,select;fd=sys.stdin.fileno();old=termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                if select.select([sys.stdin],[],[],0)[0]:
                    ch=sys.stdin.read(1)
                    if ch==' ' and py>=h-7:vy=-4.0
                    elif ch in ['q','Q']:gm=False;break
            finally:termios.tcsetattr(fd,termios.TCSADRAIN,old)
        else:
            import msvcrt
            if msvcrt.kbhit():
                ch=msvcrt.getch()
                if ch==b' ' and py>=h-7:vy=-4.0
                elif ch in [b'q',b'Q']:gm=False;break
        vy+=0.45;py+=vy
        if py>=h-7:py=h-7;vy=0
        # Spawn obstacles at interval; pick ground or bird
        if frm-lst_obs>max(30,80-int(spd*5)):
            typ=random.choice(['cactus','cactus','cactus','bird'])
            obs.append([w-1,random.choice([h-13,h-15]) if typ=='bird' else h-7,typ]);lst_obs=frm
        # Move and recycle; check collisions
        nob=[]
        for ox,oy,typ in obs:
            ox-=spd
            if ox>-12:nob.append([ox,oy,typ])
            else:scr+=10;continue
            if (typ=='bird' and abs(px-ox)<7 and abs(py-oy)<3) or (typ!='bird' and abs(px-ox)<5 and py>=oy-5):
                hlth-=1;continue
        obs=nob
        # Clouds parallax
        for i in range(len(cld)):
            cld[i][0]-=0.3
            if cld[i][0]<-15:cld[i]=[w+10,random.randint(2,5)]
        # Render scene grid
        grd=[[" " for _ in range(w)] for _ in range(h)]
        for cx,cy in cld:
            ix=int(cx)
            if 0<=ix<w-10 and 0<=cy<h-5:
                ca=["\033[38;2;200;200;200m  ░▒▓▓▒░  \033[0m","\033[38;2;220;220;220m░▒▓████▓▒░\033[0m","\033[38;2;240;240;240m▒▓▓▓▓▓▓▓▓▒\033[0m"]
                for dy,ln in enumerate(ca):
                    if cy+dy<h:
                        for dx in range(10):
                            if 0<=ix+dx<w:grd[cy+dy][ix+dx]=ln[dx*9:dx*9+9] if dx<len(ln)//9 else " "
        for mx,peak_h in mnt_pos:
            bx=int((mx-frm*0.2)%w)
            for dy in range(peak_h):
                for dx in range(-dy,dy+1):
                    yy=h-8-dy;xx=bx+dx
                    if 0<=yy<h and 0<=xx<w:
                        if dy==0:grd[yy][xx]="\033[38;2;139;69;19m▲\033[0m"
                        elif abs(dx)==dy:grd[yy][xx]="\033[38;2;101;67;33m╱\033[0m" if dx<0 else "\033[38;2;101;67;33m╲\033[0m"
                        elif dy<peak_h//2:grd[yy][xx]="\033[38;2;160;82;45m░\033[0m"
                        else:grd[yy][xx]="\033[38;2;139;69;19m▒\033[0m"
        for i in range(w):grd[h-6][i]="\033[38;2;128;128;128m═\033[0m"
        for i in range(0,w,3):grd[h-5][i]="\033[38;2;100;100;100m░\033[0m" if i%6==0 else "\033[38;2;80;80;80m·\033[0m"
        # Player (dino) sprite
        dino=["\033[38;2;34;139;34m      ▄▄▄█████▄▄▄  \033[0m","\033[38;2;34;139;34m    ▄███████████▀  \033[0m","\033[38;2;34;139;34m    ████████████   \033[0m","\033[38;2;34;139;34m    ▀██████████▀   \033[0m","\033[38;2;34;139;34m      ██    ██     \033[0m","\033[38;2;34;139;34m      ▀▀    ▀▀     \033[0m"]
        dino_y=int(py)
        for dy,ln in enumerate(dino):
            if 0<=dino_y+dy<h and 0<=px<w:grd[dino_y+dy][px]=ln
        # Obstacles
        for ox,oy,typ in obs:
            ix=int(ox)
            if typ=='cactus':
                cact=["\033[38;2;0;128;0m   ││││   \033[0m","\033[38;2;0;128;0m ┌─┼┼┼┼─┐ \033[0m","\033[38;2;0;100;0m │▓▓▓▓▓▓│ \033[0m","\033[38;2;0;100;0m┌┼▓▓▓▓▓▓┼┐\033[0m","\033[38;2;0;100;0m││▓▓▓▓▓▓││\033[0m","\033[38;2;0;100;0m││▓▓▓▓▓▓││\033[0m","\033[38;2;0;100;0m││▓▓▓▓▓▓││\033[0m","\033[38;2;0;100;0m└┴▓▓▓▓▓▓┴┘\033[0m"]
                for dy,ln in enumerate(cact):
                    if 0<=oy+dy<h and 0<=ix<w:grd[oy+dy][ix]=ln
            elif typ=='bird':
                bird=["\033[38;2;139;0;0m  ╭───╮  \033[0m","\033[38;2;139;0;0m ╱◉ ◉╲ \033[0m","\033[38;2;139;0;0m╱  ▼  ╲\033[0m","\033[38;2;100;0;0m▔▔▔▔▔▔▔\033[0m"]
                for dy,ln in enumerate(bird):
                    if 0<=oy+dy<h and 0<=ix<w:grd[oy+dy][ix]=ln
        sys.stdout.write("\033[H")
        hrt="\033[1;31m♥\033[0m"*hlth+"\033[2;37m♡\033[0m"*(3-hlth);spd_pct=int((spd/4)*100)
        print(f"\033[1;33mSCORE:{scr:05d}\033[0m  \033[1;34m{int(time.time()-st_time)}s\033[0m  {hrt} \033[1;31mHP:{hlth}/3\033[0m  \033[1;35m{spd_pct}%\033[0m  \033[1;36mSPACE↑ Q\033[0m\n")
        for row in grd:print("  "+"".join(str(x) for x in row))
        sys.stdout.flush();time.sleep(0.028)
    sys.stdout.write("\033[?25h");
    print(f"\n\033[1;33mGame Over! Score:{scr} Time:{int(time.time()-st_time)}s\033[0m")
    input("[Enter]")
    
# MODE 4: Video → ASCII with optional preprocessing and binary writes
def m4():
    if not cv2:print("OpenCV not installed!"); input("Enter..."); return
    print("\n"+"="*70+"\n\033[1;36mMODE 4: ASCII MOVIE PLAYER 🎬\033[0m\n"+"="*70)
    pth=input("Video path: ").strip().strip('"')
    if not os.path.exists(pth): print("File not found"); input("Enter..."); return
    print("Res: [1] fast =120 \n[2] medium =200 \n[3] good =300 \n[4] better =400 \n[5] excellent =500 \n[6] ultra =600")
    res_ch=input("> ").strip(); res_map={1:120,2:200,3:300,4:400,5:500,6:600}
    wid=res_map.get(int(res_ch) if res_ch.isdigit() else 3,300)
    print("\n\033[1;35m🎨 Mode:\033[0m  [1] RGB  [2] BW")
    rgb=input("> Choice: ").strip()!='2'
    if wid>=400 and rgb:
        print("\n\033[1;33m⚠️  RGB at high resolution is slow. BW recommended for 60 FPS.\033[0m")
        if input("Continue with RGB? (y/N): ").strip().lower()!='y':
            rgb=False; print("\033[1;32m✅ Using BW for better performance\033[0m")
    print(f"\n\033[1;36m{'🚀 GPU ACTIVE' if gpu_on else '⏳ CPU PROCESSING'}\033[0m\nLoading video...\n")
    aud_pth=None
    try:
        import pygame,subprocess,sys as _sys
        try: _sys.stdout.reconfigure(line_buffering=False)
        except: pass
        if os.name=='nt':
            try: os.system('mode con: cols=160 lines=50'); os.system('')
            except: pass
        pygame.mixer.init(); aud_pth=f"temp_audio_{int(time.time())}.wav"
        try:
            subprocess.run(['ffmpeg','-i',pth,'-vn','-acodec','pcm_s16le','-ar','44100','-ac','2',aud_pth,'-y'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=30)
            if os.path.exists(aud_pth):
                pygame.mixer.music.load(aud_pth); print("\033[1;32m✅ Audio extracted\033[0m")
            else: aud_pth=None; print("\033[1;33m⚠️  No audio\033[0m")
        except: aud_pth=None; print("\033[1;33m⚠️  No FFmpeg\033[0m")
    except: aud_pth=None; print("\033[1;33m⚠️  No audio\033[0m")
    try:
        cap=cv2.VideoCapture(pth); fps=cap.get(cv2.CAP_PROP_FPS) or 30.0
        tfc=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); dly=1.0/fps
        chr=" .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        test_times=[]
        for _ in range(5):
            ret,frm=cap.read();
            if not ret: break
            ts=time.time(); h,w,_=frm.shape; hgt=int((h/w)*wid*0.55); frm=cv2.resize(frm,(wid,hgt))
            if gpu_on:
                pix=cp.array(frm)
                if rgb:
                    b,g,r=pix[:,:,0],pix[:,:,1],pix[:,:,2]; gry=(0.299*r+0.587*g+0.114*b).astype(cp.uint8); pix=cp.asnumpy(pix)
                else:
                    gry=cp.mean(pix,axis=2).astype(cp.uint8); pix=None
                gry=cp.asnumpy(gry)
            else:
                if rgb: pix=frm; gry=cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY)
                else: gry=cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY); pix=None
            # build string efficiently
            if rgb:
                lines=[]
                for y in range(hgt):
                    line_chars=[]
                    for x in range(wid):
                        v=gry[y,x]; idx=int((v/255)*(len(chr)-1)); b,g,r=int(pix[y,x,0]),int(pix[y,x,1]),int(pix[y,x,2])
                        line_chars.append(f"\033[38;2;{r};{g};{b}m{chr[idx]}")
                    line_chars.append("\033[0m"); lines.append(''.join(line_chars))
                asc='\n'.join(lines)
            else:
                lines=[]
                for y in range(hgt):
                    row_chars=[chr[int((gry[y,x]/255)*(len(chr)-1))] for x in range(wid)]
                    lines.append(''.join(row_chars))
                asc='\n'.join(lines)
            test_times.append(time.time()-ts)
        avg_proc=sum(test_times)/len(test_times) if test_times else 0.033
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        print(f"\033[1;32m✅ Avg frame time: {avg_proc*1000:.1f}ms ({1/max(avg_proc,1e-6):.1f} FPS capable)\033[0m")
        pre_proc=False
        if avg_proc>dly:
            print(f"\033[1;33m⚠️  Processing {avg_proc*1000:.0f}ms slower than target {dly*1000:.0f}ms ({fps:.1f} FPS)\033[0m")
            print("\033[1;35mOptions:\033[0m\n  [1] 🚀 Pre-process (smooth)\n  [2] ⚡ Real-time")
            if input("> ").strip()=="1":
                pre_proc=True
                print(f"\n\033[1;36m⏳ Pre-processing {tfc} frames...\033[0m")
                # Preprocess: cache pre-encoded frames to bytes for fast playback
                cache_bin=[]; cap.set(cv2.CAP_PROP_POS_FRAMES,0); proc_st=time.time()
                for i in range(tfc):
                    ret,frm=cap.read();
                    if not ret: break
                    h,w,_=frm.shape; hgt=int((h/w)*wid*0.55); frm=cv2.resize(frm,(wid,hgt))
                    if gpu_on:
                        pix=cp.array(frm)
                        if rgb:
                            b,g,r=pix[:,:,0],pix[:,:,1],pix[:,:,2]; gry=(0.299*r+0.587*g+0.114*b).astype(cp.uint8); pix=cp.asnumpy(pix)
                        else:
                            gry=cp.mean(pix,axis=2).astype(cp.uint8); pix=None
                        gry=cp.asnumpy(gry)
                    else:
                        if rgb: pix=frm; gry=cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY)
                        else: gry=cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY); pix=None
                    if rgb:
                        lines=[]
                        for y in range(hgt):
                            line_chars=[]
                            for x in range(wid):
                                v=gry[y,x]; idx=int((v/255)*(len(chr)-1)); b,g,r=int(pix[y,x,0]),int(pix[y,x,1]),int(pix[y,x,2])
                                line_chars.append(f"\033[38;2;{r};{g};{b}m{chr[idx]}")
                            line_chars.append("\033[0m"); lines.append(''.join(line_chars))
                        asc='\n'.join(lines)+'\n'
                    else:
                        lines=[]
                        for y in range(hgt):
                            row_chars=[chr[int((gry[y,x]/255)*(len(chr)-1))] for x in range(wid)]
                            lines.append(''.join(row_chars))
                        asc='\n'.join(lines)+'\n'
                    cache_bin.append(asc.encode('utf-8'))
                    if (i+1)%100==0 or i==tfc-1:
                        pct=((i+1)/tfc)*100; elp=time.time()-proc_st; eta=(elp/(i+1))*(tfc-(i+1))
                        sys.stdout.write(f"\r\033[1;36m⏳ {i+1}/{tfc} ({pct:.1f}%) ETA:{int(eta)}s\033[0m"); sys.stdout.flush()
                print(f"\n\033[1;32m✅ Done in {time.time()-proc_st:.1f}s. Smooth at {fps:.1f} FPS\033[0m")
        else:
            print(f"\033[1;32m✅ Real-time OK at {fps:.1f} FPS\033[0m")
        input("\nPress Enter (SPACE=Pause Q=Quit)...")
        frm_num=0; pau=False; pau_time=0
        if aud_pth and os.path.exists(aud_pth): pygame.mixer.music.play()
        sys.stdout.write("\033[?25l")
        if pre_proc:
            stdout_buf=sys.stdout.buffer; home=b"\033[H"
            playback_start=time.time(); frames_played=0
            while frm_num< len(cache_bin):
                if os.name!='nt':
                    import termios,tty,select
                    fd=sys.stdin.fileno(); old=termios.tcgetattr(fd)
                    try:
                        tty.setcbreak(fd)
                        if select.select([sys.stdin],[],[],0)[0]:
                            ch=sys.stdin.read(1)
                            if ch==' ':
                                pau=not pau
                                if pau:
                                    if aud_pth: pygame.mixer.music.pause(); pau_time=time.time()
                                else:
                                    if aud_pth: pygame.mixer.music.unpause(); playback_start+=time.time()-pau_time
                            elif ch in ['q','Q']: break
                    finally: termios.tcsetattr(fd,termios.TCSADRAIN,old)
                else:
                    import msvcrt
                    if msvcrt.kbhit():
                        ch=msvcrt.getch()
                        if ch==b' ':
                            pau=not pau
                            if pau:
                                if aud_pth: pygame.mixer.music.pause(); pau_time=time.time()
                            else:
                                if aud_pth: pygame.mixer.music.unpause(); playback_start+=time.time()-pau_time
                        elif ch in [b'q',b'Q']: break
                if pau:
                    sys.stdout.write("\033[H\n\033[1;33m⏸️  PAUSED\033[0m"); sys.stdout.flush(); time.sleep(0.05); continue
                stdout_buf.write(home); stdout_buf.write(cache_bin[frm_num]); stdout_buf.flush()
                frm_num+=1; frames_played+=1
                # Playback timing: target = playback_start + frames_played*dly (handles pause drift)
                target=playback_start + frames_played*dly; slp=target-time.time()
                if slp>0: time.sleep(slp)
        else:
            while True:
                if os.name!='nt':
                    import termios,tty,select
                    fd=sys.stdin.fileno(); old=termios.tcgetattr(fd)
                    try:
                        tty.setcbreak(fd)
                        if select.select([sys.stdin],[],[],0)[0]:
                            ch=sys.stdin.read(1)
                            if ch==' ':
                                pau=not pau
                                if pau:
                                    if aud_pth: pygame.mixer.music.pause(); pau_time=time.time()
                                else:
                                    if aud_pth: pygame.mixer.music.unpause()
                            elif ch in ['q','Q']: break
                    finally: termios.tcsetattr(fd,termios.TCSADRAIN,old)
                else:
                    import msvcrt
                    if msvcrt.kbhit():
                        ch=msvcrt.getch()
                        if ch==b' ':
                            pau=not pau
                            if pau:
                                if aud_pth: pygame.mixer.music.pause(); pau_time=time.time()
                            else:
                                if aud_pth: pygame.mixer.music.unpause()
                        elif ch in [b'q',b'Q']: break
                if pau: sys.stdout.write("\033[H\n\033[1;33m⏸️  PAUSED\033[0m"); sys.stdout.flush(); time.sleep(0.05); continue
                loop_st=time.time(); ret,frm=cap.read(); 
                if not ret: break
                h,w,_=frm.shape; hgt=int((h/w)*wid*0.55); frm=cv2.resize(frm,(wid,hgt))
                if gpu_on:
                    pix=cp.array(frm)
                    if rgb:
                        b,g,r=pix[:,:,0],pix[:,:,1],pix[:,:,2]; gry=(0.299*r+0.587*g+0.114*b).astype(cp.uint8); pix=cp.asnumpy(pix)
                    else:
                        gry=cp.mean(pix,axis=2).astype(cp.uint8); pix=None
                    gry=cp.asnumpy(gry)
                else:
                    if rgb: pix=frm; gry=cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY)
                    else: gry=cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY); pix=None
                if rgb:
                    lines=[]
                    for y in range(hgt):
                        line_chars=[]
                        for x in range(wid):
                            v=gry[y,x]; idx=int((v/255)*(len(chr)-1)); b,g,r=int(pix[y,x,0]),int(pix[y,x,1]),int(pix[y,x,2])
                            line_chars.append(f"\033[38;2;{r};{g};{b}m{chr[idx]}")
                        line_chars.append("\033[0m"); lines.append(''.join(line_chars))
                    asc='\n'.join(lines)+'\n'
                else:
                    lines=[]
                    for y in range(hgt):
                        row_chars=[chr[int((gry[y,x]/255)*(len(chr)-1))] for x in range(wid)]
                        lines.append(''.join(row_chars))
                    asc='\n'.join(lines)+'\n'
                sys.stdout.write("\033[H"); sys.stdout.buffer.write(asc.encode('utf-8')); sys.stdout.flush()
                slp=dly-(time.time()-loop_st);
                if slp>0.001: time.sleep(slp)
        sys.stdout.write("\033[?25h"); cap.release()
        if aud_pth:
            try: pygame.mixer.music.stop(); os.remove(aud_pth)
            except: pass
        print("\n\033[1;32m✅ Complete!\033[0m")
    except Exception as e:
        sys.stdout.write("\033[?25h");
        if aud_pth:
            try: pygame.mixer.music.stop(); os.remove(aud_pth)
            except: pass
        print(f"\033[1;31m⚠️  Error: {e}\033[0m")
    input("\n[Enter]")
def main():
    while True:
        print("\033[1;36m╔═══════════════════════════════════════════════════════════════════╗\033[0m")
        print("\033[1;36m║              VisT - Visual Terminal Tool                          ║\033[0m")
        print("\033[1;36m║                  Code Olympics 2025                               ║\033[0m")
        print("\033[1;36m╚═══════════════════════════════════════════════════════════════════╝\033[0m\n")
        print(f"GPU:{'ON' if gpu_on else 'OFF'}")
        print("[1] Image->ASCII🖼️ \n[2] Data Viz📊 \n[3] Raptors Go🦖 \n[4] Movie📺 \n[0] Exit❌")
        ch=input("> ").strip()
        if ch=='1': clr(); m1()
        elif ch=='2': clr(); m2()
        elif ch=='3': clr(); m3()
        elif ch=='4': clr(); m4()
        elif ch=='0': clr(); print("Bye!"); break
        else:
            print("Invalid choice"); time.sleep(1)
if __name__=="__main__":
    clr()
    print("ViST - Visual Studio 500 starting...")
    main()

