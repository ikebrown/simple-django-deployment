from django.core.files import File
from filer.models.filemodels import File as FilerFile
import os

videodir = '/home/innomed_upload'
videos = os.listdir(videodir)
flvfiles = [f for f in videos if f.endswith('.flv')]

for f in flvfiles:
    print "Laster %s" % f
    infile = os.path.join(videodir, f)
    dfile = File(open(infile, 'r'), f)
    ffile  = FilerFile(original_filename=f, owner_id=2)
    ffile.file = dfile
    ffile.save()
    print "Lastet %s" % f
    print "-----------"
    
"""
FilerFile.objects.filter(original_filename__endswith='.pdf', folder=None).update(folder=20)
"""

40040507