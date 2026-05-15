# EKF TF Bringup

Package ROS 2 ini dibuat untuk mensimulasikan dan membangun TF Tree secara utuh mulai dari `map` -> `odom` -> `base_link` -> `wheels & lasers`. Package ini mengintegrasikan beberapa komponen penting:

1. **Map Server**: Membaca dan memublikasikan `TES.pgm` menggunakan konfigurasi Nav2.
2. **Robot Localization (EKF)**: Menggabungkan (fusing) odometry (`/odom`) dan IMU (`/imu/data`) untuk memublikasikan transformasi dari `odom` ke `base_link`.
3. **Robot State Publisher**: Menggunakan `robot.urdf` untuk memublikasikan TF statik komponen robot (roda mecanum dan sensor Lidar).
4. **Static Transform Publisher**: Sebagai *dummy* untuk memublikasikan transformasi dasar `map` ke `odom`.

---

## 🛠️ Cara Build dan Menjalankan

Karena ini adalah package ROS 2, pastikan Anda berada di direktori *workspace* Anda (`/home/fadlan/Documents/EKF_TES`) sebelum menjalankan perintah.

### 1. Build Package
Buka terminal dan lakukan kompilasi:
```bash
cd ~/Documents/EKF_TES
colcon build --packages-select ekf_tf_bringup
```

### 2. Source Workspace
**Penting:** Jika Anda membuka terminal baru, Anda **wajib** melakukan *source* agar sistem mengenali package yang baru di-build.
```bash
source install/setup.bash
```

### 3. Jalankan Launch File
Jalankan file peluncuran utama yang akan menyalakan Map Server, EKF, dan Robot State Publisher secara bersamaan:
```bash
ros2 launch ekf_tf_bringup tf_launch.py
```

---

## 👁️ Visualisasi dengan RViz2

Untuk melihat hasil peta dan simulasi robot (TF tree) yang telah dibangun, buka terminal baru:

1. Source workspace ROS 2 Anda jika perlu:
   ```bash
   source /opt/ros/humble/setup.bash
   ```
2. Jalankan RViz2:
   ```bash
   rviz2
   ```

### Konfigurasi Tampilan di RViz2:
Setelah aplikasi RViz2 terbuka, lakukan langkah-langkah berikut di panel kiri (`Displays`):

1. **Ubah Global Options:**
   - Ubah kolom `Fixed Frame` dari `map` (atau `odom`) ke **`map`**.

2. **Tambahkan Map:**
   - Klik tombol **`Add`** di bagian bawah panel kiri.
   - Pilih tab **`By topic`**, lalu cari `/map` -> klik **`Map`** -> tekan OK.
   - Peta `TES.pgm` sekarang akan muncul di layar.

3. **Tambahkan TF (Transform):**
   - Klik tombol **`Add`** -> pilih tab **`By display type`** -> pilih **`TF`** -> tekan OK.
   - Ini akan memunculkan garis-garis sumbu koordinat (X merah, Y hijau, Z biru) untuk menunjukkan hierarki `map`, `odom`, `base_link`, roda, dan laser.
   - Anda bisa me-nonaktifkan TF tertentu (misal menyembunyikan TF roda) dengan menekan tanda panah kecil di sebelah tulisan `TF` di panel kiri.

4. **Tambahkan Robot Model (Opsional):**
   - Klik tombol **`Add`** -> pilih **`RobotModel`** -> tekan OK.
   - Di panel `RobotModel`, pastikan kolom `Description Topic` mengarah ke `/robot_description`. Ini akan menampilkan bentuk kotak biru yang merupakan visualisasi robot dari `robot.urdf`.

> **Tip:** Anda dapat menyimpan konfigurasi RViz ini dengan menekan tombol `File` -> `Save Config As...` (misalnya simpan sebagai `my_robot.rviz`) sehingga Anda tidak perlu mengulang pengaturannya lagi di masa depan.
