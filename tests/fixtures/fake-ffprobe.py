#!/usr/bin/env python3
import json

print(json.dumps({
    "streams": [{
        "codec_type": "video",
        "codec_name": "h264",
        "width": 1920,
        "height": 1080,
        "duration": "8.000000",
        "avg_frame_rate": "30/1",
    }],
    "format": {"format_name": "mov,mp4,m4a,3gp,3g2,mj2", "duration": "8.000000"},
}))
