# -*- coding: utf-8 -*-
import sys
from DisplayCAL import RealDisplaySizeMM, config
from DisplayCAL.dev.mocks import check_call
from DisplayCAL.edid import get_edid
from tests.data.display_data import DisplayData
import pytest


@pytest.mark.skipif(sys.platform == "darwin", reason="not working properly under MacOS")
def test_device_id_from_edid_1():
    """Testing DisplayCAL.colord.device_id_from_edid() function."""
    from DisplayCAL.colord import device_id_from_edid

    with check_call(config, "getcfg", DisplayData.CFG_DATA, call_count=2):
        with check_call(
            RealDisplaySizeMM, "_enumerate_displays", DisplayData.enumerate_displays()
        ):
            edid = get_edid(0)
    device_id = device_id_from_edid(edid)
    assert isinstance(device_id, str)
    assert device_id != ""
