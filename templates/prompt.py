smoke_detection_prompt = """
Analyze the aerial image from the UAV's camera and detect potential forest fires. Answer the following questions based on the image analysis
in a JSON schema. If a question cannot be determined from the image answer with 'Cannot be determined'.

  forest_fire_smoke_visible: Is smoke from a forest fire visible in the image? Answer with one of the following options: ['Yes', 'No']
  forest_fire_flames_visible: Are flames from a forest fire visible in the image? Answer with one of the following options: ['Yes', 'No']
  confirm_uncontrolled_forest_fire: Can you confirm that this is an uncontrolled forest fire? Answer with one of the following options: ['Yes', 'Closer investigation required', 'No forest fire visible']
  fire_state: What is the current state of the forest fire? Answer with one of the following options: ['Ignition Phase', 'Growth Phase', 'Fully Developed Phase', 'Decay Phase', 'Cannot be determined', 'No forest fire visible']
  fire_type: What type of fire is it? Answer with one of the following options: ['Ground Fire', 'Surface Fire', 'Crown Fire', 'Cannot be determined', 'No forest fire visible']
  fire_intensity: What is the intensity of the fire? Answer with one of the following options: ['Low', 'Moderate', 'High', 'Cannot be determined', 'No forest fire visible']
  fire_size: What is the size of the fire? Answer with one of the following options: ['Small', 'Medium', 'Large', 'Cannot be determined', 'No forest fire visible']
  fire_hotspots: Does the forest fire have multiple hotspots? Answer with one of the following options: ['Multiple hotspots', 'One hotspot', 'Cannot be determined', 'No forest fire visible']
  infrastructure_nearby: Is there infrastructure visible near the forest fire? Answer with one of the following options: ['Yes', 'No', 'Cannot be determined', 'No forest fire visible']
  people_nearby: Are there people visible near the forest fire? Answer with one of the following options: ['Yes', 'No', 'Cannot be determined', 'No forest fire visible']
  tree_vitality: Describe the vitality of the trees around the fire. Answer with one of the following options: ['Vital', 'Moderate Vitality', 'Declining', 'Dead', 'Cannot be determined', 'No forest fire visible']
"""