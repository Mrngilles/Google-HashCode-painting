input_file = 'right_angle.in'
output_file = 'right_angle.out'

# Read input
def read_input():
	wall = None
	with open(input_file) as f:
	    lines = f.readlines()
	    count = 0
	    for line in lines:
			if (count == 0):
				num_rows = int(line.split()[0])
				num_cols = int(line.split()[1])
			else:
				if wall == None: 
					wall = [['.' for x in range(num_cols)] for x in range(num_rows)]
				wall[count - 1] = line[0:-1]
			count += 1
	return wall, num_rows, num_cols

# scan for lines (horizontal)
cells_cover_by_rows = 0
def scan_lines(wall):
	map_lines = dict()
	row_count = 0

	for (index, row) in enumerate(wall):
		list_lines = []
		# print row
		start_position = -1
		end_position = -1
		position = 0
		for cell in row:
			if start_position == -1 and cell == '#':
				start_position = position
			
			if ( ((position + 1 < len(row) and row[position + 1] == '.') or (position == len(row) - 1 and cell == '#') ) 
				and start_position != -1 and end_position == -1):
				end_position = position
			
			if start_position != -1 and end_position != -1:
				# found a line
				# print start_position, end_position
				list_lines.append( (start_position, end_position) )
				start_position = -1
				end_position = -1
				row_count += 1
				# cells_cover_by_rows += (end_position - start_position + 1)
			
			position += 1

		map_lines[index] = list_lines
	return row_count, map_lines

def scan_columns(wall):
	map_lines = dict()
	col_count = 0
	for col in range(num_cols):
		list_lines = []
		start_position = -1
		end_position = -1
		for position in range(num_rows):
			cell = wall[position][col]
			if start_position == -1 and cell == '#':
				start_position = position
			
			if (( (position + 1 < num_rows and wall[position + 1][col] == '.') or (position == num_rows - 1 and cell == '#') ) 
				and start_position != -1 and end_position == -1):
				end_position = position
			
			if start_position != -1 and end_position != -1:
				# found a line
				# print end_position - start_position + 1#, start_position, end_position
				# print start_position, end_position
				start_position = -1
				end_position = -1
				col_count += 1
				list_lines.append( (start_position, end_position) )
		map_lines[col] = list_lines
	return col_count

def search_rectangle(map_lines, num_rows, num_cols):
	# print map_lines
	left = 0
	right = num_cols - 1
	top = None
	bottom = num_rows - 1
	for row in range(num_rows):
		list_lines = map_lines.get(row, None)
		# print 'row'
		# print list_lines
		if list_lines:
			if top == None:
				top = row
			# list_lines_above = map_lines.get(row - 1, None)	
			list_lines_below = map_lines.get(row + 1, None)	
			first_line = list_lines[0]
			updated = False
			for (start_position, end_position) in list_lines_below:
				if start_position >= left and start_position <= right:
					left = start_position
					bottom = row + 1
					updated = True
					# print 'Update left'
				if end_position <= right and end_position >= left:
					right = end_position
					bottom = row + 1
					updated = True
					# print 'Update right'
				if start_position < left and right < end_position:
					bottom = row + 1
					updated = True
					# return left, right, top, bottom
				# print 'start-end'
				# print start_position, end_position
				# print left, right, top, bottom
			if not updated:
				return left, right, top, bottom
	return left, right, top, bottom

def clear_rectangle(left, right, top, bottom):
	for row in range(top, bottom + 1):
		l = list(wall[row])
		for col in range(left, right + 1):
			l[col] = '.'
		wall[row] = "".join(l)		

def generate_output_file(map_lines, row_count, num_rows):
	with open(output_file, 'w') as f:
		# print map_lines
		f.write(str(row_count) + '\n')
		for row in range(num_rows):
			list_lines = map_lines.get(row, None)
			if list_lines:
				for (start_position, end_position) in list_lines:
					# print 'PAINT_LINE {} {} {} {}'.format(row, start_position, row, end_position)
					f.write('PAINT_LINE %d %d %d %d\n' % (row, start_position, row, end_position)) 


# print 'row count', row_count
# print 'col count', col_count
# wall, num_rows = read_input()
# row_count, map_lines = scan_lines(wall)
# generate_output_file(map_lines, row_count, num_rows)

wall, num_rows, num_cols = read_input()
for i in range(20):
	row_count, map_lines = scan_lines(wall)
	rect = search_rectangle(map_lines, num_rows, num_cols)
	print rect
	print 'width', rect[1] - rect[0] + 1
	print 'height', rect[3] - rect[2] + 1
	print
	clear_rectangle(*rect)
	# for row in range(0, 10):
	# 	print wall[row][0:20]
	# print

