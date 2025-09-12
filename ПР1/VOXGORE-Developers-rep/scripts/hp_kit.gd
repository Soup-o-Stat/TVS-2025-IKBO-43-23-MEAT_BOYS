extends Area3D

var type: String = "low"

func _ready():
	self.name="hp_kit"

func _process(delta: float) -> void:
	if WaveHandler.start_wave==true:
		Global.score+=5
		queue_free()
