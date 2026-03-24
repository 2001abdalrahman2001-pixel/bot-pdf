#!/bin/bash
# تشغيل البوت كخدمة ويب عبر gunicorn
gunicorn bot:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
