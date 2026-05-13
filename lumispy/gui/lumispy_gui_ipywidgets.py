# -*- coding: utf-8 -*-
# Copyright 2019-2026 The LumiSpy developers
#
# This file is part of LumiSpy.
#
# LumiSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the license, or
# (at your option) any later version.
#
# LumiSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LumiSpy. If not, see <https://www.gnu.org/licenses/#GPL>.

import ipywidgets
from IPython.display import display as ipy_display


def time2nav_tool_ipy(obj, display=True, **kwargs):
    output = ipywidgets.Output()
    wdict = {}
    apply = ipywidgets.Button(
        description="Apply", tooltip="Apply the selected intervals."
    )

    wdict["apply_button"] = apply

    def on_apply_clicked(b):
        with output:
            output.clear_output()
            try:
                obj.validate_intervals()
            except ValueError as e:
                print("ValueError: " + str(e))
            # if obj.validate_intervals() is False:
            # raise ValueError("negative values in intervals are not allowed")

        obj.apply_button_clicked()

        with output:
            print("Result available via: tool.result")

    apply.on_click(on_apply_clicked)

    box = ipywidgets.VBox([ipywidgets.HBox([apply]), output])

    ipy_display(box)

    obj.widget = box

    return {
        "widget": box,
        "wdict": wdict,
    }
