smoke_detection_schema = {
    "type": "object",
    "properties": {
        "forest_fire_smoke_visible": {
            "type": "string",
            "enum": [
                "Yes",
                "No"
            ]
        },
        "forest_fire_flames_visible": {
            "type": "string",
            "enum": [
                "Yes",
                "No"
            ]
        },
        "confirm_uncontrolled_forest_fire": {
            "type": "string",
            "enum": [
                "Yes",
                "Closer investigation required",
                "No forest fire visible"
            ]
        },
        "fire_state": {
            "type": "string",
            "enum": [
                "Ignition Phase",
                "Growth Phase",
                "Fully Developed Phase",
                "Decay Phase",
                "Cannot be determined",
                "No forest fire visible"
            ]
        },
        "fire_type": {
            "type": "string",
            "enum": [
                "Ground Fire",
                "Surface Fire",
                "Crown Fire",
                "Cannot be determined",
                "No forest fire visible"
            ]
        },
        "fire_intensity": {
            "type": "string",
            "enum": [
                "Low",
                "Moderate",
                "High",
                "Cannot be determined",
                "No forest fire visible"
            ]
        },
        "fire_size": {
            "type": "string",
            "enum": [
                "Small",
                "Medium",
                "Large",
                "Cannot be determined",
                "No forest fire visible"
            ]
        },
        "fire_hotspots": {
            "type": "string",
            "enum": [
                "Multiple hotspots",
                "One hotspot",
                "Cannot be determined",
                "No forest fire visible"
            ]
        },
        "infrastructure_nearby": {
            "type": "string",
            "enum": [
                "Yes",
                "No",
                "Cannot be determined",
                "No forest fire visible"
            ]
        },
        "people_nearby": {
            "type": "string",
            "enum": [
                "Yes",
                "No",
                "Cannot be determined",
                "No forest fire visible"
            ]
        },
        "tree_vitality": {
            "type": "string",
            "enum": [
                "Vital",
                "Moderate Vitality",
                "Declining",
                "Dead",
                "Cannot be determined",
                "No forest fire visible"
            ]
        }
    },
    "required": [
        "forest_fire_smoke_visible",
        "forest_fire_flames_visible",
        "confirm_uncontrolled_forest_fire",
        "fire_state",
        "fire_type",
        "fire_intensity",
        "fire_size",
        "fire_hotspots",
        "infrastructure_nearby",
        "people_nearby",
        "tree_vitality"
    ],
    "additionalProperties": False
}