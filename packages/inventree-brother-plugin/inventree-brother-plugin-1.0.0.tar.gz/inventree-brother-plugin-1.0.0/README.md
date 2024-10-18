[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PEP](https://github.com/inventree/inventree-python/actions/workflows/pep.yaml/badge.svg)


# inventree-brother-plugin

A label printing plugin for [InvenTree](https://inventree.org), which provides support for the [Brother label printers](https://www.brother.com.au/en/products/all-labellers/labellers).

This plugin supports printing to *some* Brother label printers with network (wired or WiFi) support. Refer to the [brother_ql docs](https://github.com/pklaus/brother_ql/blob/master/brother_ql/models.py) for a list of label printers which are directly supported.

## Installation

Install this plugin manually as follows:

```
pip install inventree-brother-plugin
```

Or, add to your `plugins.txt` file to install automatically using the `invoke install` command:

```
inventree-brother-plugin
```
 
### Debian / Ubuntu requirements

The following command can be used to install all OS-requirements on Debian / Ubuntu-based distros:
```bash
apt install build-essential libpoppler-cpp-dev pkg-config poppler-utils
```

You might also need the following Python packages:
```bash
pip install pdf-info python-poppler
```

## Configuration Options
The following list gives an overview of the available settings. Also check out the `brother-ql` package for more information.

* **Printer Model**
Currently supported models are: 
QL-500, QL-550, QL-560, QL-570, QL-580N, QL-600, QL-650TD, QL-700, QL-710W, QL-720NW, QL-800, QL-810W, QL-820NWB, QL-1050, QL-1060N, QL-1100, QL-1100NWB, QL-1115NWB, PT-P750W, PT-P900W, PT-P950NW

* **Label Media**
Size and type of the label media. Supported options are (not all labels are available on all printers): 
12, 18, 29, 38, 50, 54, 62, 62red, 102, 103, 104, 17x54, 17x87, 23x23, 29x42, 29x90, 39x90, 39x48, 52x29, 54x29, 60x86, 62x29, 62x100, 102x51, 102x152, 103x164, d12, d24, d58, pt12, pt18, pt24, pt36

* **IP Address**
If connected via TCP/IP, specify the IP address here.

* **USB Device**
If connected via USB, specify the device identifier here (VENDOR_ID:PRODUCT_ID/SERIAL_NUMBER, e.g. from `lsusb`).

* **Auto Cut**
Cut label after printing.

* **Rotation**
Rotation angle, either 0, 90, 180 or 270 degrees.

* **Compression**
Set image compression (required for some printers).

* **High Quality**
Print in high quality (required for some printers).
