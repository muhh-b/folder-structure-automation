# folder-structure-automation

This Python script allows you to create a complex folder structure in Google Drive and generate QR codes that link to each folder for easy access.

## Prerequisites

Before you can use this script, you need to have the following:

- Python installed on your machine (Python 3.6 or higher is recommended).
- Google API credentials (client_secret.json) for the Google Drive API.
- The necessary Python libraries installed. You can install them using pip:

    ```
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client qrcode pillow
    ```

## Usage

1. Clone or download this repository to your local machine.

2. Place your Google API credentials (`client_secret.json`) in the project directory.

3. Run the script by executing the following command in your terminal:

    ```
    python app.py
    ```

4. The script will authenticate with Google Drive, create the folder structure defined in the `folder_structure` dictionary, and generate QR codes for each folder. The QR codes will link to their respective folders.

5. You can find the generated QR code images and folders in your Google Drive.

## Configuration

- Modify the `folder_structure` dictionary in the script to define your desired folder structure. You can nest folders within folders as needed.

- Replace the `root_folder_id` in the `main` function with the ID of the parent folder where you want to create the folder structure.

- Customize the QR code appearance by modifying the code in the `generate_and_upload_qr_code` function.



## References

- [Google Drive API Documentation](https://developers.google.com/drive)
- [qrcode Library](https://pypi.org/project/qrcode/)
- [Pillow (PIL Fork) Library](https://pillow.readthedocs.io/en/stable/)

## Contributing

Contributions are welcome! Please open an issue or create a pull request with any improvements or bug fixes.


## Contact

For questions or feedback, you can reach out to mbadague@gmail.com

