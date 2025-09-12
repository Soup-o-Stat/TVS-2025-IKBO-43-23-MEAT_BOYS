extends Node2D

func _ready():
	$Label.text="YOUR SCORE: "+str(Global.score)
