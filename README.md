# ros_ujian_semester4_tengah-semester

Repository ini digunakan untuk membuat simulasi gazebo untuk ujian tengah semester 4.

Catatan yang sudah dilakukan:

1. Membuat design.
2. Memvalidasi simulasi dengan bounding box sederhana dan tetap menggunakan design sebagai skin.
3. menambahkan inertia robot
4. memastikan integrasi ros dan gazebo - robot sudah terjadi.
5. sudah dapat bergerak secara sederhana untuk maju menggunakan cmd_vel.
6. Percobaan dengan teleop
7. Penambahan imu ke dalam robot dan dapat di echo topic nya untuk melihat hasil.

Yang belum dilakukan (TODO):

1. Kalibrasi parameter noise IMU agar sesuai kebutuhan eksperimen
2. Odometry & Pose Monitoring dimana akan memonitoring pose dengan ros2
3. Integrasi dengan rviz (walaupun sudah bisa, namun akan di coba lagi nanti) dimana akan melihat robot dan pose secara visual.

## Integrasi Sensor IMU

Sensor IMU sudah ditambahkan pada model robot melalui file xacro dan datanya dipublish ke ROS 2 melalui ros_gz_bridge.

Topik yang digunakan:

1. Topic simulasi (Gazebo): /imu
2. Topic ROS 2 hasil bridge: /imu (sensor_msgs/msg/Imu)

Langkah menjalankan simulasi dengan IMU:

1. Build workspace:

```bash
colcon build --packages-select my_robot
source install/setup.bash
```

2. Jalankan simulasi Gazebo:

```bash
ros2 launch my_robot gazebo.launch.py
```

3. Buka terminal lain untuk memantau data IMU:

```bash
source install/setup.bash
ros2 topic list | grep imu
ros2 topic echo /imu
```

4. Opsional, cek frekuensi publish IMU:

```bash
source install/setup.bash
ros2 topic hz /imu
```

Catatan:

1. Update rate IMU saat ini diset 100 Hz di file robot.xacro.
2. Data IMU mencakup orientation, angular_velocity, dan linear_acceleration.
3. Noise sensor sudah diaktifkan agar perilaku simulasi lebih realistis.

## Menjalankan kontrol cmd_vel

1. Build workspace:

```bash
colcon build --packages-select my_robot
source install/setup.bash
```

2. Jalankan simulasi Gazebo:

```bash
ros2 launch my_robot gazebo.launch.py
```

3. Buka terminal lain, lalu jalankan cmd vel beserta kecepatan yang diinginkan:

```bash
source install/setup.bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.01}, angular: {z: 0.0}}"
```

4. Untuk mengubah kecepatan atau rotasi, nilai pada point 3 dapat diubah linear atau angularnya.

## Menjalankan Teleop Keyboard

1. Build workspace:

```bash
colcon build --packages-select my_robot
source install/setup.bash
```

2. Jalankan simulasi Gazebo:

```bash
ros2 launch my_robot gazebo.launch.py
```

3. Buka terminal lain, lalu jalankan teleop:

```bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel
```

4. Gunakan tombol pada jendela teleop (misalnya i, j, l, k) untuk menggerakkan robot.
