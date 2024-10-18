"""
FoxLabel

An python parametters library.
"""

__version__ = "1.3"
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
Cách dùng phần mềm:
- Bước 1: Mở thư mục ảnh bằng 'Open Dir'
- Bước 2: Đánh nhãn
    - Chú ý các phím tắt trên menu.
    - Hover chuột vào nhãn nào, thì nhìn tên của nó phía dưới phải (đầu tiên của status bar dưới phải)
    - Bấm chuột vào góc box để thay đổi kích thước
    - Bấm chuột vào vùng của box để di chuyển nó
    - Ctr_lăn chuột để zoom ảnh
    - Các phím tắt:
        - a, s, d, f, z, 1, e, 3, Ctr_1, Ctr_2, Ctr_3, Ctr_9
        - a: Lùi, cho đến đầu thì hiện thông báo
        - d: tiến cho đến cuối thì hiện thông báo
        - s: lưu 
        - f: dán box cuối cùng đã save, tự động save luôn
        - z: xóa box
        - 1: tạo mới box
        - e: edit label của box
        - 3: nhân đôi box được chọn
        - Ctrl+1: Copy last box saved từ file ra, nghĩa là có thể copy xuyên các lần đánh nhãn khác nhau (sau khi tắt phần mềm)
        - Ctrl+2, Ctrl+3: Convert video => image, edit, thêm sửa xóa image => Gộp lại thành video.
        - Ctrl+9: Đánh nhãn hết các file chưa có label, dùng nhãn save lần cuối, đánh trong thư mục gốc của Open Dir


    
First time install: pip install  Foxlabel
Update Package    : pip install --upgrade --force-reinstall --no-deps Foxlabel
      """
)
from FoxLabel.FoxLabel import Fmain

def start_program():

    Fmain()
