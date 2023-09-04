from __future__ import print_function
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import os.path
import qrcode
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont

# Your parsed JSON folder structure
folder_structure = {
  "SHCC": {
    "GER": {
      "TGBT-GER 4.1": {
        "SSL": ["TENS-LT-ARR"],
        "RDC": ["TDN-S1-RDC", "TDN-S3-RDC"],
        "R+1": ["TDN-S1-1E"],
        "R+2": ["TDN-S1-2E"],
        "R+3": ["TENS-LT ECS"]
      },
      "TGBT-GER 4.2": {
        "RDC": ["TDN-CUIS", "TDN-S2-RDC", "TDN-S4-RDC"],
        "R+1": ["TDN-S2-1E"],
        "R+2": ["TDN-S2-2E"],
        "R+3": ["TEN-CTA", "TEN-VENT"]
      },
      "TGHQ-GER 4.1": {
        "RDC": ["TDHQ-S1-RDC", "TDHQ-S3-RDC"],
        "R+1": ["TDHQ-S1-1E"],
        "R+2": ["TDHQ-S1-2E"]
      },
      "TGHQ-GER 4.2": {
        "RDC": ["TDHQ-S2-RDC", "TDHQ-S4-RDC"],
        "R+1": ["TDHQ-S2-1E"],
        "R+2": ["TDHQ-S2-2E"]
      },
      "TGS-GER 4": {
        "R+1": ["TEN-DES-1E"],
        "R+3": ["TEN-ASC", "TEN-DES"]
      },
      "TGB-GER": {
        "EXT": ["TEN-EC EX5", "TEN-EC EX6", "TENS-LY-FM"]
      }
    },
    "HG": {
      "HG NORD": {
        "TGBT HG 2.1": {
          "SSL": ["TSN-CUIS-01", "TSN-CUIS-02", "TSN-CUIS-03", "TSN-CUIS-04", "TDN-CUIS-01", "TDN-CUIS-02"],
          "RDC": ["TDN-COM-MED", "TDN-COM-NORD", "TDN-CON-CHI"],
          "R+1": ["TDN-COM-NORD", "TDN-HOS CHI"],
          "R+2": ["TDN-HDJ-CAR", "TDN-HOS MED"],
          "R+3": ["TDN-COM-NORD", "TEN-CVC-04 N"],
          "TOITURE": ["TDN-VENT-NORD", "TDN-CTA-NORD"]
        },
        "TGBT HG 2.2": {
          "SSL": ["TEN-CVC 01NA", "TDN-COM-NORD", "TEN-CVC 02NA", "TEN-CVC-02NB", "TDN-SP1", "TEN-ATR-AIR", "TDN-STE", "TEN-LT-EAU-STE"],
          "RDC": ["TDN-URG-01", "TDN-UMG-02", "TDN-UMG-01"],
          "R+1": ["TDN-BDP-02", "TDN-REA-02"],
          "R+2": ["TDN-COM-NORD", "TDN-HEMO", "TDN-HDJ-ENC"],
          "R+3": ["TDN-LAB-01"]
        },
        "TGHQ HG 2.1": {
          "RDC": ["TDHQ-COM-MED", "TDHQ-COM-CHI", "TDHQ-COM-NORD"],
          "R+1": ["TDHQ-HOS-CHI", "TDHQ-COM-NORD"],
          "R+2": ["TDHQ-HOS-MED", "TDHQ-HDJ-CAR"],
          "R+3": ["TDHQ-COM-NORD"]
        },
        "TGHQ HG 2.2": {
          "SSL": ["TDHQ-COM-NORD", "TDHQ-STE"],
          "RDC": ["TDHQ-URG-01", "TDHQ-IMG-02", "TDHQ-IMG-01"],
          "R+1": ["TDHQ-REA-02"],
          "R+2": ["TDHQ-COM-NORD", "TDHQ-HEMO", "TDHQ-HDJ-ENC", "TEHQ-SOP-01", "TEHQ-SOP-02", "TEHQ-SOP-03", "TEHQ-SOP-04"],
          "R+3": ["TDHQ-LAB-01"]
        }
      },
      "HG SUD": {
        "TGBT HG 1.1": {
          "SSL": ["TDN-COM-SUD", "TEN-LT-SST-EG", "TEN-LT-SST-ECS", "TEN-LT-SST-EC", "TDN-PHAR"],
          "RDC": ["TDN-END", "TDN-COM-SUD", "TDN-CON-ME"],
          "R+1": ["TDN-HOS-OPHT", "TDN-HOS-GEN"],
          "R+2": ["TDN-COM-SUD", "TDN-HOS-PED"],
          "R+3": ["TGN-PHOTOV", "TEN-CVC-04 S", "TEN-LT-SST-ECSOL"],
          "TOITURE": ["TDN-VENT-SUD", "TDN-CTA-SUD"]
        },
        "TGBT HG 1.2": {
          "SSL": ["TDN-BND", "TDN-PRK", "TEN-CVC 02SB", "TDN-ATE", "TEN-CVC 02SA"],
          "RDC": ["TDN-UTA-01", "TDN-UTA-02", "TDN-URG-02"],
          "R+1": ["TDN-COM-SUD", "TDN-HDJ-CHI"],
          "R+2": ["TDN-HOS-NEU", "TDN-HOS-ENC"],
          "R+3": ["TDN-LAB-02", "TDN-COM-SUD", "TDN-CVC-05"]
        },
        "TGHQ HG 1.1": {
          "SSL": ["TDHQ-COM-SUD", "TDHQ-PHAR"],
          "RDC": ["TDHQ-END", "TDHQ-COM-SUD", "TDHQ-CON-ME"],
          "R+1": ["TDHQ-HOS-GYNE", "TDHQ-HOS-OPHT"],
          "R+2": ["TDHQ-HOS-PED", "TDHQ-COM-SUD"]
        },
        "TGHQ HG 1.2": {
          "SSL": ["TDHQ-ATE"],
          "RDC": ["TDHQ-UTA-01", "TDHQ-URG-02", "TDHQ-URG-01"],
          "R+1": ["TDHQ-COM-SUD", "TDHQ-HDJ-CHI"],
          "R+2": ["TDHQ-HOS-NEU", "TDHQ-HOS-ENC", "TEHQ-SOP-05", "TEHQ-SOP-06", "TEHQ-SOP-07", "TEHQ-SOP-08"],
          "R+3": ["TDHQ-LAB-02", "TDHQ-COM-SUD"]
        }
      }
    },
    "SSR": {
      "TGBT SSR 3.1": {
        "SSL": ["TDN-COM-NORD", "TEN-CVC 01B", "TDN-COM-CENTRE"],
        "RDC": ["TDN-COM-NORD", "TDN-BALNEO", "TDN-CON 1"],
        "R+1": ["TDN-COM-CENTRE", "TDN-HOS H2", "TDN-HOS ENF E", "TDN-ADM"],
        "R+2": ["TDN-COM-CENTRE", "TDN-HOS C"],
        "R+3": ["TDN-COM-NORD", "TDN-COM-CENTRE"],
        "TOITURE": ["TEN-VENT", "TE-CTA"]
      },
      "TGBT SSR 3.2": {
        "SSL": ["TEN-CTA 02B", "TEN-LTEP", "TEN-LTSURP", "TDN-COM-SUD", "TEN-LTECEG", "TEN-LTECS", "TEN-CTA02A"],
        "RDC": ["TDN-COM-SUD", "TDN-COM-CENTRE", "TDN-CON2"],
        "R+1": ["TDN-SP2", "TDN-SP1"],
        "R+2": ["TDN-HOS B1", "TDN-HOS B2", "TDN-HOS A"],
        "R+3": ["TDN-HOS D1", "TDN-HOS D2", "TEN-CVC03"]
      },
      "TGHQ SSR 3.1": {
        "SSL": ["TDHQ-COM-NORD", "TDHQ-COM-CENTRE"],
        "RDC": ["TDHQ-BALNEO", "TDHQ-COM-NORD", "TDHQ-CON 1"],
        "R+1": ["TDHQ-HOS ENF E", "TDHQ-HOS H2", "TDHQ-COM-CENTRE", "TDHQ-ADM"],
        "R+2": ["TDHQ-HOS C", "TDHQ-COM-CENTRE"],
        "R+3": ["TDHQ-COM-CENTRE", "TDHQ-COM-NORD"]
      },
      "TGHQ SSR 3.2": {
        "SSL": ["TDHQ-COM-SUD"],
        "RDC": ["TDHQ-COM-SUD", "TDHQ-COM-CENTRE", "TDHQ-CON 2"],
        "R+1": ["TDHQ-SP1", "TDHQ-SP2"],
        "R+2": ["TDHQ-HOS B1", "TDHQ-HOS B2", "TDHQ-HOS A"],
        "R+3": ["TDHQ-HOS D1", "TDHQ-HOS D2"]
      }
    }
  }
}



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def create_folder(service, parent_id, folder_name):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id'), folder

def get_folder_path(service, folder_id):
    folder_metadata = service.files().get(fileId=folder_id, fields='id, name, parents').execute()
    folder_path = [folder_metadata]

    while 'parents' in folder_metadata:
        parent_id = folder_metadata['parents'][0]
        if parent_id == 'root':
            break
        parent_metadata = service.files().get(fileId=parent_id, fields='id, name, parents').execute()
        folder_path.insert(0, parent_metadata)
        folder_metadata = parent_metadata

    return folder_path


def create_folders_recursive(service, parent_id, folder_structure):
    if isinstance(folder_structure, list):  # Check if it's a list of folders
        for folder_name in folder_structure:
            folder_id, folder_metadata = create_folder(service, parent_id, folder_name)
            generate_and_upload_qr_code(service, folder_id, folder_metadata)
    elif isinstance(folder_structure, dict):  # Check if it's a dictionary of subfolders
        for folder_name, subfolders in folder_structure.items():
            folder_id, folder_metadata = create_folder(service, parent_id, folder_name)
            generate_and_upload_qr_code(service, folder_id, folder_metadata)
            create_folders_recursive(service, folder_id, subfolders)

def generate_and_upload_qr_code(service, folder_id, folder_metadata):
    folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
    
    # Create a QR code with the folder URL
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(folder_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Customize the QR code image with the folder path
    draw = ImageDraw.Draw(qr_img)
    font = ImageFont.load_default()  # You can customize the font if needed
    folder_path = '/'.join(folder_metadata['name'] for folder_metadata in get_folder_path(service, folder_id))
    draw.text((10, qr_img.size[1] - 20), folder_path, fill="black", font=font)
    
    # Convert the QR code image to a bytes stream
    qr_img_stream = BytesIO()
    qr_img.save(qr_img_stream, format="PNG")
    qr_img_stream.seek(0)

    # Upload the QR code image to the folder
    qr_code_metadata = {
        'name': 'qr_code.png',
        'parents': [folder_id]
    }

    service.files().create(
        body=qr_code_metadata,
        media_body=MediaIoBaseUpload(qr_img_stream, mimetype='image/png'),
        fields='id'
    ).execute()



def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Create the folders recursively
        root_folder_id = "root"  # Replace with the parent folder ID
        create_folders_recursive(service, root_folder_id, folder_structure)

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()