extends CharacterBody3D

@export var acceleration: float = 15.0
@export var deceleration: float = 20.0

@export var guns_list: Array[String] = ["pistol", "famas", "mg", "ak", "arbalet"]
@export var gun_cooldowns := {"pistol": 0.25, "famas": 0.5, "mg": 0.1, "ak": 0.12, "arbalet": 1.5}
@export var gun_ammo := {"pistol": 12, "famas": 25, "mg": 20, "ak": 30, "arbalet": 999}
@export var current_gun: String = "pistol"

@export var health_state: int = 0
var current_ammo: int
var reloading := false
var can_shoot := true
var shoot_cooldown_timer := 0.0

var melle_damage_get := false
var melle_damage_cooldown := 0.0

var is_shaking := false
var shake_intensity := 0.0
var shake_decay := 0.9
var shake_duration := 0.5
var shake_timer := 0.0
var initial_camera_position: Vector3

var gamepad_aim_active := false
var last_mouse_position := Vector2.ZERO
var current_look_target := Vector3.ZERO
const ROTATION_SPEED := 20.0

var previous_hp: int = PlayerData.hp

var bullet_scenes := {
	"arbalet": preload("res://scenes/arrow.tscn"),
	"default": preload("res://scenes/bullet.tscn")
}

func _ready():
	Input.set_mouse_mode(Input.MOUSE_MODE_HIDDEN)
	$models.rotation.x = 0
	$score_label.text = str(Global.score)
	Global.enemy_kills = 0
	initial_camera_position = $Camera3D.position
	current_ammo = gun_ammo[current_gun]
	previous_hp = PlayerData.hp
	update_hp_parameters()
	change_current_gun()


func _process(delta):
	cursor_handler()
	update_score_label()
	handle_height_reset()
	handle_melee_damage(delta)
	input_events()
	reload_animations_checker()
	look_at_cursor()
	handle_movement(delta)
	move_and_slide()
	handle_camera_shake(delta)
	handle_shoot_cooldown(delta)

func take_damage(amount: int):
	PlayerData.hp -= amount
	update_hp_parameters()

func input_events():
	if PlayerData.softlock: return
	if Input.is_action_just_pressed("reload"):
		reload()
	if Input.is_action_pressed("shoot") and can_shoot:
		shoot()

func handle_movement(delta: float):
	if PlayerData.softlock: return
	
	var input_dir = Input.get_vector("go_left", "go_right", "go_up", "go_down")
	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	if direction != Vector3.ZERO:
		velocity.x = lerp(velocity.x, -direction.x * PlayerData.max_speed, acceleration * delta)
		velocity.z = lerp(velocity.z, -direction.z * PlayerData.max_speed, acceleration * delta)
	else:
		velocity.x = lerp(velocity.x, 0.0, deceleration * delta)
		velocity.z = lerp(velocity.z, 0.0, deceleration * delta)

	if velocity.length() > 0.1:
		$player_anim.play("walk")
	else:
		$player_anim.play("idle")
		velocity = Vector3.ZERO

func update_hp_parameters():
	if PlayerData.hp == previous_hp: return
	
	PlayerData.hp = clamp(PlayerData.hp, 0, 3)
	
	match PlayerData.hp:
		3:
			show_hearts(3)
			$models/LalPlayerHead.mesh = load("res://media/models/lal_player_head.vox")
			health_state = 0
		2:
			show_hearts(2)
			$models/LalPlayerHead.mesh = load("res://media/models/lal_player_head_damaged.vox")
			play_damage_effect(0.2)
			health_state = 1
		1:
			show_hearts(1)
			$models/LalPlayerHead.mesh = load("res://media/models/lal_player_head_high_damaged.vox")
			play_damage_effect(0.3)
			health_state = 2
		0:
			hide_hearts()
			$player_anim.play("death")
			PlayerData.softlock = true

	previous_hp = PlayerData.hp

func play_damage_effect(intensity: float):
	start_shake(intensity)
	$health_down_sound.play()

func show_hearts(amount: int):
	$hearts/Heart.visible = amount >= 1
	$hearts/Heart2.visible = amount >= 2
	$hearts/Heart3.visible = amount >= 3

func hide_hearts():
	$hearts/Heart.hide()
	$hearts/Heart2.hide()
	$hearts/Heart3.hide()

func shoot():
	if not (can_shoot and not reloading and current_ammo > 0): return
	
	var anim_player = get_gun_animation_player(current_gun)
	
	if current_gun == "famas":
		fire_famas_burst(anim_player)
	else:
		current_ammo -= 1
		fire_bullet()
		if anim_player: anim_player.play("shoot")

	can_shoot = false
	shoot_cooldown_timer = gun_cooldowns[current_gun]

func fire_bullet():
	var bullet_scene = bullet_scenes.get(current_gun, bullet_scenes["default"])
	var bullet = bullet_scene.instantiate()
	var marker = $models.get_node(current_gun + "/Marker3D")
	bullet.global_transform = marker.global_transform
	bullet.direction = -marker.global_transform.basis.z
	get_parent().add_child(bullet)

	if current_gun == "arbalet":
		$crossbow_shoot_sound.play()
	else:
		$shoot_sound.play()

	if gamepad_aim_active:
		Input.start_joy_vibration(0, 1, 1, 0.3)

func fire_famas_burst(anim_player):
	for i in range(2): # 2 пули
		if current_ammo <= 0: break
		current_ammo -= 1
		fire_bullet()
		if anim_player: anim_player.play("shoot")
		if i == 0:
			await get_tree().create_timer(0.1).timeout

func reload():
	if reloading: return
	var anim_player = get_gun_animation_player(current_gun)
	if anim_player:
		anim_player.play("reload")
		reloading = true
		current_ammo = gun_ammo[current_gun]

func reload_animations_checker():
	if reloading:
		var anim_player = get_gun_animation_player(current_gun)
		if anim_player and not anim_player.is_playing():
			reloading = false

func change_current_gun():
	for gun in guns_list:
		$models.get_node(gun).visible = (gun == current_gun)
	current_ammo = gun_ammo[current_gun]
	var anim_player = get_gun_animation_player(current_gun)
	if anim_player: anim_player.play("idle")

func get_gun_animation_player(gun: String) -> AnimationPlayer:
	var path = "models/%s/%s_anim" % [gun, gun]
	return get_node(path) if has_node(path) else null

func cursor_handler():
	$Cursor.position = get_viewport().get_mouse_position()

func update_score_label():
	$score_label.text = str(Global.score)

func handle_height_reset():
	if position.y != 0:
		position.y = 0

func handle_melee_damage(delta: float):
	if melle_damage_get and melle_damage_cooldown <= 0:
		take_damage(1)
		melle_damage_cooldown = 300
	
	if melle_damage_cooldown > 0:
		PlayerData.max_speed = 20
		melle_damage_cooldown -= 250 * delta
	else:
		PlayerData.max_speed = 10
		melle_damage_cooldown = 0

func handle_shoot_cooldown(delta: float):
	if not can_shoot:
		shoot_cooldown_timer -= delta
		if shoot_cooldown_timer <= 0:
			can_shoot = true

func start_shake(intensity: float):
	is_shaking = true
	shake_intensity = intensity
	shake_timer = 0.0

func handle_camera_shake(delta: float):
	if not is_shaking: return
	if shake_timer < shake_duration:
		var random_offset = Vector3(
			randf_range(-shake_intensity, shake_intensity),
			randf_range(-shake_intensity, shake_intensity),
			randf_range(-shake_intensity, shake_intensity))
		$Camera3D.position = initial_camera_position + random_offset
		shake_intensity *= shake_decay
		shake_timer += delta
	else:
		$Camera3D.position = initial_camera_position
		is_shaking = false

func look_at_cursor():
	if PlayerData.hp <= 0 or PlayerData.softlock: return
	
	var target_plane = Plane(Vector3.UP, position.y)
	var ray_length = 1000
	var target_position: Vector3
	var current_mouse_position = get_viewport().get_mouse_position()
	var gamepad_aim = Input.get_vector("look_right", "look_left", "look_down", "look_up")

	if gamepad_aim.length() > 0.1:
		gamepad_aim_active = true
		$Cursor.hide()
		target_position = position + Vector3(gamepad_aim.x, 0, gamepad_aim.y).normalized() * 10
	elif current_mouse_position != last_mouse_position:
		gamepad_aim_active = false
		$Cursor.show()

	last_mouse_position = current_mouse_position

	if not gamepad_aim_active:
		var from = $Camera3D.project_ray_origin(current_mouse_position)
		var to = from + $Camera3D.project_ray_normal(current_mouse_position) * ray_length
		target_position = target_plane.intersects_ray(from, to)

	if target_position:
		current_look_target = current_look_target.lerp(target_position, ROTATION_SPEED * get_process_delta_time())
		$models.look_at(current_look_target, Vector3.UP)
		$models.rotate_y(deg_to_rad(180))

func _on_damage_collision_area_entered(area: Area3D) -> void:
	if area.name.begins_with("attack_area"):
		melle_damage_get = true
	elif area.name.begins_with("weapon_box") and is_instance_valid(area):
		current_gun = area.in_the_box
		change_current_gun()
		area.call_deferred("queue_free")
	elif area.name.begins_with("hp_kit") and is_instance_valid(area):
		PlayerData.hp += 1
		$heal_sound.play()
		$heal_particles.emitting = true
		update_hp_parameters()
		area.call_deferred("queue_free")

func _on_damage_collision_area_exited(area: Area3D) -> void:
	if area.name.begins_with("attack_area"):
		melle_damage_get = false

func _on_player_anim_animation_finished(anim_name: StringName):
	if anim_name == "death":
		$ColorRect/AnimationPlayer.play("transition")

func _on_animation_player_animation_finished(anim_name: StringName):
	if anim_name == "transition":
		get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
