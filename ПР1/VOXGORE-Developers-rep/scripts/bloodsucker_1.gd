extends CharacterBody3D

@export var speed: float = 3.0
@export var hp: int = 50
@export var inertia: float = 1.0

var player: Node3D = null
var dead_actions: bool=false

func _ready():
	player = $"../player"

func _process(delta):
	if position.y>0:
		position.y=0
	if inertia<1:
		inertia+=0.1
	if inertia>11:
		inertia=1
	if player != null and hp>0:
		if $AnimationPlayer.is_playing()==false:
			$AnimationPlayer.play("walk")
		var distance_to_player = global_position.distance_to(player.global_position)
		look_at(player.global_position)
		var direction = (player.global_position - global_position).normalized()
		velocity = direction * speed * inertia
		move_and_slide()
	if self.hp<=0:
		if self.dead_actions==false:	
			Global.enemies_on_arena-=1
			if Global.enemies_on_arena<0:
				Global.enemies_on_arena=0
			$AnimationPlayer.play("death")
			Global.enemy_kills+=1
			Global.score+=1
			if $attack_area/CollisionShape3D.disabled==false:
				$attack_area/CollisionShape3D.disabled=true
			dead_actions=true
		position.y-=0.05
		if position.y<-100:
			queue_free()
		
func _on_area_3d_area_entered(area):
	if area.name.substr(0, 6) == "bullet" and not area.has_hit:
		$AnimationPlayer.play("hit_left")
		self.hp -= 20
		$AudioStreamPlayer3D2.play()
		$blood.emitting = true
		inertia=-2
	if area.name.substr(0, 5) == "arrow":
		$AnimationPlayer.play("hit_left")
		self.hp -= 25
		$AudioStreamPlayer3D2.play()
		$blood.emitting = true
		inertia=-2

func _on_hit_right_area_entered(area: Area3D) -> void:
	if area.name.substr(0, 6) == "bullet" and not area.has_hit:
		$AnimationPlayer.play("hit_right")
		$AudioStreamPlayer3D2.play()
		self.hp -= 20
		$blood.emitting = true
		area.has_hit = true
		inertia=-2
	if area.name.substr(0, 5) == "arrow":
		$AnimationPlayer.play("hit_right")
		$AudioStreamPlayer3D2.play()
		self.hp -= 25
		$blood.emitting = true
		inertia=-2

func _on_hit_center_area_entered(area: Area3D) -> void:
	if area.name.substr(0, 6) == "bullet" and not area.has_hit:
		$AnimationPlayer.play("hit_center")
		$AudioStreamPlayer3D2.play()
		self.hp -= 20
		$blood.emitting = true
		area.has_hit = true
		inertia=-2
	if area.name.substr(0, 5) == "arrow":
		$AnimationPlayer.play("hit_center")
		$AudioStreamPlayer3D2.play()
		self.hp -= 25
		$blood.emitting = true
		inertia=-2
