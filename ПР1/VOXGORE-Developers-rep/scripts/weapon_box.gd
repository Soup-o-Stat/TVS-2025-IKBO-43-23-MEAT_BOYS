extends Area3D

var weapons_in_the_box=["famas", "mg", "ak", "pistol", "arbalet"]
var in_the_box="gun"

func _ready():
	var box_chance=randi()%len(weapons_in_the_box)
	self.in_the_box=weapons_in_the_box[box_chance]
	self.name="weapon_box"

func _process(delta: float) -> void:
	if WaveHandler.start_wave==true:
		Global.score+=5
		queue_free()
