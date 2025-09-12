extends StaticBody3D

var player_in_shop=false
var player_buying=false

func _on_shop_area_area_entered(area: Area3D) -> void:
	if area.name.substr(0, 16)=="damage_collision" and WaveHandler.start_wave==false:
		player_in_shop=true

func _on_shop_area_area_exited(area: Area3D) -> void:
	if area.name.substr(0, 16)=="damage_collision":
		player_in_shop=false

func _process(delta: float) -> void:
	if Input.is_action_just_pressed("interact") and player_buying==false and player_in_shop:
		PlayerData.softlock=true
		$Node2D.show()
		player_buying=true
	if Input.is_action_just_pressed("back") and player_buying:
		$Node2D.hide()
		player_buying=false
		PlayerData.softlock=false
		
