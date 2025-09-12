extends AudioStreamPlayer

func play_music(name):
	stream=load("res://media/music/"+str(name))
	play()
