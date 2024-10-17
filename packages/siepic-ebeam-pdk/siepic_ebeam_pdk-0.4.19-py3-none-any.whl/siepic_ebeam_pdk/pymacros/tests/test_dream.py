"""

by Lukas Chrostowski 2024

"""

designer_name = "Example"
top_cell_name = "EBeam_%s_MZI" % designer_name

import pya
from pya import *

import siepic_ebeam_pdk
from SiEPIC.scripts import connect_pins_with_waveguide, export_layout
from SiEPIC.utils.layout import new_layout

import os


def test_dream():
    tech_name = "EBeam"
    from SiEPIC.utils import get_technology_by_name

    TECHNOLOGY = get_technology_by_name(tech_name)

    cell, ly = new_layout(tech_name, top_cell_name, GUI=True, overwrite=True)

    waveguide_type = "Strip TE 1550 nm, w=500 nm"

    cell_1 = ly.create_cell("ebeam_dream_microlens_edge_couplers_BB", "EBeam-Dream", {})
    t = pya.Trans.from_s("r0 %s, %s" % (0, 0))
    inst1 = cell.insert(pya.CellInstArray(cell_1.cell_index(), t))

    # Test Dream library import
    for lib in pya.Library().library_ids():
        li = pya.Library().library_by_id(lib)
        if not li.is_for_technology(ly.technology_name) or li.name() == "Basic" or "dream" not in li.name().lower():
            # print(" - skipping library: %s" % li.name())
            continue

        # all the pcells
        print(" - Library: %s" % li.name())
        print("   All PCells: %s" % li.layout().pcell_names())


    # Save
    path = os.path.dirname(os.path.realpath(__file__))
    filename = "test_dream"
    file_out = export_layout(cell, path, filename, relative_path="", format="oas")

    from SiEPIC.utils import klive

    klive.show(file_out, technology=tech_name, keep_position=True)


if __name__ == "__main__":
    test_dream()
