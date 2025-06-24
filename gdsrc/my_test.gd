extends Node

func _ready():
    var result = 4 * pow(2, 3)
    print("Result: ", result)
    get_tree().quit()
