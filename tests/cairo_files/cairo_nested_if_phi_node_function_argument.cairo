func testfunc(arg, arg2):
    ret
end

func main{}():
	[ap] = 3; ap++
	if [ap-1] == 3:
		[ap] = 10

		if [ap-1] == 5:
			[ap] = 6; ap++
		else:
			[ap] = 1; ap++
		end
	else:
		if [ap-1] == 4:
			[ap] = 7; ap++
		else:
			[ap] = 2; ap++
		end
	end
    testfunc([ap-1], 2)
	ret
end