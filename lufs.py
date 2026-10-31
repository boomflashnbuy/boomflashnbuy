import sys,subprocess,json,re
f=sys.argv[1]
o=subprocess.run(['ffmpeg','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
print(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1])
