from core import BridgeFactory, BridgeCalculator, BridgeData, LoadApplier
from utilities import Point, display_float, kN
import quantities as pq
from graphics import BridgeGUI

if __name__ == "__main__":
    # Bridge constants
    AREA_LOAD = (5 + 1 + 0.75) * kN / pq.m ** 2
    WIDTH = 3.7 * pq.m
    SPAN = 107.96 / 3 * pq.m
    HEIGHT_WIDTH_RATIO = 1
    NUMBER_OF_PANELS = 8

    SUPPORTS = {
        Point(0 * pq.m, 0 * pq.m),
        Point(SPAN, 0 * pq.m)
    }

    bridge_factory = BridgeFactory()

    beams = bridge_factory.get_beams_for_k_bridge(NUMBER_OF_PANELS, SPAN, HEIGHT_WIDTH_RATIO)

    bridge = BridgeData(beams)

    load_applier = LoadApplier(bridge, SUPPORTS)
    # load_applier.add_point_load(Point(SPAN / 2, 0 * pq.m), 1 * kN)
    load_applier.add_uniformly_distributed_load(AREA_LOAD * WIDTH / 2)

    bridge_calculator = BridgeCalculator(bridge)
    bridge_calculator.calculate_member_forces()
    bridge_calculator.calculate_highest_member_forces()
    bridge_calculator.calculate_min_area_and_i()

    GUI = BridgeGUI()
    GUI.draw_bridge(bridge_calculator)

    GUI.add_information(f"Area Load: {display_float(AREA_LOAD)}")
    GUI.add_information(f"Width: {display_float(WIDTH)}")
    GUI.add_information(f"Span: {display_float(SPAN)}")
    GUI.add_information(f"Height/Width ratio: {display_float(HEIGHT_WIDTH_RATIO)}")

    for beam_group, beam_group_property in bridge_calculator.beam_groups.items():
        GUI.add_information(
            f"{beam_group.name} ({beam_group.color}): "
            f"Minimum area: {display_float(beam_group_property.min_area.rescale('mm**2'))}")
        GUI.add_information(f"{beam_group.name} ({beam_group.color}): Minimum I: "
                            f"{display_float(beam_group_property.min_i.rescale('mm**4') / 10 ** 6)}*10**6")

    GUI.display()
