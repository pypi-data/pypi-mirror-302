from .. import util
from ..registry import builtin


@builtin(tag="xbstrap::package")
def xbstrap_package(ctx, node):
    obj = ctx.evaluate(node, tag="tag:yaml.org,2002:map")
    if "architecture" not in obj:
        obj["architecture"] = "@OPTION:arch@"

    return util.represent(obj)


@builtin(tag="meson::setup")
def meson_setup(ctx, node):
    obj = ctx.evaluate(node, tag="tag:yaml.org,2002:map")
    d_args = [f"-D{k}={v}" for k, v in obj.get("defines", {}).items()]
    return util.represent(
        {
            "args": [
                "meson",
                "--cross-file",
                "@SOURCE_ROOT@/scripts/meson-@OPTION:arch-triple@.cross-file",
                "--prefix=/usr",
                "--libdir=lib",
                "--buildtype=debugoptimized",
            ]
            + d_args
            + ["@THIS_SOURCE_DIR@"]
        }
    )


@builtin(tag="ninja::build")
def ninja_build(ctx, node):
    return util.represent(
        {
            "args": [
                "ninja",
            ]
        }
    )


@builtin(tag="ninja::install")
def ninja_install(ctx, node):
    return util.represent(
        {
            "args": [
                "ninja",
                "install",
            ],
            "environ": {
                "DESTDIR": "@THIS_COLLECT_DIR@",
            },
            "quiet": True,
        }
    )
