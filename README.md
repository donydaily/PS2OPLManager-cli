# 🎮 oplmgr — PS2 OPL USB Manager for Linux

`oplmgr` adalah **tool CLI Linux-native** untuk mengelola game **PlayStation 2 (PS2)** yang digunakan dengan **OPL (Open PS2 Loader)**, khususnya untuk **USB / harddisk external (FAT32)**.

Tool ini dibuat sebagai **alternatif Linux** untuk **USBUtil / OPL Manager (Windows)**, dengan fokus pada:

* cepat
* ringan
* scriptable
* cocok untuk power-user Linux (Arch, Ubuntu, Mint, dll)

---

## ✨ Fitur

* ✅ **Dual mode:** CLI **dan** Interactive UI (fzf)
* ✅ Convert **ISO → format OPL USB**
* ✂️ Split otomatis **1GB (FAT32 safe)**
* 🔍 Auto-detect **USB PS2** (tanpa `--usb`)
* 🆔 Deteksi **Game ID (SLUS/SLES/SCUS)**
* 💿 Deteksi **CD / DVD** otomatis
* 🗂 Generate, update & **rebuild `ul.cfg`**
* 📃 List game di USB
* ✏️ Rename judul game (metadata)
* 🗑 **Delete game (bersih + aman)**
* 📊 Progress bar CLI

---

## 🖥️ Sistem yang Didukung

* Linux (Arch Linux, Ubuntu, Linux Mint, dll)
* Python **≥ 3.10**
* File system USB: **FAT32** (wajib untuk PS2)

---

## 📦 Dependency

### Dependency Sistem

Pastikan Python sudah terpasang:

```bash
python --version
```

Jika belum:

```bash
# Arch Linux
sudo pacman -S python

# Ubuntu / Mint
sudo apt install python3
```

### Dependency Python

Install via `pip`:

```bash
pip install pycdlib tqdm psutil
```

### Dependency Tambahan (UI Mode)

Untuk menggunakan **Interactive UI**:

```bash
# Arch Linux
sudo pacman -S fzf

# Ubuntu / Mint
sudo apt install fzf
```

---

## 📂 Struktur Project

```text
PS2OPLManager-cli/
├── oplmgr           # CLI utama
├── iso.py           # Deteksi Game ID & tipe CD/DVD
├── splitter.py      # Split ISO 1GB
├── ulcfg.py         # Handler ul.cfg
├── usb.py           # Auto-detect USB PS2
├── meta.py          # Rename / metadata
└── utils.py         # Helper (opsional)
```

---

## 💾 Struktur USB PS2 (OPL)

USB **harus FAT32** dan memiliki struktur:

```text
/PS2_USB/
├── DVD/
├── CD/
└── ul.cfg
```

Jika folder `DVD` / `CD` belum ada, `oplmgr` akan membuatnya otomatis.

---

## 🚀 Instalasi

Clone atau salin source code:

```bash
git clone https://github.com/donydaily/PS2OPLManager-cli.git
cd oplmgr
```

Beri izin eksekusi:

```bash
chmod +x oplmgr.py
```

(Opsional) Pasang global:

```bash
sudo ln -s $(pwd)/oplmgr /usr/local/bin/oplmgr
```

Sekarang bisa dipanggil dengan:

```bash
oplmgr
```

---

## 🎛️ Mode Penggunaan

`oplmgr` bisa digunakan dengan **dua mode**:

### 1️⃣ Mode CLI (Manual / Scriptable)

Cocok untuk automation, scripting, atau SSH.

```bash
oplmgr add game.iso
oplmgr list
oplmgr rename SLUS_203.12 "God of War"
oplmgr delete SLUS_203.12
oplmgr rebuild
```

### 2️⃣ Mode UI (fzf Interactive)

Mode interaktif mirip OPL Manager Windows, tapi tetap CLI.

```bash
oplmgr ui
```

Fitur UI:

* Pilih game pakai keyboard
* Tidak perlu hafal GAME ID
* Rename / Delete / Rebuild dari menu

---

## 🔌 Auto Detect USB PS2

`oplmgr` akan otomatis mencari:

* Partisi **FAT32**
* Memiliki folder `DVD/` atau `CD/`

Jika USB PS2 terdeteksi, kamu **tidak perlu** menulis path manual.

Jika tidak terdeteksi:

* Pastikan USB sudah di-mount
* Pastikan FAT32
* Pastikan folder `DVD` atau `CD` ada

---

## 📥 Menambahkan Game ISO

### Tambah satu ISO

```bash
oplmgr add game.iso
```

Yang terjadi:

1. ISO dibaca
2. Game ID terdeteksi
3. ISO di-split 1GB
4. File dimasukkan ke `DVD/` atau `CD/`
5. `ul.cfg` di-update

---

### Tambah banyak ISO (folder)

```bash
oplmgr add ./iso/
```

Semua file `.iso` dalam folder akan diproses.

---

## 📃 Melihat Daftar Game

```bash
oplmgr list
```

Contoh output:

```text
SLUS_203.12  DVD  God of War
SLUS_209.46  DVD  Resident Evil 4
SCES_533.26  CD   Shadow of the Colossus
```

---

## ✏️ Rename Judul Game

Rename hanya mengubah **judul di `ul.cfg`**, tidak mengubah file game.

```bash
oplmgr rename SLUS_203.12 "God of War (USA)"
```

---

## 🗑 Menghapus Game (Delete)

Menghapus game **secara aman & bersih**:

* Semua file `ul.<GAME_ID>.*` dihapus
* Entri di `ul.cfg` dibersihkan

```bash
oplmgr delete SLUS_203.12
```

Gunakan ini **jangan hapus manual**, agar OPL tidak error.

---

## 🧹 Rebuild `ul.cfg`

Digunakan jika:

* Game tidak muncul di OPL
* `ul.cfg` rusak / duplikat
* Habis hapus / copy file manual

`oplmgr rebuild` akan:

* Scan folder `DVD/` dan `CD/`
* Sinkronkan ulang `ul.cfg` dari file asli
* Menghapus entri hantu / duplikat

```bash
oplmgr rebuild
```

⚠️ Sangat direkomendasikan setelah perubahan manual.

---

## ⚠️ Catatan Penting

* ❗ Gunakan **ISO PS2 valid**
* ❗ USB **HARUS FAT32**
* ❗ Jangan rename file `ul.*` manual
* ❗ Jangan hapus `ul.cfg`
