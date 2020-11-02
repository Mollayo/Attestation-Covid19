from PyPDF2 import PdfFileWriter, PdfFileReader
import qrcode
import datetime
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import numpy as np
import argparse
import os


# Motifs
# travail-achats-sante-famille-handicap-sport_animaux-convocation-missions-enfants

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-name", required=True, type=str)
    parser.add_argument("--last-name", required=True, type=str)
    parser.add_argument("--birth-date", required=True, type=str, help="DD/MM/YYYY")
    parser.add_argument("--birth-city", required=True, type=str)
    parser.add_argument("--address", required=True, type=str, help="Address")
    parser.add_argument("--current-city", required=True, type=str, help="Postcode City")
    parser.add_argument("--leave-date", required=False, type=str, help="DD/MM/YYYY")
    parser.add_argument("--leave-hour", required=False, type=str, help="HH:MM")
    parser.add_argument("--motifs", required=True, type=str, help="- delimited: travail-achats-sante-famille-handicap-sport_animaux-convocation-missions-enfants")
    parser.add_argument("--output", required=False, type=str, help="specify the output file")
    return parser.parse_args()


args = parse_args()

theTime = datetime.datetime.now()
if args.leave_date is None or args.leave_hour is None:
    args.leave_date=theTime.strftime('%d/%m/%Y')
    args.leave_hour=theTime.strftime('%Hh%M')
if args.output is None:
    args.output='attestation.pdf'

print("Args:", args)

# ---------------------------
#  First Page (All fields to fill)
# ---------------------------

img = Image.open("input-page1.png")
img_array = np.array(img)

img = Image.fromarray(img_array)


# Create crosses:
def get_cross():
    image = Image.new('RGB', (30, 30), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(image)
    image_font = ImageFont.truetype("Arial.ttf", 35)
    image_draw.text((3, -4), f'X', (0, 0, 0), font=image_font)
    return np.array(image)


# travail-achats-sante-famille-handicap-sport_animaux-convocation-missions-enfants
img_array = np.array(img)
cross = get_cross()
if "travail" in args.motifs:
    img_array[525:555, 157:187] = cross
if "achats" in args.motifs:
    img_array[620:650, 157:187] = cross
if "sante" in args.motifs:
    img_array[735:765, 157:187] = cross
if "famille" in args.motifs:
    img_array[820:850, 157:187] = cross
if "handicap" in args.motifs:
    img_array[907:937, 157:187] = cross
if "sport_animaux" in args.motifs:
    img_array[987:1017, 157:187] = cross
if "convocation" in args.motifs:
    img_array[1118:1148, 157:187] = cross
if "missions" in args.motifs:
    img_array[1198:1228, 157:187] = cross
if "enfants" in args.motifs:
    img_array[1292:1322, 157:187] = cross

# QR CODE
qr_text = f"Cree le: {theTime.strftime('%d/%m/%Y a %Hh%M')};\n" \
          f" Nom: {args.last_name};\n" \
          f" Prenom: {args.first_name};\n" \
          f" Naissance: {args.birth_date} a {args.birth_city};\n" \
          f" Adresse: {args.address} {args.current_city};\n" \
          f" Sortie: {args.leave_date} a {args.leave_hour};\n" \
          f" Motifs: {args.motifs}"


qr = qrcode.make(qr_text, border=0)
qr = qr.resize((200, 200))
qr = np.array(qr).astype(np.uint8) * 255
qr = qr.repeat(3).reshape(qr.shape[0], qr.shape[1], -1)
# img_array = np.array(img)
#img_array[1228:1428, 890:1090] = np.array(qr)
img_array[1330:1530, 890:1090] = np.array(qr)
img = Image.fromarray(img_array)


# Fill args
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("Arial.ttf", 22)
font_small = ImageFont.truetype("Arial.ttf", 14)
# 260, 307
draw.text((260, 285), f'{args.first_name} {args.last_name}', (0, 0, 0), font=font)
# 255, 357
draw.text((255, 331), f'{args.birth_date}', (0, 0, 0), font=font)
# 190, 407
draw.text((628, 331), f"{args.birth_city}", (0, 0, 0), font=font)
draw.text((280, 376), f"{args.address}", (0, 0, 0), font=font)

draw.text((228, 1370), f"{args.current_city}", (0, 0, 0), font=font)
draw.text((190, 1415), datetime.datetime.now().strftime("%d/%m/%Y"), (0, 0, 0), font=font)
draw.text((500, 1415), datetime.datetime.now().strftime("%Hh%M"), (0, 0, 0), font=font)


img.save("output-1.pdf", save_all=False, resolution=150)

# ---------------------------
#  Second Page (Big QR code)
# ---------------------------
img_array = np.array(Image.open('input-page2.png'))
img_array[:] = 255
qr = Image.fromarray(qr)
qr = qr.resize((qr.size[0] * 3, qr.size[1] * 3))
qr = np.array(qr)
img_array[113:113 + qr.shape[0], 113:113 + qr.shape[1]] = qr
#plt.imsave("output-2.pdf", img, format="pdf")
img = Image.fromarray(img_array)
img.save("output-2.pdf", save_all=False, resolution=150)

# --------------------
# Merge PDFs
# --------------------
pdf1 = PdfFileReader('output-1.pdf')
pdf2 = PdfFileReader('output-2.pdf')
writer = PdfFileWriter()
writer.addPage(pdf1.getPage(0))
writer.addPage(pdf2.getPage(0))
writer.write(open(args.output, "wb"))
os.remove('output-1.pdf')
os.remove('output-2.pdf')
