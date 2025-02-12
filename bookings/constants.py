hotel_details_schema ={
  "type": "object",
  "properties": {
    "hotel": {
      "type": "string",
      "title": "Hotel Name"
    },
    "room_type": {
      "type": "string",
      "title": "Room Type",
      "enum": ["suite", "single_room", "studio", "deluxe_room"],
      "enumNames": ["Suite", "Single Room", "Studio", "Deluxe Room"]
    },
    "room_no": {
      "type": "integer",
      "title": "Room Number",
      "minimum": 1
    }
  }
}
