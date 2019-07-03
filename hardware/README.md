INSTALL script copies files to
/usr/bin,
/etc/systemd/system,
/etc/udev/rules.d
and reloads udev rules and systemctl daemon
Be aware of the fact that rsync puts data from camera to
/tmp/AlexN/camera_,
camera_ directory name is from .id_camera file that can be found
in each camera. Let it be like that for now.
