import json,sys,base64,re
out=sys.argv[1]; parts=[]
for f in sys.argv[2:]:
    t=json.load(open(f))[0]['text']
    m=re.search(r'@@(.*?)@@',t,re.S); parts.append(m.group(1))
open(out,'wb').write(base64.b64decode(''.join(parts)))
