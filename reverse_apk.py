import subprocess
import sys
import os


def list_packages(name):
    print(subprocess.getoutput(f"adb shell pm list packages | grep {name}"))


def get_path_by_package_name(package):
    return subprocess.getoutput(f"adb shell pm path {package}")


def get_app_by_path(paths):
    path = paths.split("apk")[0] + "apk"
    path_final = path.split("package:")[1]
    subprocess.getoutput(f"adb pull {path_final}")


def unpackage_apk():
    subprocess.getoutput("apktool d base.apk")


def get_android_manifest():
    full_manifest_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base/AndroidManifest.xml")
    return subprocess.getoutput(f"cat {full_manifest_path}")


def get_entry_point(manifest):
    part_one = manifest.split("android.intent.category.LAUNCHER")[0]
    part_two = part_one.split("<activity android:")[1]
    part_three = part_two.split("android:name=\"")[1]
    entry_point = part_three.split("\" android:")[0]
    print(entry_point)


def turn_debuggable(manifest, package):
    part_one = manifest.split("<application ")[0]
    part_two = manifest.split("<application ")[1]
    final = part_one + '<application android:debuggable="true" ' + part_two
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base/AndroidManifest.xml"), 'w') as file:
        file.write(final)
    print("TAG DEBUGGABLE INJECTED!")
    subprocess.getoutput("rm fucked.apk")
    print("COMPILING DEBUGGABLE APK")
    subprocess.getoutput("apktool b base -o fucked.apk")
    print("ASSIGNING APK")
    subprocess.getoutput("apksigner sign --ks fuck.keystore --ks-pass file:my-passfile.txt --v1-signing-enabled true --v2-signing-enabled true fucked.apk")
    print("UNINSTALLING OLD APK")
    subprocess.getoutput(f"adb uninstall {package}")
    print("INSTALLING APK")
    subprocess.getoutput("adb install -r -t fucked.apk")


def reverse_by_package(package, is_debuggable):
    print("Identificando caminho do aplicativo\n")
    paths = get_path_by_package_name(package)
    print("Clonando aplicativo\n")
    print(get_app_by_path(paths))
    print("Desempacotando aplicativo\n")
    print(unpackage_apk())
    manifest = get_android_manifest()
    if is_debuggable:
        turn_debuggable(manifest, package)
    else:
        get_entry_point(manifest)


def print_options():
    print("Reverse application\n")
    print("-p to get entrypoint by packagename\n")
    print("-n to get package name that contains the name\n")
    print("-d turn the apk debuggable by package name example reverse_apk.py -d com.oxxy.app")


if __name__ == "__main__":
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-h":
            print_options()
        if sys.argv[i] == "-p":
            reverse_by_package(sys.argv[i + 1], False)
        if sys.argv[i] == "-n":
            list_packages(sys.argv[i + 1])
        if sys.argv[i] == "-d":
            reverse_by_package(sys.argv[i + 1], True)
