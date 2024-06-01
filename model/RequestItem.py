class Item:
    def __init__(self,
                 is_support_material: bool,
                 perimeter_speed: float,
                 small_perimeter_speed: float,
                 external_perimeter_speed: str,
                 infill_speed: float,
                 solid_infill_speed: float,
                 top_solid_infill_speed: float,
                 gap_fill_speed: float,
                 bridge_speed: float,
                 support_material_speed: float,
                 travel_speed: float,
                 first_layer_speed: float):
        self.is_support_material = is_support_material
        self.perimeter_speed = perimeter_speed
        self.small_perimeter_speed = small_perimeter_speed
        self.external_perimeter_speed = external_perimeter_speed
        self.infill_speed = infill_speed
        self.solid_infill_speed = solid_infill_speed
        self.top_solid_infill_speed = top_solid_infill_speed
        self.gap_fill_speed = gap_fill_speed
        self.bridge_speed = bridge_speed
        self.support_material_speed = support_material_speed
        self.travel_speed = travel_speed
        self.first_layer_speed = first_layer_speed

    def to_dict(self):
        return {
            'perimeter_speed': self.perimeter_speed,
            'small_perimeter_speed': self.small_perimeter_speed,
            'external_perimeter_speed': self.external_perimeter_speed,
            'infill_speed': self.infill_speed,
            'solid_infill_speed': self.solid_infill_speed,
            'top_solid_infill_speed': self.top_solid_infill_speed,
            'gap_fill_speed': self.gap_fill_speed,
            'bridge_speed': self.bridge_speed,
            'support_material_speed': self.support_material_speed,
            'travel_speed': self.travel_speed,
            'first_layer_speed': self.first_layer_speed,
        }
