function font_awesome_file_icon(mime_type) {
    data = {
        'image/jpeg' :'fa fa-file-image-o',
        'image/bmp' :'fa fa-file-image-o',
        'image/png' :'fa fa-file-image-o',
        'image/webp' :'fa fa-file-image-o',
        'image/x-icon' :'fa fa-file-image-o',
        'image/vnd.microsoft.icon' :'fa fa-file-image-o',
        'audio/midi' : 'fa fa-file-audio-o',
        'audio/mpeg' : 'fa fa-file-audio-o',
        'audio/webm' : 'fa fa-file-audio-o',
        'audio/ogg' : 'fa fa-file-audio-o',
        'audio/wav' : 'fa fa-file-audio-o',
        'video' : 'fa fa-file-video-o',
        'application/pdf' : 'fa fa-file-pdf-o',
        'application/msword': 'fa fa-file-word-o',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'fa fa-file-word-o',
        'application/vnd.ms-excel' : 'fa fa-file-excel-o',
        'application/vnd.oasis.opendocument.spreadsheet' : 'fa fa-file-excel-o',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' : 'fa fa-file-excel-o',
        'text/plain' : 'fa fa-file-text-o',
        'text/html' : 'fa fa-file-code-o',
        'application/json' : 'fa fa-file-code-o',
        'application/gzip' : 'fa fa-file-archive-o',
        'application/zip' : 'fa fa-file-archive-o',
        'application/octet-stream' : 'fa fa-file-o',
        'application/vnd.ms-powerpoint' : 'fa fa-file-powerpoint-o',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation' : 'fa fa-file-powerpoint-o',
        'application/vnd.ms-powerpoint.addin.macroEnabled.12' : 'fa fa-file-powerpoint-o',
    };
    if (mime_type) {
        var mimetype = mime_type.split("'");
    }

    if (data[mimetype]) {
        return data[mimetype];
    }
    return "fa fa-file-pdf-o";
}