import dataclasses
import subprocess
from typing import List


@dataclasses.dataclass(frozen=True)
class TestDevice:
    """Describes a device that can be used for testing"""
    name: str
    udid: str
    version: str | None = None
    preferred: bool = False

    def __repr__(self):
        return "<TestDevice named '{name}' running {platform}:{version}, UDID={udid}".format(
            **self.__dict__)


def __exec(params: List[str], check=True) -> List[str]:
    pipe = subprocess.run(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)
    return [s.strip() for s in pipe.stdout.decode('utf-8').split('\n')]


def __get_adb_device_prop(adb_name: str, prop_name: str) -> str:
    return __exec(['adb', '-s', adb_name, 'shell', 'getprop', prop_name])[0]


def get_devices() -> List[TestDevice]:
    """Retrieve all available TestDevices"""
    devices: List[TestDevice] = []
    devices.extend(get_android_devices())
    return devices


def get_android_devices() -> List[TestDevice]:
    """
    Retrieve a list of Android devices connected to the machine
    """
    devices: List[TestDevice] = []
    all_devices_info = __exec(['adb', 'devices'])

    for line in all_devices_info:
        if len(line) == 0 or line.startswith('List of devices') or line == '== Devices Offline ==':
            continue

        adb_device_name = line.split("\t")[0]
        version = __get_adb_device_prop(adb_device_name, 'ro.build.version.sdk')
        udid = __get_adb_device_prop(adb_device_name, 'ro.serialno')

        device = TestDevice(name=adb_device_name, version=version, udid=udid)
        devices.append(device)

    return devices


def _get_standard_capabilities():
    return {
        "autoAcceptAlerts":  True,
        "autoDismissAlerts": True,
        "newCommandTimeout": 15000,
    }


def get_capabilities_android(device: TestDevice) -> dict:
    """ Get caps for an Android device """
    return {
        "automationName":  "UIAutomator2",
        "platformName":    "Android",
        "platformVersion": device.version,
        "udid":            device.name,
        **_get_standard_capabilities()
    }


def get_local_device_caps():
    """ Get the first local device matching the `platform` """
    _devices = get_android_devices()
    if len(_devices) == 0:
        raise ConnectionError("No physical devices available")

    found = _devices[0]
    print(f"Selected device '{found.name}'")
    return get_capabilities_android(found)


def execute_commands(command: List[str], check_output: bool = True) -> str | subprocess.Popen:
    if not check_output:
        return subprocess.Popen(command)
    else:
        return subprocess.check_output(command).decode("utf-8")
