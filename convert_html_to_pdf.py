from weasyprint import HTML
import sys

def convert_to_pdf():
    print("Converting report.html to report.pdf...")
    try:
        HTML('/home/yuvi/2026-IonQ/report.html').write_pdf('/home/yuvi/2026-IonQ/report.pdf')
        print("Success: /home/yuvi/2026-IonQ/report.pdf generated.")
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    convert_to_pdf()
