import re, glob, os
files = sorted(glob.glob("sections/*.md"))
terms = ["workspace overlay","packed lower","upper","overlay","lease + generation fencing","tombstone","copy-up","pcluster","463.471","492.831","387.973","235.930","261,490","JuiceFS","149.7","37.3","41.6","73.6","65.8"]
print("file".ljust(22), " ".join(t[:8].rjust(9) for t in terms))
for f in files:
    t = open(f, encoding="utf-8").read()
    print(os.path.basename(f).ljust(22), " ".join(str(t.count(x)).rjust(9) for x in terms))
t = open("proposal_final.md", encoding="utf-8").read()
print("\nTOTAL overlay:", t.count("overlay"), "| JuiceFS:", t.count("JuiceFS"), "| 463.471:", t.count("463.471"))
