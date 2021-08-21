# mac 备份系统
# 找到存储卡，例如 `/dev/disk2`
diskutil list
# 然后取消挂载

# 使用dd进行备份
sudo dd if=/dev/disk2 bs=4m > /path/to/backupImage.img
sudo dd if=/dev/disk2 bs=1m | gzip > /path/to/backupImage.gz
sudo dd if=/dev/disk2 bs=4m | xz -z -e -9 -T 12 -v -c > /path/to/backupImage.xz

# 恢复系统
sudo dd if=/path/to/backupImage.img of=/dev/disk2 bs=4m;sync
gzip -dc /path/to/backupImage.gz | sudo dd of=/dev/disk2 bs=1m
xz -d /path/to/backupImage.xz -c | sudo dd of=/dev/disk2 bs=4m

# 如果系统显示resource busy,表明需要先将TF卡从系统中卸载
df -f # 找到盘符名称，带分区，例如 `/dev/disk2s1`
sudo diskutil unmount /dev/disk2s1 # 卸载