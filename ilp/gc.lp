Minimize
	y1 + y2 + y3
Subject To
	v1: x11 + x12 + x13 = 1
	v2: x21 + x22 + x23 = 1
	v3: x31 + x32 + x33 = 1	
	
	d1: x11 - y1 <= 0
	d2: x12 - y2 <= 0
	d3: x13 - y3 <= 0
	d4: x21 - y1 <= 0
	d5: x22 - y2 <= 0
	d6: x23 - y3 <= 0	
	d7: x31 - y1 <= 0
	d8: x32 - y2 <= 0
	d9: x33 - y3 <= 0
	
	e1: x11 + x21 <= 1
	e2: x11 + x31 <= 1
	e3: x21 + x31 <= 1	
	e4: x12 + x22 <= 1
	e5: x12 + x32 <= 1
	e6: x22 + x32 <= 1	
	e7: x13 + x23 <= 1
	e8: x13 + x33 <= 1
	e9: x23 + x33 <= 1	
Bounds
	0 <= x11 <= 1	
	0 <= x12 <= 1	
	0 <= x13 <= 1	
	
	0 <= x21 <= 1	
	0 <= x22 <= 1	
	0 <= x23 <= 1
	
	0 <= x31 <= 1	
	0 <= x32 <= 1	
	0 <= x33 <= 1
	
	0 <= y1 <= 1	
	0 <= y2 <= 1
	0 <= y3 <= 1
Integers
	x11 x12 x13 x21 x22 x23 x31 x32 x33 y1 y2 y3
End