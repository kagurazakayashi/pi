echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "g_mass_storage" | sudo tee -a /etc/modules
dd if=/dev/zero of=/home/my_u_disk.bin bs=1024 count=1000 #1G
sudo modprobe g_mass_storage file=/home/my_u_disk.bin removable=1 dVendor=0x0781 idProduct=0x5572 bcdDevice=0x011a iManufacturer="SanDisk" iProduct="Cruzer Switch" iSerialNumber="1234567890"

# 在内存中创建
mkdir /mnt/vram
mount -t ramfs none /mnt/vram -o maxsize=6144m
mount ramfs /mnt/vram -t ramfs -o size=6144m

# 格式化为 exfat
apt install exfat-fuse exfat-utils
mkfs.exfat -n USBRAM /mnt/vram
fsck.exfat -n USBRAM /mnt/vram

# 开机启动脚本
sudo vim /etc/rc.local
# 在exit 0 之前添加代码
# 系统启动时在执行这段代码时是使用root用户权限的
