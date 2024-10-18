"""
FoxLabel

An python parametters library.
"""

__version__ = "1.2"
__author__ = "Nguyễn Tuấn Anh - nt.anh.fai@gmail.com"
__name__ = "Foxlabel - Phần mềm chuyên dụng đánh nhãn ảnh Object Detection"
__credits__ = "MIT License"
__console__ = "FoxLabel or ntanh_foxlabel"
__help__ = ""

print(__name__ )
print("Version:",__version__)
print("Console:", __console__)
print(
    """
First time install: pip install  Foxlabel
Update Package    : pip install --upgrade --force-reinstall --no-deps Foxlabel
      """
)
from FoxLabel.FoxLabel import Fmain

def start_program():

    Fmain()
