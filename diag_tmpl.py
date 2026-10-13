import os, glob
base="/usr/src/homeassistant/homeassistant/components"
print("components list contains 'template':", os.path.isdir(os.path.join(base,"template")))
tmpl=glob.glob(base+"/template/*.py")
print("template py files:", [os.path.basename(p) for p in tmpl])
hits=[]
for p in tmpl:
    t=open(p, errors="replace").read()
    if "device_tracker" in t:
        hits.append(os.path.basename(p))
print("template files mentioning device_tracker:", hits)
# поищем где вообще есть template device_tracker платформа
for p in glob.glob(base+"/device_tracker/*.py"):
    t=open(p, errors="replace").read()
    if "template" in t:
        print("device_tracker file mentioning template:", os.path.basename(p))
