import subprocess


def asrun(ascript):
    osa = subprocess.run(
        ["/usr/bin/osascript", "-"], input=ascript, text=True, capture_output=True
    )
    if osa.returncode == 0:
        return osa.stdout.rstrip()
    else:
        raise ChildProcessError(f"AppleScript: {osa.stderr.rstrip()}")


def add_reminder(list_name: str, item: str, note: str = ""):
    with open("add-item.scpt", "r") as f:
        template = f.read()

    script = (
        template.replace("%LIST%", list_name)
        .replace("%ITEM%", item)
        .replace("%NOTE%", note)
    )

    return asrun(script)
