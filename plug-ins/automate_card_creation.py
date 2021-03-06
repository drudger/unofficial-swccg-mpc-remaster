#!/usr/bin/python
 
from gimpfu import *

import json
PLACEHOLDER_JSON = "/home/chris/SWCCG/data/json/Sets/Premiere/Dark/Boring Conversation Anyway.json"
PLACEHOLDER_IMAGE = "/home/chris/Downloads/gemp-cards/cropped/boringconversationanyway.gif"

#region Magic Numbers
 
#region Text Layer Names
ABILITY_ARMOR_TEXT_LAYER = "Ability Armor Text"
CARD_TITLE_TEXT_LAYER = "Card Title Text"
CARD_TYPE_TEXT_LAYER = "Card Type Text"
DEPLOY_TEXT_LAYER = "Deploy Text"
DESTINY_TEXT_LAYER = "Destiny Text"
DROID_EXTRA_TEXT_LAYER = "Droid ExtraText"
FORFEIT_TEXT_LAYER = "Forfeit Text"
GAME_TEXT_LAYER = "Game Text #1"
LORE_TEXT_LAYER = "Lore Text"
NON_DROID_TEXT_GROUP = "Non-Droid Fields"
POWER_TEXT_LAYER = "Power Text"
SENSITIVITY_TEXT_LAYER = "Sensitivity Text"
#endregion

#region Visible/Invisible
INVISIBLE = False
VISIBLE = True
#endregion

#region Art Vars
# Art size
ART_WIDTH = 1200
ART_HEIGHT = 800

# Art Offsets
ART_OFFSET_X = 219
ART_OFFSET_Y = 633
#endregion

#region Label Layer Names
ABILITY_LABEL_LAYER = "ABILITY LABEL"
ARMOR_LABEL_LAYER = "ARMOR LABEL"
POWER_LABEL_LAYER = "POWER LABEL"
#endregion

#region Lower Right Icons
LOWER_RIGHT_ICONS_GROUP = "Lower Right Specialty Icons"
TOP_PILOT_ICON_LAYER = "Top-Pilot-Icon"
TOP_WARRIOR_ICON_LAYER = "Top-Warrior-Icon"
MIDDLE_WARRIOR_ICON_LAYER = "Middle-Warrior-Icon"
BOTTOM_WARRIOR_ICON_LAYER = "Bottom-Warrior-Icon"
#endregion

#region Specialty Icon Border Layers
SPEC_BORDER_TOP_LAYER = "Top Border"
SPEC_BORDER_MIDDLE_LAYER = "Middle Border"
SPEC_BORDER_BOTTOM_LAYER = "Bottom Border"
#endregion

#region Text Field Values
ABILITY_TEXT = "ABILITY"
ARMOR_TEXT = "ARMOR"
LORE_FIRST_LINE_MAX_CHARS = 49
LORE_SPACER = "      "
POWER_TEXT = "POWER"
#endregion

#region Template Names
TEMPLATE_ALIEN = "Template-Alien"
TEMPLATE_BATTLE_DROID = "Template-Battle-Droid"
TEMPLATE_DROID = "Template-Droid"
TEMPLATE_EFFECT = "Template-Effect"
TEMPLATE_IMPERIAL = "Template-Imperial"
TEMPLATE_INTERRUPT = "Template-Interrupt"
TEMPLATE_REBEL = "Template-Rebel"
#endregion

#endregion

#region Main Function
def automate_card_creation(image, drawable, json_file, image_file):

  # Error Checking
  if json_file.find(".json") == -1:
    message = "ERROR: Json File must end with .json"
    print( message )
    pdb.gimp_message( message )
    return None

  ### Create Undo Group ###
  pdb.gimp_image_undo_group_start(image)

  # Store Card Data In Var
  card_data = []
  card_data = get_card_data(json_file)

  # Card Title, Destiny, 
  insert_universal_fields(image, card_data)
  insert_art_into_image(image, image_file)

  card_type = card_data["front"]["type"]

  if card_type == "Character":
    # Character Card
    insert_character_data(image, card_data)
  elif card_type == "Starshp":
    print("Starship")
  elif card_type == "Vehicle":
    print("Vehicle")
  elif card_type == "Weapon":
    print("Weapon")
  elif "&" in card_data["front"]["title"]:
    print("Combo Card")
  elif card_type == "Effect"or card_type == "Interrupt":
    insert_effect_interrupt(image, card_data)

  ### End Undo Group ###
  pdb.gimp_image_undo_group_end(image)

#endregion

def insert_character_data(image, card_data):

  toggle_character_template(image, card_data)

  insert_power_data(image, card_data)

  insert_deploy_and_forfeit(image, card_data)

  insert_ability_and_extra_text(image, card_data)

  # Check for Specialty Icons
  if "icons" in card_data["front"]:

    insert_specialty_icons(image, card_data)

def insert_effect_interrupt(image, card_data):
  # Turn on Card Type layer and fill it
  card_type_layer = pdb.gimp_image_get_layer_by_name(image, CARD_TYPE_TEXT_LAYER)
  make_visible(card_type_layer)

  # Construct card type and insert it
  sub_type = ""
  base_type = card_data["front"]["type"]

  if "subType" in card_data["front"]:
    sub_type = card_data["front"]["subType"] + " "

  combined_card_type = sub_type + base_type
  pdb.gimp_text_layer_set_text( card_type_layer, combined_card_type.upper() )

  # Toggle templates off
  make_invisible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_INTERRUPT) )
  make_invisible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_EFFECT) )

  # Toggle on appropriate template
  if card_data["front"]["type"] == "Interrupt":
    make_visible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_INTERRUPT) )
  if card_data["front"]["type"] == "Effect":
    make_visible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_EFFECT) )


def insert_specialty_icons(image, card_data):
    icons = card_data["front"]["icons"]
    num_icons = len( icons )
    if "Warrior x2" in icons:
      num_icons += 1

    insert_specialty_borders(image, num_icons)

    if "Pilot" in icons:
      make_visible(  pdb.gimp_image_get_layer_by_name(image, TOP_PILOT_ICON_LAYER) )

      if "Warrior" in icons:
        make_visible(  pdb.gimp_image_get_layer_by_name(image, MIDDLE_WARRIOR_ICON_LAYER) )
      elif "Warrior x2" in icons:
        make_visible(  pdb.gimp_image_get_layer_by_name(image, MIDDLE_WARRIOR_ICON_LAYER) )
        make_visible(  pdb.gimp_image_get_layer_by_name(image, BOTTOM_WARRIOR_ICON_LAYER) )

    elif "Warrior" in icons:
      make_visible(  pdb.gimp_image_get_layer_by_name(image, TOP_WARRIOR_ICON_LAYER) )

    elif "Warrior x2" in icons:
      make_visible(  pdb.gimp_image_get_layer_by_name(image, TOP_WARRIOR_ICON_LAYER) )
      make_visible(  pdb.gimp_image_get_layer_by_name(image, MIDDLE_WARRIOR_ICON_LAYER) )

def insert_specialty_borders(image, num_icons):
  make_visible(  pdb.gimp_image_get_layer_by_name(image, SPEC_BORDER_TOP_LAYER) )

  if num_icons > 1:
    make_visible(  pdb.gimp_image_get_layer_by_name(image, SPEC_BORDER_MIDDLE_LAYER) )
  if num_icons > 2:
    make_visible(  pdb.gimp_image_get_layer_by_name(image, SPEC_BORDER_BOTTOM_LAYER) )

def insert_ability_and_extra_text(image, card_data):
  # Check if Character a Droid
  if card_data["front"]["subType"] == "Droid":

    # Remove Ability Label
    make_invisible( pdb.gimp_image_get_layer_by_name(image, ABILITY_LABEL_LAYER) )

    # Check if Droid is a Battle-Droid
    if "armor" in card_data["front"]:
      droid_armor_text_layer = pdb.gimp_image_get_layer_by_name(image, ABILITY_ARMOR_TEXT_LAYER)
      extra_text_layer = pdb.gimp_image_get_layer_by_name(image, SENSITIVITY_TEXT_LAYER)

      make_visible( pdb.gimp_image_get_layer_by_name(image, ARMOR_LABEL_LAYER) )
      make_visible( extra_text_layer )
      make_visible( droid_armor_text_layer )

      text = card_data["front"]["armor"]
      pdb.gimp_text_layer_set_text(droid_armor_text_layer, text)
      pdb.gimp_text_layer_set_text(extra_text_layer, card_data["front"]["extraText"][0])
    else:
      make_invisible( pdb.gimp_image_get_layer_by_name(image, ABILITY_LABEL_LAYER) )
      make_invisible( pdb.gimp_image_get_layer_by_name(image, ABILITY_ARMOR_TEXT_LAYER) )
      make_invisible( pdb.gimp_image_get_layer_by_name(image, SENSITIVITY_TEXT_LAYER) )
      droid_extra_text_layer = pdb.gimp_image_get_layer_by_name(image, DROID_EXTRA_TEXT_LAYER) 
      make_visible( droid_extra_text_layer )
      text = card_data["front"]["extraText"][0]
      pdb.gimp_text_layer_set_text(droid_extra_text_layer, text)
  else:
    # Change Ability Armor Text
    make_invisible( pdb.gimp_image_get_layer_by_name(image, ARMOR_LABEL_LAYER) )
    make_visible( pdb.gimp_image_get_layer_by_name(image, ABILITY_LABEL_LAYER) )
    make_visible( pdb.gimp_image_get_layer_by_name(image, ABILITY_ARMOR_TEXT_LAYER) )
    ability_armor_text_layer = pdb.gimp_image_get_layer_by_name(image, ABILITY_ARMOR_TEXT_LAYER)
    text = card_data["front"]["ability"]
    pdb.gimp_text_layer_set_text(ability_armor_text_layer, text)

    # Check for extra text
    if "extraText" in card_data["front"]:
      # Change Sensitivity Text
      sensitivity_text_layer =  pdb.gimp_image_get_layer_by_name(image, SENSITIVITY_TEXT_LAYER)
      make_visible( sensitivity_text_layer )
      text = card_data["front"]["extraText"][0]
      pdb.gimp_text_layer_set_text(sensitivity_text_layer, text)

def insert_power_data(image, card_data):
    # Change Power Text
    power_text_label_layer = pdb.gimp_image_get_layer_by_name(image, POWER_LABEL_LAYER)
    power_text_layer = pdb.gimp_image_get_layer_by_name(image, POWER_TEXT_LAYER)
    pdb.gimp_text_layer_set_text(power_text_layer, card_data["front"]["power"])
    make_visible(power_text_label_layer)
    make_visible(power_text_layer)

def toggle_character_template(image, card_data):
  dark_light = card_data["side"]

  templates_dict = populate_character_templates_dict(image, dark_light)

  for template in templates_dict:
    make_invisible( pdb.gimp_image_get_layer_by_name(image, template) )

  subType = card_data["front"]["subType"]

  if subType == "Alien":
    make_visible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_ALIEN) )
  elif subType == "Rebel":
    make_visible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_REBEL) )
  elif subType == "Droid":
    if "armor" in card_data["front"]:
      make_visible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_BATTLE_DROID) )
    else:
      make_visible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_DROID) )
  elif subType == "Imperial":
    make_visible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_IMPERIAL) )
  else:
    make_visible( pdb.gimp_image_get_layer_by_name(image, TEMPLATE_REBEL) )

def populate_character_templates_dict(image, dark_light):
  # Both Sides
  template_alien_layer = pdb.gimp_image_get_layer_by_name(image, TEMPLATE_ALIEN)
  template_battle_droid_layer = pdb.gimp_image_get_layer_by_name(image, TEMPLATE_BATTLE_DROID)
  template_droid_layer = pdb.gimp_image_get_layer_by_name(image, TEMPLATE_DROID)

  templates_dict = {
    TEMPLATE_ALIEN: template_alien_layer,
    TEMPLATE_BATTLE_DROID: template_battle_droid_layer,
    TEMPLATE_DROID: template_droid_layer,
  }

  # Light Side
  if dark_light == "Light":
    template_rebel_layer = pdb.gimp_image_get_layer_by_name(image, TEMPLATE_REBEL)
    templates_dict[TEMPLATE_REBEL] = template_rebel_layer

  # Dark Side
  if dark_light == "Dark":
    template_imperial_layer = pdb.gimp_image_get_layer_by_name(image, TEMPLATE_IMPERIAL)
    templates_dict[TEMPLATE_IMPERIAL] = template_imperial_layer

  return templates_dict

def insert_deploy_and_forfeit(image, card_data):
  # Change Deploy Text
  deploy_text_layer = pdb.gimp_image_get_layer_by_name(image, DEPLOY_TEXT_LAYER)
  pdb.gimp_text_layer_set_text(deploy_text_layer, card_data["front"]["deploy"])
  make_visible(deploy_text_layer)

  # Change Forfeit Text
  forfeit_text_layer = pdb.gimp_image_get_layer_by_name(image, FORFEIT_TEXT_LAYER)
  pdb.gimp_text_layer_set_text(forfeit_text_layer, card_data["front"]["forfeit"])
  make_visible(forfeit_text_layer)

def insert_universal_fields(image, card_data):
  # Change Card Title Text
  card_title_layer = pdb.gimp_image_get_layer_by_name(image, CARD_TITLE_TEXT_LAYER)
  pdb.gimp_text_layer_set_text(card_title_layer, card_data["front"]["title"])

  # Change Destiny Text
  destiny_layer = pdb.gimp_image_get_layer_by_name(image, DESTINY_TEXT_LAYER)
  pdb.gimp_text_layer_set_text(destiny_layer, card_data["front"]["destiny"])

  # Change Lore Text
  lore_text_layer = pdb.gimp_image_get_layer_by_name(image, LORE_TEXT_LAYER)
  format_and_change_lore_text(card_data, lore_text_layer)

  # Change Game Text
  game_text_layer = pdb.gimp_image_get_layer_by_name(image, GAME_TEXT_LAYER)
  pdb.gimp_text_layer_set_text(game_text_layer, card_data["front"]["gametext"])

def format_and_change_lore_text(card_data, lore_text_layer):
  output = ""
  if "lore" in card_data["front"]:
    output = LORE_SPACER + card_data["front"]["lore"]
  """
  output_count = 0
  
  # First line of lore needs spacing
  first_line = True
  max_chars_first_line = LORE_FIRST_LINE_MAX_CHARS
  max_chars_first_line += len( LORE_SPACER ) + len( LORE_SPACER )

  output += LORE_SPACER
  output_count += len( LORE_SPACER )

  # Go through each word.
  str_array = card_data["front"]["lore"].split(' ')
  for word in str_array:
    to_input = word + " "
    output += to_input
    output_count += len( to_input )

    # Add newline at end of first line
    if first_line and ( output_count + len( LORE_SPACER ) >= max_chars_first_line ):
      output += ( LORE_SPACER + "\n" )
      first_line = False    
  """
  pdb.gimp_text_layer_set_text(lore_text_layer, output)

def insert_art_into_image(image, image_file):
  # Create layer from image
  art_asset_layer = pdb.gimp_file_load_layer(image, image_file)

  # Insert layer into image
  ART_COORDS_LAYER = "Art Coords"
  art_coords_layer= pdb.gimp_image_get_layer_by_name(image, ART_COORDS_LAYER)
  pdb.gimp_image_insert_layer(image, art_asset_layer, art_coords_layer, 0)

  # Scale layer to spec and offset
  local_origin = True
  pdb.gimp_layer_scale(art_asset_layer, ART_WIDTH, ART_HEIGHT, local_origin)
  pdb.gimp_layer_set_offsets(art_asset_layer, ART_OFFSET_X, ART_OFFSET_Y)

#region Helper Functions
def get_card_data(json_file):
    card_data = []

    # Open json file
    with open(json_file, "rt") as json_data:
      card_data = json.loads(json_data.read())[0]

    return card_data

def make_invisible(item):
  pdb.gimp_item_set_visible(item, INVISIBLE)

def make_visible(item):
  pdb.gimp_item_set_visible(item, VISIBLE)
 
#endregion

register(
  "python_fu_get_json_and_image",
  "Creates SWCCG card based on json and image file from user input.",
  "Takes user input of a json and image file. The script then populates the appropriate text fields with the data, chooses a matching template, and inserts the card image.",
  "Chris Hinds", "Chris Hinds", "2021",
  "Automate card creation.",
  "",
  [
    (PF_IMAGE, "image", "takes current image", None),
    (PF_DRAWABLE, "drawable", "Input layer", None),
    (PF_FILE, "json_file", "Json File Input", PLACEHOLDER_JSON),
    (PF_FILE, "image_file", "Image File Input", PLACEHOLDER_IMAGE)
  ],
  [],
  automate_card_creation, menu="<Image>/SWCCG/Full")
 
main()
