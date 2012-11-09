# coding: utf-8
import re
import os
import sys
from django.conf import settings
from cStringIO import StringIO
from PIL import Image
from datetime import datetime
from copy import deepcopy
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.files.uploadhandler import FileUploadHandler, \
    StopUpload, SkipFile, StopFutureHandlers

class CQUploadHandler(FileUploadHandler):
    def __init__(self, request):
        super(CQUploadHandler, self).__init__(request)
        self.request = request
        self.request.META['file_store'] = {
            'uploaded': 0,
        }

    def receive_data_chunk(self, raw_data, start):
        #session = self.request.session
        #current_size = session['file_store']['uploaded'] + self.chunk_size
        current_size = self.request.META['file_store']['uploaded'] + self.chunk_size
        #session['file_store']['uploaded'] += self.chunk_size
        #check for limits
        if settings.MAX_FILE_SIZE < current_size:
            #del session['file_store']
            #session.save()
            messages.info(self.request, _(
                "Uploaded file exceeded size limit set to %(size)smb and was dropped") % {
                    'size' :settings.MAX_FILE_SIZE/1024/1024
            })
            #raise SkipFile #("No data above %s bytes are allowed" % settings.MAX_FILE_SIZE)
            raise StopUpload(connection_reset=True) #"No data above %s bytes are allowed" % settings.MAX_FILE_SIZE)
        self.request.META['file_store']['uploaded'] = current_size
        #session['file_store']['uploaded'] = current_size
        #session.save()
        return raw_data

    def file_complete(self, file_size):
        pass

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding):
        META['file_store'] = {
            'uploaded': 0,
        }
        #self.request.session['file_store'] = {
        #    'uploaded': 0,
        #}
        #self.request.session.save()
        return None

    def upload_complete(self):
        if 'file_store' in self.request.session:
            del self.request.session['file_store']
            self.request.session.save()

def handle_uploaded_file(f, path, size=()):
    fp_path = os.path.join(settings.MEDIA_ROOT, path)
    os.path.exists(fp_path) or os.makedirs(fp_path)

    #getting rid of non kawaii signs and letters
    f_name = re.sub(re.compile(r'\(|\ |\)|!|\'|\"|\?|:|\+|}|{|\^|\%|\$|\#|@|~|`|,', re.S ),'_',f.name)
    f_name = re.sub(re.compile(r'_+'),'_',f_name)

    tmp_path = deepcopy(fp_path)
    fp_path = os.path.join(fp_path, f_name)

    try:
        os.lstat(fp_path)
        now = datetime.now()
        f_name = "%s_%s" % (now.strftime("%y%m%d_%H%M%S"), f_name)
        fp_path = os.path.join(tmp_path, f_name)
    except OSError:
        pass #everthing is fine, writing
    fp = StringIO() if size else open(fp_path, 'wb+')

    for chunk in f.chunks():
        fp.write(chunk)
    if size:
        fp.seek(0)
        source_image = Image.open(fp)
        new_image = source_image.resize(size)
        new_image.save(fp_path)

    return os.path.join(path, f_name)

