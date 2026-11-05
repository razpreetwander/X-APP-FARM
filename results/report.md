# APK Analysis Report - ZArchiver

## 1. Source Code Organization (Package-wise)
Decompiled Java/Kotlin source code ko niche diye gaye packages me organize kiya gaya hai:
- **ru.zdevs.zarchiver**: Isme main application class (`ZApp`), main activity (`ZArchiver`), image viewer (`ZImageViewer`), aur text editor (`ZTextEditor`) hain.
- **ru.zdevs.zarchiver.activity**: App ke dialog activities (jaise `SettingsDlg`, `AboutDlg`, `ExtractDlg`, `InstallApkDlg`) yahan hain.
- **ru.zdevs.zarchiver.archiver**: Archive management aur native JNI bridge (`C2JBridge`, `NArc`) ka logic yahan hai.
- **ru.zdevs.zarchiver.io**: File system aur storage I/O handlers (SAF support ke saath).
- **ru.zdevs.zarchiver.ui**: UI controls, views, aur preferences (jaise `FilePanelView`, `EditPassword`).
- **rikka.shizuku / moe.shizuku.api**: Shizuku framework integration elevated permissions ke liye.
- **Third-party libraries**: SlidingPanel, SubScaleView, aur Android Support libraries.

## 2. AndroidManifest Analysis
### Permissions:
- `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE` (Storage access)
- `MANAGE_EXTERNAL_STORAGE` (Scoped storage bypass for Android 11+)
- `ACCESS_SUPERUSER` (Root access support)
- `WAKE_LOCK` (Background tasks ke liye)
- `FOREGROUND_SERVICE` (Service running background tasks)
- `REQUEST_INSTALL_PACKAGES` (APK install karne ke liye)
- `moe.shizuku.manager.permission.API_V23` (Shizuku support)

### Activities:
- `ru.zdevs.zarchiver.ZArchiver`: Main entry point (Launcher activity).
- `ru.zdevs.zarchiver.ZSelectFile`: File picker activity.
- `ru.zdevs.zarchiver.ZImageViewer`: Image viewing feature.
- `ru.zdevs.zarchiver.ZTextEditor`: Text editing feature.

### Services & Providers:
- `ZArchiverService`: Background archiving/extraction tasks.
- `FileProvider` / `ArchiveFileProvider`: File sharing functionality.

## 3. API Endpoints & Network Calls
**Important Finding**: Is APK me `android.permission.INTERNET` permission **nahi hai**.
- App directly internet se communicate nahi karta.
- Source code me koi actual API endpoints nahi mile.
- Kuch URLs mile hain (jaise `zdevs.ru` ya Play Store links) jo sirf browser me help pages ya plugin download karne ke liye open kiye jate hain.
- Cloud support ke liye ye app plugins ka use karta hai, jiske liye alag permission (`ru.zdevs.zarchiver.permission.PLUGIN.CLOUD`) define ki gayi hai.

## 4. Login / Auth Flow
ZArchiver ek local file manager hai, isliye isme network login nahi hai. "Auth" yahan **Archive Passwords** se related hai:
- **Password Input**: `ru.zdevs.zarchiver.ui.text.EditPassword` class password input handle karti hai.
- **Encryption Types**: App AES-128, AES-192, AES-256 aur ZipCrypto encryption support karta hai (`R.string.CMP_ENCRYPT_*`).
- **Flow**: Jab koi user password-protected archive open karta hai ya naya banata hai, `ExtractDlg` ya compression dialog (f0.h, f0.p) `EditPassword` view show karta hai. User ka password native libraries (`libp7zip.so`, `libunrar.so`) ko pass kiya jata hai decryption/encryption ke liye.
- **Internal Security**: `i.a` class internal data encryption ke liye `javax.crypto.Cipher` ka use karti hai.
