"""
Generate QR codes for High Five Recognition tokens
Usage: python generate_qr_codes.py
"""

import qrcode
import os
from typing import List

# Configuration
APP_URL = "https://your-app.streamlit.app"  # Change this to your Streamlit app URL
OUTPUT_DIR = "qr_codes"
COLORS = ["red", "blue", "green", "yellow", "purple", "orange"]


def generate_qr_code(token: str, color: str, output_path: str):
    """Generate a QR code for a specific token and color"""
    url = f"{APP_URL}?token={token}&color={color}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    print(f"✓ Generated: {output_path}")


def generate_batch(prefix: str, start: int, count: int, colors: List[str]):
    """Generate a batch of QR codes"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for i in range(start, start + count):
        token = f"{prefix}{i:03d}"  # e.g., CONF001, CONF002
        color = colors[i % len(colors)]  # Cycle through colors
        
        filename = f"{token}_{color}.png"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        generate_qr_code(token, color, output_path)


def main():
    print("🎨 High Five QR Code Generator\n")
    
    print("Examples:")
    print("  1. Conference tokens: CONF001-CONF100")
    print("  2. Team tokens: TEAM-A-001, TEAM-B-001")
    print("  3. Department tokens: HR-001, IT-001")
    print()
    
    # Get user input
    prefix = input("Enter token prefix (e.g., CONF, TEAM, EVENT): ").strip()
    start_num = int(input("Start number (e.g., 1): "))
    count = int(input("How many QR codes to generate: "))
    
    print(f"\n⚠️  Make sure to update APP_URL in this script to your actual Streamlit app URL!")
    print(f"Current URL: {APP_URL}\n")
    
    proceed = input("Generate QR codes? (yes/no): ").strip().lower()
    
    if proceed == "yes":
        print(f"\n🚀 Generating {count} QR codes...\n")
        generate_batch(prefix, start_num, count, COLORS)
        print(f"\n✅ Done! QR codes saved to '{OUTPUT_DIR}/' directory")
        print(f"\n💡 Tip: You can now print these QR codes and attach them to physical tokens!")
    else:
        print("Cancelled.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
