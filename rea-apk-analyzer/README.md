# APK Analyzer

## Setup (ek baar)
Settings -> Secrets and variables -> Actions me ye secrets add karo:
- `GEMINI_API_KEY` - zaroori, analysis/edit ke liye.
- `KEYSTORE_BASE64` - zaroori AAB/APK signing ke liye. Apni .jks/.keystore file ko base64 karo:
  `base64 -w0 apna.keystore > keystore.txt` (ya Mac: `base64 -i apna.keystore -o keystore.txt`), uska content paste karo.
- `KEYSTORE_PASSWORD` - keystore ka password.
- `KEY_ALIAS` - key alias ka naam.
- `KEY_ALIAS_PASSWORD` - alias ka password (agar keystore password jaisa hi hai to wahi daal do).
- `BOSS_EMAIL`, `EMAIL_APP_PASS` - optional, email updates ke liye (Gmail app password).

## Har run ke liye
1. APK daalo: (a) chhota ho to `apk/` folder me, ya (b) bada ho to Releases me naya release banake APK attach karo
2. `changes.txt` me likho kya karna hai. Agar koi actual code/resource change chahiye (jaise color/text/behaviour), to wo clearly, ek line me likho.
3. Actions -> APK Analyze -> Run workflow

## Output (Artifacts, run page se)
- `recovered-source` - zip: decompiled source (`source_with_changes` agar changes apply hue, warna `source_raw`), apktool resources+smali, native libs, reports.
- `app-release-apk` - signed APK.
- `app-release-aab` - signed AAB.
- `report` - raw report folder.

## Kaise decide hota hai changes wala vs raw
- Gemini pehle `out/jadx_project` me changes.txt ke actual code changes apply karta hai, aur `report/report.md` ke end me `CHANGES_APPLIED: yes/no` likhta hai.
- Agar `yes`: changed source se build/sign try hota hai.
- Agar `no`, ya changed source build/sign me fail ho jaye: automatically bina-change wale original (`pristine`) source se build/sign hota hai, fallback.
- `report/build_status.md` me likha milega konsa version mila aur kyun.

## Honest limits
- Decompiled source approximation hai: comments, original variable naam (agar obfuscated), aur exact Gradle build files wapas nahi aate.
- AI se decompiled/obfuscated code edit karke recompile karna unreliable hai, khaaskar badi ya heavily obfuscated apps me. Jab bhi edit fail ho, bina-change wala APK/AAB milega, taaki kuch na kuch usable zaroor mile.
- Native (.so) ka source code nahi milta, sirf pseudo-C report me.
- AAB/APK naye keystore se sign hote hain (tumhari apni keystore). Play Store par existing app update karne ke liye wahi original upload key use karo, warna update reject ho sakta hai.
- Sirf apni ya permission wali APK analyze karo.
