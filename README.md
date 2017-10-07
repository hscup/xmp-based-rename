## A Script to rename image file base on `FlightYawDegree` field XMP metadata

## How to use

### Install prerequisite
This script using Pillow-a image processing library in Python

1. Create and activate virtual environment

```bash
vituralenv --python=python3.6 myenv
cd myenv
source myenv/bin/activate
```

2. Install prerequisite 

```bash
pip install Pillow
```

3. Run the script

```bash
python rename.py <images_folder>
```

Make sure do step 2-3 in virtual environment created and activated in step 1