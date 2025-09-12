extends Area3D

@export var speed: float = 50.0
@export var lifetime: float = 5.0

var direction: Vector3 = Vector3.ZERO
var has_hit: bool=false

func _ready():
	self.name="bullet"
	set_process(true)
	rotate_y(deg_to_rad(90))

func _process(delta):
	global_translate(direction * speed * delta*-1)
	if self.has_hit==true:
		queue_free()
