Minimize
	0 E1_0 + 0 E1_0 + 0 E2_0 + 4 E3_4 + 5 E3_5 + 6 E3_6 + 7 E3_7 + 8 E3_8 + 9 E3_9 + 10 E3_10 + 4 E4_4 + 15 E5_15
Subject To
	c1: E1_0 = 1
	c2: E2_0 = 1
	c3: E3_4 + E3_5 + E3_6 + E3_7 + E3_8 + E3_9 + E3_10 = 1
	c4: E4_4 = 1
	c5: E5_15 = 1
	c6: 0 E2_0 - 0 E1_0 >= 0
	c7: 4 E3_4 + 5 E3_5 + 6 E3_6 + 7 E3_7 + 8 E3_8 + 9 E3_9 + 10 E3_10 - 0 E2_0 >= 4
	c8: 4 E4_4 - 0 E2_0 >= 4
	c9: 15 E5_15 - 4 E3_4 - 5 E3_5 - 6 E3_6 - 7 E3_7 - 8 E3_8 - 9 E3_9 - 10 E3_10 >= 5
	c10: 15 E5_15 - 4 E4_4 >= 11
	c11: 0 <= 1
	c12: 0 E2_0 <= 1
	c13: 0 E3_0 +  E3_1 +  E3_2 +  E3_3 +  E3_4 <= 1
	c14: 0 E3_1 +  E3_2 +  E3_3 +  E3_4 +  E3_5 <= 1
	c15: 0 E3_2 +  E3_3 +  E3_4 +  E3_5 +  E3_6 <= 1
	c16: 0 E3_3 +  E3_4 +  E3_5 +  E3_6 +  E3_7 <= 1
	c17: 0 E3_4 +  E3_5 +  E3_6 +  E3_7 +  E3_8 <= 1
	c18: 0 E3_5 +  E3_6 +  E3_7 +  E3_8 +  E3_9 <= 1
	c19: 0 E3_6 +  E3_7 +  E3_8 +  E3_9 +  E3_10 <= 1
	c20: 0 E4_0 +  E4_1 +  E4_2 +  E4_3 +  E4_4 <= 1
	c21: 0 <= 1
Bounds
	0 <= E1_0 <= 1
	0 <= E2_0 <= 1
	0 <= E3_4 <= 1
	0 <= E3_5 <= 1
	0 <= E3_6 <= 1
	0 <= E3_7 <= 1
	0 <= E3_8 <= 1
	0 <= E3_9 <= 1
	0 <= E3_10 <= 1
	0 <= E4_4 <= 1
	0 <= E5_15 <= 1
Integers
	E1_0
	E2_0
	E3_4
	E3_5
	E3_6
	E3_7
	E3_8
	E3_9
	E3_10
	E4_4
	E5_15
End